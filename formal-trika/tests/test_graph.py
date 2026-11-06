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
    def test_only_explicit_theorem_references_are_counted(self):
        t = load_tool('treeka')
        evidence = {
            'works': {'a': {'ledger': 'translation-work/wa/passages.jsonl',
                            'chunks': ['a-p01', 'a-p02']}},
            'entries': {'Example.lean :: result': {'chunks': [{'locator': 'a-p01'},
                                                                {'locator': 'vbt'}]}}
        }
        refs = t.formal_references(evidence)
        self.assertEqual(refs, {('wa', 'a-p01'): ['Example.lean :: result']})
        self.assertNotIn(('wa', 'a-p02'), refs)
        evidence['works']['b'] = {'ledger': 'translation-work/wb/passages.jsonl',
                                  'chunks': ['a-p01']}
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            t.formal_references(evidence)

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
            essays = tw / 'wb' / 'scholar' / 'essays'
            essays.mkdir(parents=True)
            (essays / 'example.json').write_text(json.dumps({'target': 'a-p01'}))
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
            self.assertEqual(doc['format'], 'treeka-research-index/2')
            self.assertIn('a-p01', doc['ambiguous_locators'])
            self.assertIsNone(doc['works']['wa:a-p01']['formalized'])
            self.assertEqual(doc['works']['wa:a-p01']['essays'], [])
            self.assertEqual(doc['works']['wb:a-p01']['essays'], ['example.json'])

    def test_audits_run(self):
        s = load_tool("source_audit")
        d = load_tool("decision_check")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for module in (s, d):
                sys.argv = ['audit.py', '--tw', str(root)]
                self.assertEqual(module.main(), 1)
            work = root / 'w'
            work.mkdir()
            (work / 'passages.jsonl').write_text('{"locator":"w-p01"}\n')
            (work / 'SOURCE.txt').write_text('candidate')
            for module in (s, d):
                sys.argv = ['audit.py', '--tw', str(root)]
                self.assertEqual(module.main(), 0)
            scholar = work / 'scholar'
            scholar.mkdir()
            (scholar / 'decisions.jsonl').write_text('{malformed\n')
            sys.argv = ['decision_check.py', '--tw', str(root)]
            self.assertEqual(d.main(), 1)


if __name__ == "__main__":
    unittest.main()
