#!/usr/bin/env python3
"""Validate handoff-entry inventories with optional storage-neutral adapter helpers."""

import argparse
import copy
import hashlib
import json
import posixpath
from datetime import datetime
from pathlib import Path

INVALID = {
    "invalid",
    "erroneous",
    "incomplete",
    "quarantined",
    "wrong_predecessor",
    "unsuitable_for_continuity",
}
FIELDS = {
    "entry_id",
    "entry_type",
    "journal_id",
    "title",
    "handoff_series_id",
    "handoff_series_title",
    "handoff_sequence",
    "predecessor_entry_id",
    "predecessor_entry_title",
    "coverage_start_exclusive",
    "coverage_end_inclusive",
    "source_ledger",
    "entry_created_at",
    "supersedes_entry_id",
    "correction_reason",
    "invalidation_status",
    "invalidation_reason",
    "content",
    "provenance",
    "updated_at",
    "status",
    "checksum",
    "immutable_path",
    "full_read",
}


class AmbiguityError(ValueError):
    """Machine-readable failure with exact candidate identities."""

    def __init__(self, reason, entries=()):
        self.report = {
            "status": "blocked",
            "reason": reason,
            "candidates": [
                {
                    "entry_id": e.get("entry_id"),
                    "title": e.get("title"),
                    "handoff_sequence": e.get("handoff_sequence"),
                    "failure_reason": reason,
                }
                for e in entries
            ],
        }
        super().__init__(json.dumps(self.report, ensure_ascii=False))


def fail(reason, *entries):
    raise AmbiguityError(reason, entries)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    if not nonempty(value):
        raise ValueError("Timezone-qualified timestamp required")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timezone-qualified timestamp required")
    return parsed


def digest(entry):
    """SHA-256 of exact UTF-8 content; not proof of provenance authenticity."""
    return hashlib.sha256(entry["content"].encode("utf-8")).hexdigest()


def identify(entry):
    result = copy.deepcopy(entry)
    if not nonempty(result.get("entry_id")):
        path = result.get("immutable_path")
        if (
            not nonempty(path)
            or posixpath.normpath(path) != path
            or not path.startswith("/")
            or not nonempty(result.get("content"))
            or result.get("checksum") != digest(result)
        ):
            fail(
                "Stable ID or immutable normalized path and verified SHA-256 required",
                result,
            )
        result["entry_id"] = "path:" + path + "@sha256:" + result["checksum"]
    return result


def validate_entry(entry):
    """Clean entry schema and cross-field checks; never normalize title formats."""
    if not isinstance(entry, dict):
        fail("Entry must be an object")
    e = identify(entry)
    if set(e) - FIELDS:
        fail("Unknown entry fields: " + ", ".join(sorted(set(e) - FIELDS)), e)
    required_text = (
        "entry_id",
        "journal_id",
        "handoff_series_id",
        "handoff_series_title",
        "title",
        "content",
    )
    if e.get("entry_type") != "therapist_handoff" or any(
        not nonempty(e.get(k)) for k in required_text
    ):
        fail("Required identity, type, title, or content missing", e)
    n = e.get("handoff_sequence")
    if type(n) is not int or n < 1:
        fail("Sequence number must be a positive integer", e)
    if e["title"] != f"{e['handoff_series_title']} — Entry {n}":
        fail("Canonical title and sequence metadata must agree", e)
    if e.get("full_read") is not True:
        fail("Entry cannot be retrieved in full", e)
    if "checksum" in e and e["checksum"] != digest(e):
        fail("Content checksum mismatch", e)
    try:
        timestamp(e["entry_created_at"])
        if "updated_at" in e:
            timestamp(e["updated_at"])
    except (KeyError, TypeError, ValueError):
        fail("Invalid creation or update timestamp", e)
    if e.get("predecessor_entry_id") == e["entry_id"]:
        fail("Entry cannot point to itself", e)
    if n == 1 and (
        e.get("predecessor_entry_id") is not None
        or e.get("predecessor_entry_title") is not None
    ):
        fail("Initial handoff entry must have no predecessor", e)
    invalid = e.get("invalidation_status")
    if invalid is not None:
        if (
            not isinstance(invalid, str)
            or invalid not in INVALID
            or not nonempty(e.get("invalidation_reason"))
        ):
            fail("Explicit supported invalidation and reason required", e)
        # Retain explicitly invalid branch evidence without accepting its continuity.
        return e
    if "invalidation_reason" in e:
        fail("Invalidation reason without invalidation status", e)
    if n > 1 and (
        not nonempty(e.get("predecessor_entry_id"))
        or not nonempty(e.get("predecessor_entry_title"))
    ):
        fail("Later entry requires predecessor ID and exact title", e)
    try:
        start = timestamp(e["coverage_start_exclusive"])
        end = timestamp(e["coverage_end_inclusive"])
        if end <= start or end > timestamp(e["entry_created_at"]):
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        fail("Invalid coverage interval", e)
    ledger = e.get("source_ledger")
    if not isinstance(ledger, list) or not ledger:
        fail("Nonempty source ledger required", e)
    for source in ledger:
        if not isinstance(source, dict) or any(
            not nonempty(source.get(k))
            for k in (
                "source_id",
                "title",
                "source_date",
                "retrieved_at",
                "inclusion_role",
            )
        ):
            fail("Source ledger lacks identity, dates, retrieval, or inclusion role", e)
        try:
            timestamp(source["retrieved_at"])
        except ValueError:
            fail("Invalid source retrieval timestamp", e)
    provenance = e.get("provenance")
    if not isinstance(provenance, dict) or any(
        not nonempty(provenance.get(k)) for k in ("origin", "operation_id")
    ):
        fail("Provenance origin and operation ID required", e)
    correction = e.get("supersedes_entry_id")
    if correction is not None:
        if (
            not nonempty(correction)
            or correction == e["entry_id"]
            or not nonempty(e.get("correction_reason"))
        ):
            fail(
                "Replacement requires distinct target and explicit correction reason", e
            )
    elif "correction_reason" in e:
        fail("Correction reason requires a replacement target", e)
    return e


def select(inventory):
    """Pure resolver. The caller must actually establish enumeration evidence."""
    if not isinstance(inventory, dict):
        fail("Inventory must be an object")
    scope = ("journal_id", "handoff_series_id", "handoff_series_title")
    if any(not nonempty(inventory.get(k)) for k in scope):
        fail("Exact journal and handoff series identity required")
    if inventory.get("complete") is not True or not nonempty(
        inventory.get("enumeration_evidence")
    ):
        fail("Complete enumeration and traversal evidence required")
    if not isinstance(inventory.get("entries"), list):
        fail("Entries must be an array")
    by_id = {}
    for raw in inventory["entries"]:
        e = validate_entry(raw)
        if any(e[k] != inventory[k] for k in scope):
            fail("Mixed journal or handoff series inventory", e)
        if e["entry_id"] in by_id and by_id[e["entry_id"]] != e:
            fail("Conflicting reads of the same stable ID", by_id[e["entry_id"]], e)
        by_id[e["entry_id"]] = e
    audit = sorted(by_id.values(), key=lambda e: e["handoff_sequence"])
    by_sequence = {}
    for e in audit:
        n = e["handoff_sequence"]
        if n in by_sequence:
            fail("Duplicate-sequence conflict", by_sequence[n], e)
        by_sequence[n] = e
    valid = [e for e in audit if not e.get("invalidation_status")]
    previous = None
    for e in valid:
        if previous is None:
            if e["handoff_sequence"] != 1:
                fail("Initial handoff entry or predecessor missing", e)
        else:
            if (
                e.get("predecessor_entry_id") != previous["entry_id"]
                or e.get("predecessor_entry_title") != previous["title"]
            ):
                fail("Missing or wrong predecessor; conflicting lineage", e, previous)
            if not e.get("supersedes_entry_id") and (
                timestamp(e["coverage_start_exclusive"])
                != timestamp(previous["coverage_end_inclusive"])
            ):
                fail("Coverage must continue from predecessor cutoff", e, previous)
            if timestamp(e["coverage_end_inclusive"]) < timestamp(
                previous["coverage_end_inclusive"]
            ):
                fail("Coverage cutoff cannot move backward", e, previous)
        if e.get("supersedes_entry_id"):
            target = by_id.get(e["supersedes_entry_id"])
            if target is None or target["handoff_sequence"] >= e["handoff_sequence"]:
                fail("Replacement target must be an earlier entry in this series", e)
        previous = e
    if audit and not valid:
        fail("Series has no validated initial handoff entry", *audit)
    warnings = []
    pointer = inventory.get("latest_entry_id")
    if pointer and (previous is None or pointer != previous["entry_id"]):
        warnings.append(
            "Latest-entry pointer is stale or unresolved; enumeration is authoritative"
        )
    if any("immutable_path" in e for e in audit):
        warnings.append(
            "Fallback path/checksum identity: reduced identity and concurrency guarantees"
        )
    return {
        "latest_entry": previous,
        "proposed_sequence": previous["handoff_sequence"] + 1 if previous else 1,
        "audit_inventory": audit,
        "warnings": warnings,
    }


def collect(adapter, scope):
    """Exhaustive adapter traversal followed by full exact reads."""
    inventory = adapter.enumerate_series(scope)
    if any(inventory.get(k) != v for k, v in scope.items()):
        fail("Adapter returned the wrong scope")
    if inventory.get("complete") is not True:
        fail("Enumeration incomplete")
    if not isinstance(inventory.get("entries"), list):
        fail("Enumeration must return an entries array")
    full = []
    for candidate in inventory["entries"]:
        identity = identify(candidate)
        fetched = adapter.retrieve_entry(identity["entry_id"])
        if fetched is None:
            fail("Entry cannot be retrieved in full", identity)
        fetched = identify(fetched)
        if fetched["entry_id"] != identity["entry_id"]:
            fail("Exact read returned another identity", identity, fetched)
        for key in ("title", "handoff_sequence", "handoff_series_id"):
            if fetched.get(key) != identity.get(key):
                fail("Entry changed during enumeration; re-resolve", identity, fetched)
        full.append(fetched)
    inventory = dict(inventory, entries=full)
    select(inventory)
    return inventory


def create_next(adapter, scope, prepared):
    """Verify before creation and pointer commit; never silently rebase content.

    Adapters use conditional creation when supported and disclose weaker behavior.
    An uncertain write is reconciled by operation ID, never retried blindly here.
    """
    before = select(collect(adapter, scope))
    refreshed = select(collect(adapter, scope))
    if before["audit_inventory"] != refreshed["audit_inventory"]:
        fail(
            "Series changed before write; re-resolve and rebuild",
            *refreshed["audit_inventory"],
        )
    e = validate_entry(dict(prepared, full_read=True))
    if (
        any(e[k] != scope[k] for k in scope)
        or e["handoff_sequence"] != refreshed["proposed_sequence"]
    ):
        fail("Prepared entry does not match scope and proposed sequence", e)
    if adapter.find_sequence(scope, e["handoff_sequence"]):
        latest = select(collect(adapter, scope))
        fail(
            "Proposed sequence claimed; re-resolved, rebuild before retry",
            *latest["audit_inventory"],
        )
    select(
        dict(
            scope,
            complete=True,
            enumeration_evidence="validated pre-write snapshot",
            entries=refreshed["audit_inventory"] + [e],
        )
    )
    created_id = adapter.create_entry(e, expected_entries=refreshed["audit_inventory"])
    readback = adapter.retrieve_entry(created_id)
    if readback is None:
        fail(
            "New entry read-back failed; pointer and cutoff unchanged",
            dict(e, entry_id=created_id),
        )
    verified = validate_entry(readback)
    if verified != dict(e, entry_id=created_id):
        fail("Created entry differs from prepared content or metadata", verified, e)
    after = select(collect(adapter, scope))
    if after["latest_entry"] != verified:
        fail("New entry is not the sole validated latest entry", verified)
    remaining = [r for r in after["audit_inventory"] if r["entry_id"] != created_id]
    if remaining != refreshed["audit_inventory"]:
        fail("Prior entries changed; pointer and cutoff unchanged", *remaining)
    adapter.commit_latest(scope, verified, expected_entries=after["audit_inventory"])
    if not getattr(adapter, "supports_atomic", False):
        after["warnings"].append(
            "Backend lacks atomic support; pre/post checks cannot eliminate races"
        )
    return after


def intermediate(adapter, scope):
    """Read-only resolution: never allocate or mutate an entry, pointer or source."""
    result = select(collect(adapter, scope))
    result.pop("proposed_sequence")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(select(json.loads(args.inventory.read_text())), indent=2))
    except AmbiguityError as error:
        parser.exit(2, json.dumps(error.report, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
