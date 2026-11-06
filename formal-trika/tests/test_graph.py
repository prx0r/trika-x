"""Graph-track tests: argmap nodes, crux queue, treeka assembler, audits."""
import importlib.util
import hashlib
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
    def test_empty_source_maps_fail_closed(self):
        b = load_tool('build_source_map')
        t = load_tool('treeka')
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sys.argv = ['build_source_map.py', '--tw', str(root), '--out', str(root / 'out.json')]
            with self.assertRaises(SystemExit):
                b.main()
            sm = root / 'empty.json'
            sm.write_text('{"works":{}}')
            sys.argv = ['treeka.py', '--tw', str(root), '--sourcemap', str(sm), '--out', str(root / 'out.json')]
            with self.assertRaisesRegex(ValueError, 'no works'):
                t.main()

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
        self.assertIsNone(m.parse_span('20-3'))
        self.assertEqual(m.parse_span('2.1-2.10'), ('verse', 2, 1, 2, 10))
        self.assertIsNone(m.verse_coordinate({'verse': 1.10}))
        self.assertEqual(m.parse_stotra_song("s01"), 1)
        self.assertIsNone(m.parse_stotra_song("tsa08-p03"))

    def test_locator_resolution_refuses_wrong_work_and_missing_chapter(self):
        m = load_tool('argmap_nodes')
        spans = {'a': {'a-p01': m.parse_span('1.1-1.10'),
                       'a-p02': m.parse_span('2.1-2.10')},
                 'b': {'b-p01': m.parse_span('1-10'),
                       'a-p01': m.parse_span('1-10')}}
        locsets = {work: set(items) for work, items in spans.items()}
        owners = {'a-p01': {'a', 'b'}, 'a-p02': {'a'}, 'b-p01': {'b'}}
        self.assertEqual(m.resolve_unit('a', {'verse': 2}, spans, locsets, owners)[0], 'UNKNOWN')
        self.assertEqual(m.resolve_unit('a', {'verse': '2.2'}, spans, locsets, owners)[0], 'a-p02')
        self.assertEqual(m.resolve_unit('a', {'song': 'a-p01', 'verse': 2}, spans, locsets, owners)[0], 'a-p01')
        self.assertEqual(m.resolve_unit('a', {'song': 'a-p01', 'verse': 15}, spans, locsets, owners)[1], 'LOCATOR_RANGE_CONFLICT')
        foreign = m.resolve_unit('a', {'song': 'b-p01', 'verse': 2}, spans, locsets, owners)
        self.assertEqual(foreign[0:2], ('UNKNOWN', 'FOREIGN_LOCATOR'))
        self.assertEqual(foreign[3], ['b'])

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
            self.assertEqual(by_id['w1-v05']['source_checkout_state'], 'UNVERIFIED')
            self.assertEqual(len(by_id['w1-v05']['source_file_sha256']), 64)
            self.assertEqual(len(by_id['w1-v05']['ledger_sha256']), 64)

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
                w: {"status": "CANDIDATE", "ledger_sha256": hashlib.sha256(
                    (tw / w / 'passages.jsonl').read_bytes()).hexdigest()}
                for w in ('wa', 'wb')}}))
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

    def test_treeka_rejects_stale_argmap_and_ledger_bytes(self):
        t = load_tool('treeka')
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            work = root / 'w'
            (work / 'data').mkdir(parents=True)
            ledger = work / 'passages.jsonl'
            ledger.write_text('{"locator":"w-p01"}\n')
            source = work / 'data/one.argmap.json'
            source.write_text('[]')
            sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
            smap = {'w': {'ledger_sha256': sha(ledger)}}
            node = {'work': 'w', 'locator': 'w-p01', 'source_file': 'w/data/one.argmap.json',
                    'source_file_sha256': sha(source), 'ledger_sha256': sha(ledger)}
            t.verify_inputs(root, smap, [node])
            source.write_text('[{}]')
            with self.assertRaisesRegex(ValueError, 'stale argmap'):
                t.verify_inputs(root, smap, [node])
            source.write_text('[]')
            ledger.write_text('{"locator":"w-p02"}\n')
            with self.assertRaisesRegex(ValueError, 'ledger hash mismatch'):
                t.verify_inputs(root, smap, [node])

    def test_treeka_rejects_queue_entries_without_matching_node(self):
        t = load_tool('treeka')
        node = {'work': 'w', 'locator': 'w-p01', 'verse_id': 'v1',
                'source_file': 'w/data/a.json', 'source_file_sha256': 'x',
                'ledger_sha256': 'y', 'uncertainties': ['open question']}
        item = {k: node[k] for k in ('work', 'locator', 'verse_id', 'source_file',
                                    'source_file_sha256', 'ledger_sha256')}
        item.update({'kind': 'argmap-uncertainty', 'text': 'open question'})
        t.verify_queue([node], [item], {'w': {}})
        item['text'] = 'changed question'
        with self.assertRaisesRegex(ValueError, 'stale crux queue'):
            t.verify_queue([node], [item], {'w': {}})

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


    def test_matrika_study_cards(self):
        import subprocess
        import sys as _sys
        r = subprocess.run([_sys.executable, str(ROOT / "tools" / "matrika_study.py")],
                           text=True, capture_output=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        import json as _json
        d = _json.loads((ROOT / "data" / "matrika-study.json").read_text())
        self.assertEqual(len(d["cards"]), 50)
        for c in d["cards"]:
            for k in ("phoneme", "dev", "matrika_locus", "malini_locus",
                      "clip", "class", "study", "trika_link", "needs_scholar"):
                self.assertIn(k, c)
            self.assertIsNone(c["trika_link"])  # doctrine never inferred
            self.assertTrue(c["needs_scholar"])


if __name__ == "__main__":
    unittest.main()
