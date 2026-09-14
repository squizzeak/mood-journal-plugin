import copy
import importlib.util
import json
import re
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "plugins/mood-journal/skills/mood-journal"
spec = importlib.util.spec_from_file_location(
    "select_handoff", SKILL / "scripts/select_handoff.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SCOPE = {
    "journal_id": "fictional-journal",
    "handoff_series_id": "fictional-week-1",
    "handoff_series_title": "Weekly Therapist Handoff — 2026-09-07",
}


def record(n, scope=None):
    scope = scope or SCOPE
    e = dict(
        scope,
        entry_id=f"{scope['handoff_series_id']}-entry-{n}",
        entry_type="therapist_handoff",
        handoff_sequence=n,
        title=f"{scope['handoff_series_title']} — Entry {n}",
        coverage_start_exclusive=f"2026-09-{n:02d}T00:00:00Z",
        coverage_end_inclusive=f"2026-09-{n + 1:02d}T00:00:00Z",
        entry_created_at=f"2026-09-{n + 1:02d}T00:00:00Z",
        content="Fictional handoff account.",
        full_read=True,
        provenance={"origin": "fictional test", "operation_id": f"operation-{n}"},
        source_ledger=[
            {
                "source_id": f"source-{n}",
                "title": "Fictional observation",
                "source_date": f"2026-09-{n:02d}",
                "retrieved_at": f"2026-09-{n + 1:02d}T00:00:00Z",
                "inclusion_role": "current self-report",
            }
        ],
    )
    if n > 1:
        e.update(
            predecessor_entry_id=f"{scope['handoff_series_id']}-entry-{n - 1}",
            predecessor_entry_title=f"{scope['handoff_series_title']} — Entry {n - 1}",
        )
    return e


def inventory(entries, **kwargs):
    return dict(
        SCOPE,
        entries=entries,
        complete=True,
        enumeration_evidence="Fictional adapter exhausted all pages",
        **kwargs,
    )


def chain(n):
    return [record(i) for i in range(1, n + 1)]


class FakeAdapter:
    """Fictional semantic adapter with observable reads and writes."""

    def __init__(self, entries):
        self.entries = copy.deepcopy(entries)
        self.calls = []
        self.unreadable = set()
        self.complete = True
        self.collision = None
        self.post_collision = None
        self.break_readback = False
        self.change_prior = False
        self.pointer = None
        self.cutoff = None

    def enumerate_series(self, scope):
        self.calls.append("enumerate")
        result = dict(
            scope,
            entries=copy.deepcopy(self.entries),
            complete=self.complete,
            enumeration_evidence="All fictional pages exhausted",
        )
        return result

    def retrieve_entry(self, identifier):
        self.calls.append("read")
        if identifier in self.unreadable:
            return None
        return next(
            (
                copy.deepcopy(e)
                for e in self.entries
                if module.identify(e)["entry_id"] == identifier
            ),
            None,
        )

    def find_sequence(self, scope, sequence):
        self.calls.append("find_pair")
        if self.collision:
            self.entries.append(self.collision)
            self.collision = None
        return [
            e
            for e in self.entries
            if e["handoff_series_id"] == scope["handoff_series_id"]
            and e["handoff_sequence"] == sequence
        ]

    def create_entry(self, entry, expected_entries):
        self.calls.append("create")
        self.entries.append(copy.deepcopy(entry))
        if self.break_readback:
            self.unreadable.add(entry["entry_id"])
        if self.post_collision:
            self.entries.append(self.post_collision)
        if self.change_prior:
            self.entries[0]["content"] = "External edit"
        return entry["entry_id"]

    def commit_latest(self, scope, entry, expected_entries):
        self.calls.append("commit_pointer")
        self.pointer = entry["entry_id"]
        self.cutoff = entry["coverage_end_inclusive"]


class HandoffSelectionTests(unittest.TestCase):
    def blocked(self, entries, reason):
        with self.assertRaises(module.AmbiguityError) as caught:
            module.select(inventory(entries))
        self.assertIn(reason, caught.exception.report["reason"])
        return caught.exception.report

    def test_results_2_8_9_select_9(self):
        entries = chain(9)
        ordered = [entries[1], entries[7], entries[8]] + [
            e for e in entries if e["handoff_sequence"] not in (2, 8, 9)
        ]
        result = module.select(inventory(ordered))
        self.assertEqual(result["latest_entry"]["handoff_sequence"], 9)
        self.assertEqual(result["proposed_sequence"], 10)

    def test_numeric_2_9_10_proposes_11(self):
        entries = chain(10)
        result = module.select(
            inventory([entries[1], entries[8], entries[9]] + entries[:1] + entries[2:8])
        )
        self.assertEqual(result["latest_entry"]["handoff_sequence"], 10)
        self.assertEqual(result["proposed_sequence"], 11)

    def test_canonical_title_and_metadata_agree(self):
        self.assertEqual(module.validate_entry(record(10))["handoff_sequence"], 10)

    def test_title_metadata_disagree(self):
        e = record(10)
        e["handoff_sequence"] = 9
        self.blocked(chain(9) + [e], "title")

    def test_noncanonical_titles_rejected(self):
        for suffix in ("v10", "#10", "version 10", "revision 10"):
            with self.subTest(suffix=suffix):
                e = record(10)
                e["title"] = SCOPE["handoff_series_title"] + " — " + suffix
                self.blocked(chain(9) + [e], "title")

    def test_explicit_invalid_branch_retained(self):
        entries = chain(9)
        entries[2].update(
            invalidation_status="wrong_predecessor",
            invalidation_reason="Explicit fictional invalid branch",
        )
        entries[3].update(
            predecessor_entry_id=entries[1]["entry_id"],
            predecessor_entry_title=entries[1]["title"],
            coverage_start_exclusive=entries[1]["coverage_end_inclusive"],
        )
        result = module.select(inventory(entries))
        self.assertEqual(result["latest_entry"]["handoff_sequence"], 9)
        self.assertEqual(len(result["audit_inventory"]), 9)
        self.assertEqual(
            result["audit_inventory"][2]["invalidation_status"], "wrong_predecessor"
        )

    def test_duplicate_sequence_reports_both_ids(self):
        duplicate = record(10)
        duplicate["entry_id"] = "other-claim"
        report = self.blocked(chain(10) + [duplicate], "Duplicate-sequence")
        self.assertEqual(
            {e["entry_id"] for e in report["candidates"]},
            {record(10)["entry_id"], "other-claim"},
        )

    def test_archived_predecessor_valid(self):
        entries = chain(10)
        entries[8]["status"] = "archived"
        self.assertEqual(module.select(inventory(entries))["proposed_sequence"], 11)

    def test_weekly_series_separate(self):
        other_scope = dict(
            SCOPE,
            handoff_series_id="fictional-week-2",
            handoff_series_title="Weekly Therapist Handoff — 2026-09-14",
        )
        other = [record(i, other_scope) for i in range(1, 11)]
        self.assertEqual(
            module.select(dict(inventory(other), **other_scope))["proposed_sequence"],
            11,
        )
        self.blocked(chain(10) + other, "Mixed")
        wrong_user = record(1)
        wrong_user["journal_id"] = "another-journal"
        self.blocked([wrong_user], "Mixed")

    def test_stale_pointer_is_cross_check(self):
        result = module.select(
            inventory(chain(10), latest_entry_id=record(8)["entry_id"])
        )
        self.assertEqual(result["latest_entry"]["handoff_sequence"], 10)
        self.assertIn("stale", result["warnings"][0])

    def test_wrong_predecessor_and_missing_predecessor(self):
        entries = chain(10)
        entries[-1]["predecessor_entry_id"] = record(8)["entry_id"]
        self.blocked(entries, "predecessor")
        self.blocked(chain(8) + [record(10)], "predecessor")

    def test_incomplete_enumeration_no_writes(self):
        adapter = FakeAdapter(chain(10))
        adapter.complete = False
        with self.assertRaises(module.AmbiguityError):
            module.create_next(adapter, SCOPE, record(11))
        self.assertNotIn("create", adapter.calls)

    def test_latest_unreadable_no_writes(self):
        adapter = FakeAdapter(chain(10))
        adapter.unreadable.add(record(10)["entry_id"])
        with self.assertRaises(module.AmbiguityError):
            module.create_next(adapter, SCOPE, record(11))
        self.assertNotIn("create", adapter.calls)

    def test_concurrent_claim_re_resolves_without_duplicate(self):
        adapter = FakeAdapter(chain(10))
        adapter.collision = record(11)
        with self.assertRaises(module.AmbiguityError) as caught:
            module.create_next(adapter, SCOPE, record(11))
        self.assertIn("re-resolved", caught.exception.report["reason"])
        self.assertNotIn("create", adapter.calls)
        self.assertGreaterEqual(adapter.calls.count("enumerate"), 3)

    def test_new_entry_unreadable_does_not_commit(self):
        adapter = FakeAdapter(chain(10))
        adapter.break_readback = True
        with self.assertRaises(module.AmbiguityError):
            module.create_next(adapter, SCOPE, record(11))
        self.assertIn("create", adapter.calls)
        self.assertIsNone(adapter.pointer)
        self.assertIsNone(adapter.cutoff)

    def test_intermediate_has_zero_mutations_or_allocation(self):
        adapter = FakeAdapter(chain(10))
        original = copy.deepcopy(adapter.entries)
        result = module.intermediate(adapter, SCOPE)
        self.assertEqual(result["latest_entry"]["handoff_sequence"], 10)
        self.assertNotIn("proposed_sequence", result)
        self.assertEqual(adapter.entries, original)
        self.assertTrue(set(adapter.calls) <= {"enumerate", "read"})
        self.assertIsNone(adapter.pointer)
        self.assertIsNone(adapter.cutoff)

    def test_fallback_identity_and_disclosure(self):
        e = record(1)
        del e["entry_id"]
        e["immutable_path"] = "/fictional-store/handoff-entry-1"
        e["checksum"] = module.digest(e)
        result = module.select(inventory([e]))
        self.assertTrue(result["latest_entry"]["entry_id"].startswith("path:"))
        self.assertIn("reduced", result["warnings"][0])
        later = record(2)
        later["predecessor_entry_id"] = result["latest_entry"]["entry_id"]
        self.assertEqual(module.select(inventory([e, later]))["proposed_sequence"], 3)

    def test_empty_series_creates_initial_entry(self):
        adapter = FakeAdapter([])
        result = module.create_next(adapter, SCOPE, record(1))
        self.assertEqual(result["latest_entry"]["handoff_sequence"], 1)
        self.assertNotIn("predecessor_entry_id", adapter.entries[0])
        self.assertEqual(adapter.calls.count("create"), 1)
        self.assertEqual(adapter.pointer, record(1)["entry_id"])

    def test_initial_predecessor_rejected(self):
        for target in (record(1)["entry_id"], "another-entry"):
            e = record(1)
            e.update(predecessor_entry_id=target, predecessor_entry_title="Other")
            self.blocked([e], "Entry" if target == e["entry_id"] else "Initial")

    def test_post_write_collision_no_pointer_commit(self):
        adapter = FakeAdapter(chain(10))
        adapter.post_collision = dict(record(11), entry_id="concurrent-11")
        with self.assertRaises(module.AmbiguityError):
            module.create_next(adapter, SCOPE, record(11))
        self.assertIsNone(adapter.pointer)
        self.assertIsNone(adapter.cutoff)

    def test_prior_entry_change_no_pointer_commit(self):
        adapter = FakeAdapter(chain(10))
        adapter.change_prior = True
        with self.assertRaises(module.AmbiguityError):
            module.create_next(adapter, SCOPE, record(11))
        self.assertIsNone(adapter.pointer)

    def test_valid_creation_preserves_predecessors(self):
        adapter = FakeAdapter(chain(10))
        prior = copy.deepcopy(adapter.entries)
        result = module.create_next(adapter, SCOPE, record(11))
        self.assertEqual(adapter.entries[:-1], prior)
        self.assertEqual(adapter.pointer, record(11)["entry_id"])
        self.assertEqual(adapter.cutoff, record(11)["coverage_end_inclusive"])
        self.assertIn("cannot eliminate races", result["warnings"][0])

    def test_later_self_reference_rejected(self):
        entries = chain(10)
        entries[-1]["predecessor_entry_id"] = entries[-1]["entry_id"]
        self.blocked(entries, "itself")

    def test_invalid_claim_blocks_proposed_pair(self):
        invalid = dict(
            record(11),
            invalidation_status="incomplete",
            invalidation_reason="Explicit incomplete artifact",
        )
        adapter = FakeAdapter(chain(10) + [invalid])
        with self.assertRaises(module.AmbiguityError):
            module.create_next(adapter, SCOPE, record(11))
        self.assertNotIn("create", adapter.calls)

    def test_schema_types_integrity_coverage_and_provenance(self):
        for field, value in (
            ("handoff_sequence", True),
            ("handoff_sequence", "1"),
            ("handoff_sequence", 0),
            ("handoff_series_id", ""),
            ("checksum", "wrong"),
            ("coverage_end_inclusive", "unknown"),
            ("coverage_start_exclusive", "2026-10-01T00:00:00Z"),
            ("source_ledger", []),
            ("provenance", {}),
            ("full_read", False),
            ("unexpected_field", "ignored"),
        ):
            with self.subTest(field=field):
                self.blocked([dict(record(1), **{field: value})], "")

    def test_deliberate_replacement_only(self):
        entries = chain(3)
        entries[-1].update(
            supersedes_entry_id=entries[0]["entry_id"],
            correction_reason="Correct a fictional attribution",
            coverage_start_exclusive=entries[0]["coverage_start_exclusive"],
        )
        self.assertEqual(module.select(inventory(entries))["proposed_sequence"], 4)
        del entries[-1]["correction_reason"]
        self.blocked(entries, "Replacement")

    def test_repeated_observation_deduplicates_stable_id(self):
        result = module.select(inventory(chain(10) + [record(10)]))
        self.assertEqual(len(result["audit_inventory"]), 10)

    def test_schema_document_example(self):
        text = (SKILL / "references/handoff-entry-schema.md").read_text()
        e = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S)[1])
        self.assertEqual(
            module.validate_entry(dict(e, full_read=True))["handoff_sequence"], 1
        )


if __name__ == "__main__":
    unittest.main()
