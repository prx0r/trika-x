"""Source bridge tests: passage membership is not witness authority."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / 'tools' / 'bridge_resolve.py'
spec = importlib.util.spec_from_file_location('bridge_resolve', BRIDGE)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = bridge.read_json(bridge.SNAPSHOT_PATH)
        self.mapping = bridge.read_json(bridge.MAP_PATH)
        self.evidence = bridge.read_json(bridge.EVIDENCE_PATH)
        self.inventory = bridge.inventory(self.snapshot, self.mapping, self.evidence)

    def test_exact_known_locator_not_prefix(self):
        row = bridge.resolve('chunk:tsa08-p03', self.snapshot, self.mapping, self.inventory)
        self.assertEqual(row['immutable_id'], 'pt:pid:ts:a08:7f9e4b3307f2')
        self.assertEqual(row['ledger']['status'], 'SNAPSHOT_ONLY')
        self.assertEqual(row['witness_status'], 'UNPINNED')
        for invalid in ('chunk:tsa08-p999', 'chunk:tsa08-p03-extra', 'other:tsa08-p03', 'chunk:vbt'):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                bridge.resolve(invalid, self.snapshot, self.mapping, self.inventory)

    def test_work_level_is_not_a_passage(self):
        self.assertEqual(bridge.resolve('vbt', self.snapshot, self.mapping, self.inventory)['kind'], 'work')

    def test_unknown_exit_is_nonzero(self):
        p = subprocess.run([sys.executable, str(BRIDGE), 'chunk:tsa08-p999'], text=True, capture_output=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('unknown passage', p.stderr)

    def test_bad_ledger_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            good = b'{"locator":"one"}\n'
            ledger = root / 'one' / 'passages.jsonl'
            ledger.parent.mkdir()
            ledger.write_bytes(good)
            snap = {'works': {'one': {'ledger': 'one/passages.jsonl', 'sha256': hashlib.sha256(good).hexdigest()}}}
            bridge.verify_ledgers(root, snap)
            ledger.write_bytes(good + b' ')
            with self.assertRaisesRegex(ValueError, 'differs'):
                bridge.verify_ledgers(root, snap)
            ledger.unlink()
            with self.assertRaisesRegex(ValueError, 'missing'):
                bridge.verify_ledgers(root, snap)

    def test_unverified_witness_cannot_be_promoted(self):
        mapping = copy.deepcopy(self.mapping)
        mapping['works']['tsa08']['witness'] = 'invented-siglum'
        with self.assertRaisesRegex(ValueError, 'UNPINNED'):
            bridge.inventory(self.snapshot, mapping, self.evidence)

    def test_candidates_are_advisory_never_pins(self):
        cands = bridge.read_json(bridge.CANDIDATES_PATH)
        self.assertTrue(cands.get('candidates'))
        for c in cands['candidates']:
            self.assertEqual(c.get('status') in ('CANDIDATE', 'CANDIDATE-EDITION'), True)
        # Even with candidates attached, resolution stays UNPINNED.
        row = bridge.resolve('chunk:tsa08-p03', self.snapshot, self.mapping,
                             self.inventory, candidates=cands)
        self.assertEqual(row['witness_status'], 'UNPINNED')
        self.assertIn('witness_candidates', row)
        self.assertTrue(all('source_url' in r or 'note' in r
                            for c in row['witness_candidates'] for r in c['records']))
        # And without the file, resolution still works (no promotion path).
        row2 = bridge.resolve('chunk:tsa08-p03', self.snapshot, self.mapping,
                              self.inventory, candidates={"candidates": []})
        self.assertEqual(row2['witness_status'], 'UNPINNED')
        self.assertNotIn('witness_candidates', row2)

    def test_stale_or_duplicate_snapshot_rejected(self):
        snap = copy.deepcopy(self.snapshot)
        snap['works']['tsa08']['passages'][0]['immutable_id'] = snap['works']['tsa08']['passages'][1]['immutable_id']
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            bridge.inventory(snap, self.mapping, self.evidence)
        ev = copy.deepcopy(self.evidence)
        ev['works']['tsa08']['chunks'].append('tsa08-p999')
        with self.assertRaisesRegex(ValueError, 'differs'):
            bridge.inventory(self.snapshot, self.mapping, ev)


if __name__ == '__main__':
    unittest.main()
