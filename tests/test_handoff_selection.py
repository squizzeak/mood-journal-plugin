import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "plugins/mood-journal/skills/mood-journal/scripts/select_handoff.py"
spec = importlib.util.spec_from_file_location("select_handoff", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record(version, disposition="canonical", parent=None, coverage=True):
    return {"id": f"fictional-{version}", "series_id": "fictional-series", "version": f"v{version}",
            "disposition": disposition, "parent_id": parent, "output_verified": True,
            "coverage_verified": coverage, "coverage_end": "2026-01-01T00:00:00Z" if coverage else None}


def inventory(*records, complete=True):
    return {"series_id": "fictional-series", "complete": complete, "records": list(records)}


class HandoffSelectionTests(unittest.TestCase):
    def test_old_first_hit_does_not_regress(self):
        old = record(2, "superseded")
        latest = record(8, parent=old["id"])
        result = module.select(inventory(old, latest))
        self.assertEqual(result["next_version"], 9)
        self.assertEqual(result["parent_id"], latest["id"])

    def test_numeric_order_and_invalid_reservation(self):
        older = record(9, "superseded")
        latest = record(10, parent=older["id"])
        invalid = record(11, "invalid")
        result = module.select(inventory(latest, invalid, older))
        self.assertEqual(result["next_version"], 12)
        self.assertEqual(result["parent_id"], latest["id"])

    def test_coverage_is_separate_from_parent(self):
        baseline = record(2, "superseded")
        latest = record(8, parent=baseline["id"], coverage=False)
        result = module.select(inventory(latest, baseline))
        self.assertEqual(result["parent_id"], latest["id"])
        self.assertEqual(result["coverage_baseline_id"], baseline["id"])

    def test_incomplete_duplicates_and_pending_block(self):
        cases = [inventory(record(2), complete=False), inventory(record(8), record(8)),
                 inventory(record(8), record(9, "draft")), inventory(record(8), record(9))]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                module.select(case)

    def test_stale_pointer_and_missing_or_forked_lineage_block(self):
        cases = [inventory(record(2), record(8, "superseded")),
                 inventory(record(8, parent="missing")),
                 inventory(record(2, "superseded"), record(8))]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                module.select(case)

    def test_empty_series_and_mixed_scope(self):
        self.assertEqual(module.select(inventory())["next_version"], 1)
        other = record(2); other["series_id"] = "other-series"
        with self.assertRaises(ValueError):
            module.select(inventory(other))
