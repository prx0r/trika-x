"""Practice-track tests: eligibility gate + C1 unit invariants."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_tool(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class PracticeTests(unittest.TestCase):
    def test_eligibility_tiers(self):
        e = load_tool("eligibility")
        self.assertEqual(e.classify("sit and watch the breath", "anava", "")["eligibility"], "doable")
        d = e.classify("stop breath, feel the void", "", "")
        self.assertEqual(d["eligibility"], "doable")
        self.assertTrue(any("retention" in c for c in d["cautions"]))
        r = e.classify("install the deity with seed mantra from guru", "", "")
        self.assertEqual(r["eligibility"], "requires-diksha")
        self.assertIn("withheld", r["cautions"][0])
        s = e.classify("consider the nature of consciousness", "", "")
        self.assertEqual(s["eligibility"], "study")
        # fail-closed: unknown never doable
        u = e.classify("xqzzy plugh", "mystery", "???")
        self.assertEqual(u["eligibility"], "study")

    def test_path_assembly_no_diy_diksha(self):
        import hashlib
        units = ROOT / "data" / "unit-vbt-d001.json"
        diksha = {"unit_id": "vbt-dX", "eligibility": {"eligibility": "requires-diksha"},
                  "safety": ["conferred"], "source_refs": []}
        dp = Path(self._tmp() if hasattr(self, "_tmp") else "/tmp") / "diksha.json"
        dp.write_text(json.dumps(diksha))
        out = Path("/tmp/path-test.json")
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "path_assemble.py"),
                            "--units", str(units), str(dp), "--spine", "ts-six",
                            "--slug", "test", "--out", str(out)],
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        p = json.loads(out.read_text())
        self.assertEqual(p["path_id"], "path:trika/test")
        by_id = {it["unit_id"]: it for it in p["items"]}
        self.assertEqual(by_id["vbt-dX"]["render"]["mode"], "STUDY")
        self.assertNotIn("unit", by_id["vbt-dX"]["render"])
        body = {k: v for k, v in p.items() if k != "path_sha256"}
        self.assertEqual(p["path_sha256"], hashlib.sha256(
            json.dumps(body, sort_keys=True).encode()).hexdigest())

    def test_day_gate_counts_posting_days(self):
        log = Path("/tmp/day-test.jsonl")
        if log.is_file():
            log.unlink()
        def run(*args):
            return subprocess.run([sys.executable, str(ROOT / "tools" / "day_gate.py"),
                                   "--log", str(log), *args],
                                  text=True, capture_output=True)
        self.assertEqual(run("post", "--date", "2026-11-06", "--unit", "vbt-d001").returncode, 0)
        self.assertEqual(run("post", "--date", "2026-11-06", "--unit", "vbt-d002").returncode, 0)
        st = json.loads(run("status").stdout)
        self.assertEqual(st["day_N"], 1)  # same day re-post keeps N
        self.assertEqual(st["posts"], 2)
        run("post", "--date", "2026-11-08", "--unit", "vbt-d003")
        st = json.loads(run("status").stdout)
        self.assertEqual(st["day_N"], 2)  # empty 11-07 never advances
        log.unlink()

    def test_c1_unit_invariants(self):
        u = json.loads((ROOT / "data" / "unit-vbt-d001.json").read_text(encoding="utf-8"))
        self.assertEqual(u["unit_id"], "vbt-d001")
        self.assertEqual(u["status"], "review")
        self.assertTrue(u["source_refs"])
        self.assertEqual(u["source_refs"][0]["locator"], "vbt-p03")
        # model never writes timings
        for s in u["steps"]:
            self.assertIsNone(s["seconds"])
        # technique marked R-gloss, never root text
        self.assertIn("R-gloss", u["technique_provenance"])
        # sha matches content
        body = {k: v for k, v in u.items() if k != "unit_sha256"}
        self.assertEqual(u["unit_sha256"], hashlib.sha256(
            json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest())
        # safety present
        self.assertTrue(u["safety"])
        # renderer entry point works for another mapped unit
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "syllabus_unit.py"),
                            "--dharana", "2", "--out", "/tmp/unit-vbt-d002.json"],
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


    def test_bodymap_one_truth(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "bodymap_check.py")],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ONE truth", result.stdout)


if __name__ == "__main__":
    unittest.main()

    def test_unit_to_syllabus_plug(self):
        import subprocess
        import sys as _sys
        out = Path("/tmp/syl-plug-test.json")
        r = subprocess.run([_sys.executable, str(ROOT / "tools" / "unit_to_score.py"),
                            "--unit", str(ROOT / "data" / "unit-vbt-d001.json"),
                            "--out", str(out)], text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        d = json.loads(out.read_text())
        self.assertEqual(d["kind"], "syllabus/1")
        self.assertEqual(d["from_unit"], "vbt-d001")
        self.assertTrue(d["source_refs"])
        # compiler-compat keys present; no timings written by model
        for s in d["steps"]:
            for k in ("id", "kind", "cue", "dur", "region"):
                self.assertIn(k, s)
            self.assertIsNone(s["dur"])
        # diksha units emit no steps
        du = {"unit_id": "vbt-dX", "unit_sha256": "x",
              "eligibility": {"eligibility": "requires-diksha"},
              "safety": ["conferred"], "source_refs": [], "steps": [],
              "technique_R": "install deity with seed mantra"}
        dp = Path("/tmp/du-plug-test.json")
        dp.write_text(json.dumps(du))
        out2 = Path("/tmp/syl-plug-test2.json")
        r = subprocess.run([_sys.executable, str(ROOT / "tools" / "unit_to_score.py"),
                            "--unit", str(dp), "--out", str(out2)],
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0)
        d2 = json.loads(out2.read_text())
        self.assertEqual(d2["steps"], [])
        self.assertEqual(d2["gate"]["mode"], "STUDY")
