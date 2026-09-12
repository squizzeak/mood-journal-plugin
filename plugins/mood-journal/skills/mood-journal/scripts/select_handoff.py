#!/usr/bin/env python3
"""Check a caller-supplied handoff inventory; not a discovery or write tool."""
import argparse
import json
import re
from pathlib import Path


def select(inventory):
    if inventory.get("complete") is not True:
        raise ValueError("Complete series inventory required; use an unnumbered draft")
    series = inventory.get("series_id")
    if not isinstance(series, str) or not series.strip():
        raise ValueError("Explicit series identity required")
    records = inventory.get("records")
    if not isinstance(records, list):
        raise ValueError("Records must be an array")
    by_version, by_id = {}, {}
    for record in records:
        if record.get("series_id") != series:
            raise ValueError("Mixed series inventory")
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in by_id:
            raise ValueError("Unique record IDs required")
        value = record.get("version")
        if isinstance(value, bool) or not re.fullmatch(r"v?[1-9][0-9]*", str(value)):
            raise ValueError("Positive integer handoff version required")
        version = int(str(value).removeprefix("v"))
        if version in by_version:
            raise ValueError("Duplicate version requires explicit reconciliation")
        if record.get("disposition") not in ("canonical", "superseded", "invalid", "reserved"):
            raise ValueError("Unresolved draft, failed record, or unknown disposition")
        normalized = dict(record, version=version)
        by_version[version] = normalized
        by_id[identifier] = normalized
    canonical = [r for r in by_version.values() if r["disposition"] == "canonical"]
    if records and len(canonical) != 1:
        raise ValueError("Exactly one resolved canonical parent required")
    if not records:
        return {"next_version": 1, "parent_id": None, "coverage_baseline_id": None}
    parent = canonical[0]
    if parent.get("output_verified") is not True:
        raise ValueError("Unverified parent requires reconciliation")
    if any(r["version"] > parent["version"] and r["disposition"] == "superseded" for r in by_version.values()):
        raise ValueError("Canonical pointer is behind a valid historical version")
    # Follow the explicit predecessor chain, not timestamps or search ranking.
    lineage, seen, current = [], set(), parent
    while current is not None:
        if current["id"] in seen:
            raise ValueError("Cyclic predecessor chain")
        seen.add(current["id"])
        lineage.append(current)
        previous = current.get("parent_id")
        if previous is None:
            break
        if previous not in by_id:
            raise ValueError("Missing predecessor record")
        ancestor = by_id[previous]
        if ancestor["version"] >= current["version"] or ancestor["disposition"] not in ("canonical", "superseded"):
            raise ValueError("Invalid predecessor lineage")
        current = ancestor
    if any(r["disposition"] == "superseded" and r["id"] not in seen for r in by_version.values()):
        raise ValueError("Unresolved alternate lineage")
    baseline = next((r for r in lineage if r.get("output_verified") is True and r.get("coverage_verified") is True and r.get("coverage_end")), None)
    return {"next_version": max(by_version) + 1, "parent_id": parent["id"],
            "coverage_baseline_id": baseline["id"] if baseline else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(select(json.loads(args.inventory.read_text())), indent=2))
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Handoff selection blocked: {error}\n")


if __name__ == "__main__":
    main()
