"""Graph-track tests: argmap nodes, crux queue, treeka assembler, audits."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_tool(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class GraphTests(unittest.TestCase):
    def test_range_parsing(self):
        m = load_tool("argmap_nodes")
        self.assertEqual(m.parse_range("8.1-8.17"), ("verse", (1, 17)))
        self.assertEqual(m.parse_range("1-9"), ("verse", (1, 9)))
        self.assertEqual(m.parse_range("3"), ("verse", (3, 3)))
        self.assertEqual(m.parse_range("stotra 1-4"), ("stotra", (1, 4)))
        self.assertIsNone(m.parse_range("eight"))
        self.assertEqual(m.parse_stotra_song("s01"), 1)
        self.assertIsNone(m.parse_stotra_song("tsa08-p03"))

    def test_nodes_join_rules(self):
        m = load_tool("argmap_nodes")
        with tempfile.TemporaryDirectory() as td:
            tw = Path(td)
            (tw / "w1").mkdir()
            (tw / "w1" / "passages.jsonl").write_text(
                '{"locator":"w1-p01","verses":"1-9"}\n'
                '{"locator":"w1-p02","verses":"stotra 1-4"}\n', encoding="utf-8")
            (tw / "w1" / "data").mkdir()
            (tw / "w1" / "data" / "w1.argmap.json").write_text(json.dumps([
                {"verse_id": "w1-v05", "song": "s", "verse": 5,
                 "question": "Q?", "premises": ["P"], "inference": "I",
                 "uncertainties": ["U?"], "sanskrit_sha": "x"},
                {"verse_id": "w1-stotra", "song": "s02", "verse": 99,
                 "question": "Q2?", "premises": [], "inference": None,
                 "uncertainties": [], "sanskrit_sha": "y"},
                {"verse_id": "gone-v01", "song": "gone", "verse": 999,
                 "question": "Q3?", "premises": ["P3"], "inference": None,
                 "uncertainties": [], "sanskrit_sha": "z"},
            ]), encoding="utf-8")
            out = Path(td) / "nodes.jsonl"
            sys.argv = ["argmap_nodes.py", "--tw", str(tw), "--out", str(out)]
            m.main()
            rows = [json.loads(l) for l in out.read_text().splitlines()]
            by_id = {r["verse_id"]: r for r in rows}
            self.assertEqual(by_id["w1-v05"]["locator"], "w1-p01")
            self.assertEqual(by_id["w1-stotra"]["locator"], "w1-p02")
            self.assertEqual(by_id["gone-v01"]["locator"], "UNKNOWN")

    def test_treeka_keys_and_gaps(self):
        t = load_tool("treeka")
        with tempfile.TemporaryDirectory() as td:
            tw, sm = Path(td) / "tw", Path(td) / "sm.json"
            (tw / "wa").mkdir(parents=True)
            (tw / "wa" / "passages.jsonl").write_text(
                '{"locator":"a-p01","verses":"1-9"}\n{"locator":"a-p02","verses":"10-18"}\n')
            (tw / "wb").mkdir()
            (tw / "wb" / "passages.jsonl").write_text('{"locator":"a-p01","verses":"1-5"}\n')
            sm.write_text(json.dumps({"works": {
                "wa": {"status": "CANDIDATE"}, "wb": {"status": "CANDIDATE"}}}))
            out = Path(td) / "treeka.json"
            sys.argv = ["treeka.py", "--tw", str(tw), "--sourcemap", str(sm),
                        "--out", str(out)]
            # treeka reads nodes/queue/evidence from the real formal-trika dir;
            # with fixture works the join yields unargued entries keyed work:loc
            t.main()
            doc = json.loads(out.read_text())
            self.assertIn("wa:a-p01", doc["works"])
            self.assertIn("wb:a-p01", doc["works"])
            self.assertNotIn("a-p01", doc["works"])

    def test_audits_run(self):
        s = load_tool("source_audit")
        sys.argv = ["source_audit.py"]
        self.assertEqual(s.main(), 0)
        d = load_tool("decision_check")
        sys.argv = ["decision_check.py"]
        self.assertEqual(d.main(), 0)


    def test_tensions_export_public_only(self):
        import subprocess
        import sys as _sys
        r = subprocess.run([_sys.executable, str(ROOT / "tools" / "tensions_export.py")],
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        import json as _json
        rows = [_json.loads(l) for l in
                (ROOT / "data" / "tensions-export.jsonl").read_text().splitlines() if l.strip()]
        self.assertTrue(rows)
        for c in rows:
            self.assertEqual(c["kind"], "lived-tension")
            self.assertIn("status", c)
            self.assertNotIn("body", c)  # VOICE RULE: no body text crosses


if __name__ == "__main__":
    unittest.main()
