#!/usr/bin/env python3
"""test_northstar_fixes.py — N6 and N14 from NORTHSTAR-2026-11-17.

N6: formal__evidence accepts a bare theorem name.
N14: formal__gaps counts only passage chunks, so covered+gap_count==total.
"""
import importlib.util
import unittest
from pathlib import Path

GW = Path(__file__).resolve().parent.parent / "tools" / "federation_gateway.py"


def _load():
    spec = importlib.util.spec_from_file_location("federation_gateway", GW)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class FormalEvidenceBareName(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gw = _load()

    def test_bare_name_resolves(self):
        out = self.gw.formal_evidence({"theorem": "key_five_kancukas"})
        self.assertTrue(out["found"], out)
        self.assertEqual(out["matched_by"], "bare-name")
        self.assertTrue(out["theorem"].endswith(":: key_five_kancukas"))

    def test_full_name_still_resolves(self):
        out = self.gw.formal_evidence(
            {"theorem": "AnswerKey.lean :: key_five_kancukas"})
        self.assertTrue(out["found"], out)
        self.assertNotIn("matched_by", out)

    def test_unknown_fails_closed(self):
        out = self.gw.formal_evidence({"theorem": "no_such_theorem_xyz"})
        self.assertFalse(out["found"], out)
        self.assertIn("note", out)


class FormalGapsArithmetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gw = _load()

    def test_covered_plus_gaps_equals_total(self):
        out = self.gw.formal_gaps({})
        self.assertEqual(out["covered"] + out["gap_count"], out["total"], out)
        self.assertEqual(out["coverage"],
                         f"{out['covered']}/{out['total']}")
        self.assertEqual(out["returned"], len(out["gaps"]))

    def test_no_work_level_ref_counted_as_passage(self):
        # 'vbt' is a work-level reference, not a passage locator.
        out = self.gw.formal_gaps({})
        self.assertNotIn("vbt", out["gaps"])
        self.assertEqual(out["covered"], 16, out["coverage"])

    def test_work_filter_consistent(self):
        out = self.gw.formal_gaps({"work": "vbt"})
        self.assertEqual(out["returned"], len(out["gaps"]))
        self.assertTrue(all(g.startswith("vbt") for g in out["gaps"]))


if __name__ == "__main__":
    unittest.main()
