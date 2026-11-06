"""Regression tests for source, theorem and review authorization boundaries."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReviewBoundaries(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.project = self.root / 'trika' / 'formal-trika'
        self.tools = self.project / 'tools'
        self.tools.mkdir(parents=True)
        (self.project / 'data').mkdir()
        (self.project / 'data/research-tracks.json').write_text('{"tracks": []}')
        for name in ('review_status.py', 'roboscholar.py', 'essay_compile.py'):
            shutil.copy(ROOT / 'tools' / name, self.tools / name)
        self.tw = self.root / 'translation-work'
        work = self.tw / 'demo-work'
        (work / 'data').mkdir(parents=True)
        argmap = work / 'data/argmap.json'
        argmap.write_text('{"synthetic":true}\n')
        ledger = work / 'passages.jsonl'
        ledger.write_text('{"locator":"demo-p01","verses":"1"}\n')
        sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        node = {'work': 'demo-work', 'locator': 'demo-p01', 'locator_status': 'NUMBER_RANGE',
                'source_file': 'demo-work/data/argmap.json', 'source_file_sha256': sha(argmap),
                'ledger_sha256': sha(ledger), 'verse_id': 'demo-v1', 'premises': ['candidate premise']}
        (self.project / 'data/argmap-nodes.jsonl').write_text(json.dumps(node) + '\n')
        evidence = {'works': {'demo': {'ledger': 'translation-work/demo-work/passages.jsonl',
                                       'chunks': ['demo-p01']}},
                    'entries': {'Demo.lean :: theorem': {'chunks': [{'locator': 'demo-p01'}]}}}
        (self.project / 'EVIDENCE.json').write_text(json.dumps(evidence))
        self.owner = self.root / 'owner.md'
        self.owner.write_text('# Synthetic\n> selected voice\n')
        mcp = self.root / 'svread/mcp'
        mcp.mkdir(parents=True)
        (mcp / 'audit.py').write_text('def audit(*args, **kwargs): return {"checks": []}\n')
        (mcp / 'claims.py').write_text('def link(*args, **kwargs): return {"claims": []}\n')
        self.env = {**os.environ, 'TRANSLATION_WORK': str(self.tw),
                    'SVREAD_CHECKOUT': str(self.root / 'svread')}

    def run_compiler(self, chunk='demo-p01', theorem='Demo.lean :: theorem'):
        return subprocess.run([sys.executable, str(self.tools / 'essay_compile.py'),
            '--owner', str(self.owner), '--work', 'demo-work', '--chunk', chunk,
            '--verses', 'demo-v1', '--theorems', theorem, '--slug', 'synthetic'],
            text=True, capture_output=True, env=self.env)

    def test_compiler_checks_inputs_without_claiming_proof(self):
        r = self.run_compiler()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        draft = next((self.project / 'swarm').glob('*.md')).read_text()
        self.assertIn('proof and textual entailment not checked', draft)
        self.assertNotIn('decide-verified', draft)
        graph = json.loads((self.project / 'data/expansion-graph.json').read_text())
        formal = next(n for n in graph['nodes'] if n['id'].startswith('theorem:'))
        self.assertEqual(formal['tier'], 'UNVERIFIED')

    def test_compiler_rejects_wrong_chunk_unknown_theorem_and_stale_bytes(self):
        self.assertNotEqual(self.run_compiler(chunk='demo-p02').returncode, 0)
        self.assertNotEqual(self.run_compiler(theorem='Invented.lean :: theorem').returncode, 0)
        (self.tw / 'demo-work/data/argmap.json').write_text('{"changed":true}\n')
        self.assertNotEqual(self.run_compiler().returncode, 0)
        self.assertFalse((self.project / 'swarm').exists())

    def test_review_status_does_not_fill_missing_rows_in_check_mode(self):
        control = self.project / 'control'
        control.mkdir()
        (self.project / 'recognition').mkdir()
        (control / 'Demo.lean').write_text('theorem example : True := by trivial\n')
        status = self.project / 'data/review-status.json'
        raw = json.dumps({'format': 'trika-review-status/1', 'rows': {}})
        status.write_text(raw)
        cmd = [sys.executable, str(self.tools / 'review_status.py')]
        check = subprocess.run(cmd + ['--check'], text=True, capture_output=True)
        self.assertNotEqual(check.returncode, 0)
        self.assertEqual(status.read_text(), raw)
        promotion = subprocess.run(cmd + ['--promote', 'Demo.lean :: example',
            '--reviewer', 'invented', '--reason', 'not authenticated'], capture_output=True)
        self.assertNotEqual(promotion.returncode, 0)
        self.assertEqual(status.read_text(), raw)
        status.write_text(json.dumps({'format': 'trika-review-status/1', 'rows': {
            'Demo.lean :: example': {'tier': 'Core', 'reviewer': 'invented'}}}))
        self.assertNotEqual(subprocess.run(cmd + ['--check'], capture_output=True).returncode, 0)


if __name__ == '__main__':
    unittest.main()
