"""Coverage reports must not confuse missing data or work refs with passages."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
sys.path.insert(0, str(TOOLS))


def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


treeka = load('treeka_formal')
evidence = load('evidence_check')


class ReportTests(unittest.TestCase):
    def test_chapter_ranges_do_not_match_unqualified_or_wrong_chapter(self):
        rng = treeka.verse_range('1.1-1.10')
        self.assertIsNone(treeka.in_range(2, rng))
        self.assertTrue(treeka.in_range(2, rng, single_chapter=1))
        self.assertFalse(treeka.in_range('2.2', rng))
        self.assertIsNone(treeka.in_range(1.10, rng))
        self.assertIsNone(treeka.verse_range('20-3'))

    def test_missing_checkout_is_not_empty_success(self):
        for tool, option in (('treeka_formal.py', '--tw'), ('evidence_check.py', '--root')):
            with self.subTest(tool=tool), tempfile.TemporaryDirectory() as temp:
                run = subprocess.run([sys.executable, str(TOOLS / tool), option, temp],
                                     text=True, capture_output=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertNotIn('0/0', run.stdout)
                self.assertIn('missing', run.stderr)

    def test_missing_argmap_and_unmatched_l2_are_unknown(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            self.assertIsNone(treeka.argmap_verses(path))
            (path / 'L2.md').write_text('text without a locator', encoding='utf-8')
            self.assertIsNone(treeka.has_l2(path, 'example-p01'))

    def test_corrupt_argmap_is_not_silently_counted_as_absent(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'data').mkdir()
            (path / 'data' / 'example.argmap.json').write_text('{broken', encoding='utf-8')
            with self.assertRaises(json.JSONDecodeError):
                treeka.argmap_verses(path)

    def test_unrecognized_argmap_layout_is_unknown(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'data').mkdir()
            (path / 'data' / 'example.argmap.json').write_text('{"unexpected": []}', encoding='utf-8')
            self.assertIsNone(treeka.argmap_verses(path))

    def test_evidence_keys_include_file_not_only_theorem_name(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'A.lean').write_text('theorem same : True := by trivial\n')
            (path / 'B.lean').write_text('theorem same : True := by trivial\n')
            original_root, original_sources = evidence.HERE, evidence.SOURCES
            try:
                evidence.HERE, evidence.SOURCES = path, ['A.lean', 'B.lean']
                self.assertEqual(evidence.theorems(), {'A.lean :: same', 'B.lean :: same'})
            finally:
                evidence.HERE, evidence.SOURCES = original_root, original_sources


if __name__ == '__main__':
    unittest.main()
