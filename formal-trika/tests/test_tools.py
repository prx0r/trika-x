"""Regression tests for the evidence boundary; fake Lean output is synthetic."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MUST_FAIL = ROOT / "tools" / "must_fail.py"
EMITTER = ROOT / "tools" / "emit_keys.py"
AXIOM_AUDIT = ROOT / "tools" / "axiom_audit.py"
MUTATE_SWEEP = ROOT / "tools" / "mutate_sweep.py"


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.positive = self.dir / "Positive.lean"
        self.mutant = self.dir / "Broken.lean"
        self.positive.write_text("theorem example : 1 = 1 := by decide\n")
        self.mutant.write_text("theorem example : 1 = 1 := by decide\n")
        self.lean = self.dir / "lean"
        self.lean.write_text('''#!/usr/bin/env python3
import os, sys
mode = os.environ.get("FAKE_CASE", "false")
if "--version" in sys.argv:
    print("Lean (version 4.0.0, fake)" if mode == "version" else "Lean (version 4.34.1, fake)")
    sys.exit(0)
if mode == "accepted":
    sys.exit(0)
line = 2 if mode == "wrongline" else 1
reason = "unexpected syntax" if mode == "syntax" else "Tactic `decide` proved that the proposition\\n  1 = 1\\nis false"
print(f"{sys.argv[-1]}:{line}:1: error: {reason}")
if mode == "multiple":
    print(f"{sys.argv[-1]}:1:1: error: another error")
sys.exit(1)
''')
        self.lean.chmod(0o755)

    def run_helper(self, mode="false", lean=None):
        env = os.environ.copy()
        env["FAKE_CASE"] = mode
        return subprocess.run([sys.executable, str(MUST_FAIL),
                               "--lean", str(lean or self.lean),
                               "--positive", str(self.positive),
                               "--mutant", str(self.mutant),
                               "--theorem", "example"],
                              text=True, capture_output=True, env=env)

    def test_only_expected_false_goal_passes(self):
        self.assertEqual(self.run_helper().returncode, 0)
        for case in ("accepted", "version", "syntax", "multiple", "wrongline"):
            with self.subTest(case=case):
                result = self.run_helper(case)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertNotIn("PASS", result.stdout)

    def test_missing_compiler_fails(self):
        result = self.run_helper(lean=self.dir / "missing")
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("PASS", result.stdout)

    def test_changed_theorem_cannot_pass(self):
        self.mutant.write_text("theorem example : 1 = 2 := by decide\n")
        self.assertNotEqual(self.run_helper().returncode, 0)

    def test_inventory_never_claims_to_have_checked_proofs(self):
        result = subprocess.run([sys.executable, str(EMITTER)], check=True,
                                text=True, capture_output=True)
        inventory = json.loads(result.stdout)
        self.assertEqual(inventory["verification"], "NOT_RUN")
        self.assertFalse(inventory["integration_ready"])
        self.assertEqual(inventory["source_pins"], "UNRESOLVED")
        self.assertTrue(inventory["theorems"])
        self.assertTrue(all(t["status"] == "NOT_CHECKED" for t in inventory["theorems"]))

    def test_axiom_audit_clean_and_fail_closed(self):
        result = subprocess.run([sys.executable, str(AXIOM_AUDIT), "--check"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CLEAN", result.stdout)

    def test_mutate_sweep_fails_closed_without_instrument(self):
        env = os.environ.copy()
        env["MUTATE_LEAN"] = str(self.dir / "no-such-Mutate.lean")
        result = subprocess.run([sys.executable, str(MUTATE_SWEEP)],
                                text=True, capture_output=True, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("sweep complete", result.stdout)

    def test_kappa_raw_and_chance_corrected(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "kappa", str(ROOT / "tools" / "kappa.py"))
        kappa = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kappa)
        a = ["anava"] * 6 + ["sakta"] * 6
        b = ["anava"] * 6 + ["sakta"] * 6
        r = kappa.cohen_kappa(a, b)
        self.assertEqual(r["raw"], 1.0)
        self.assertEqual(r["kappa"], 1.0)
        b2 = ["sakta"] * 6 + ["anava"] * 6
        r2 = kappa.cohen_kappa(a, b2)
        self.assertEqual(r2["raw"], 0.0)
        with self.assertRaises(ValueError):
            kappa.cohen_kappa(a, b + ["anava"])

    def test_cooccurrence_does_not_promote_a_pilot_to_doctrine(self):
        tool = ROOT / 'tools' / 'tc1_cooccurrence.py'
        empty = subprocess.run([sys.executable, str(tool), str(self.dir)],
                               text=True, capture_output=True)
        self.assertNotEqual(empty.returncode, 0)
        (self.dir / 'day-1.jsonl').write_text(json.dumps({
            'day': 1, 'arc': 'synthetic', 'heads': ['lobha', 'thina'],
            'felt': []}) + '\n')
        result = subprocess.run([sys.executable, str(tool), str(self.dir)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Exploratory only', result.stdout)
        self.assertNotIn('HOLDS', result.stdout)

    def test_external_pushback_requires_explicit_text_opt_in(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'tools' / 'pushback.py'),
             '--draft', str(self.dir / 'missing'), '--refs', str(self.dir / 'missing'),
             '--model', 'cf:example', '--out', str(self.dir / 'out')],
            text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--allow-external-text', result.stderr)

    @unittest.skipUnless((Path(os.environ.get('SVREAD_CHECKOUT', ROOT.parent.parent / 'svread')) /
                          'mcp/claims.py').is_file(),
                         'set SVREAD_CHECKOUT to exercise the cross-repo claims integration')
    def test_pushback_mock_never_edits_and_shields(self):
        import json
        draft = self.dir / "draft.md"
        draft.write_text('Claim one [w:t].\n\nOwner says "exact words" [w:t].\n')
        refs = self.dir / "refs.json"
        refs.write_text(json.dumps([{"kind": "chunk", "work": "w", "target": "t"}]))
        out = self.dir / "report.md"
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pushback.py"),
             "--draft", str(draft), "--refs", str(refs),
             "--model", "mock", "--out", str(out)],
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = out.read_text()
        self.assertIn("NEVER edits", report)
        self.assertIn("OBJECTION 1", report)
        # draft untouched
        self.assertNotIn("OBJECTION", draft.read_text())
        # verbatim shielding
        out2 = self.dir / "report2.md"
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pushback.py"),
             "--draft", str(draft), "--refs", str(refs),
             "--model", "mock", "--verbatim", "Owner says",
             "--out", str(out2)],
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("VERBATIM-SHIELDED", out2.read_text())


if __name__ == "__main__":
    unittest.main()
