#!/usr/bin/env python3
"""test_gen_prakriya_slice.py — the Lean slice stays generated, pinned, honest.

Depends on the svread checkout (SVREAD env, default /root/svread) for the
pack; labelled skip when absent — the committed .lean + receipt must still be
internally consistent either way.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent      # formal-trika
TOOL = HERE / 'tools' / 'gen_prakriya_slice.py'
CONTROL = HERE / 'control'
LEAN = CONTROL / 'PrakriyaSlice.lean'
RECEIPT = CONTROL / 'PrakriyaSlice.receipt.json'
PACK = Path(os.environ.get('SVREAD', '/root/svread')) / 'data/grammar/wheel-pack.json'


def _pack_present() -> bool:
    # unreadable/absent sibling checkout must skip, never raise at import
    # (the same PermissionError class svread hit on the runner)
    try:
        return PACK.is_file()
    except OSError:
        return False


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *args],
                          capture_output=True, text=True, timeout=300)


@unittest.skipUnless(_pack_present(), 'svread pack not present (SVREAD)')
class TestPrakriyaSlice(unittest.TestCase):
    # -- pack-dependent (skip labelled when the svread checkout is absent) --
    @unittest.skipUnless(_pack_present(), 'svread pack not present (SVREAD)')
    def test_generator_is_deterministic(self):
        r = run('--check')
        self.assertEqual(r.returncode, 0, r.stderr)

    @unittest.skipUnless(_pack_present(), 'svread pack not present (SVREAD)')
    def test_receipt_pins_the_current_pack(self):
        rec = json.loads(RECEIPT.read_text(encoding='utf-8'))
        self.assertEqual(rec['pack_sha256'],
                         __import__('hashlib').sha256(PACK.read_bytes()).hexdigest(),
                         'receipt pins the exact pack it checked')

    # -- committed bytes only (always run, incl. CI) --
    def test_receipt_is_passing_scoped_and_pins_the_file(self):
        self.assertTrue(RECEIPT.is_file(), 'receipt committed')
        self.assertTrue(LEAN.is_file(), 'PrakriyaSlice.lean committed')
        rec = json.loads(RECEIPT.read_text(encoding='utf-8'))
        self.assertEqual(rec['format'], 'svatantrya.lean-receipt/1')
        self.assertEqual(rec['exit_code'], 0, 'lean must have passed')
        self.assertEqual(rec['file_sha256'],
                         __import__('hashlib').sha256(LEAN.read_bytes()).hexdigest(),
                         'receipt pins the exact lean file')
        self.assertIn('NOT a derivation', rec['scope'])
        self.assertIn('inventory', rec['scope'])

    def test_lean_file_carries_scope_and_mutants(self):
        src = LEAN.read_text(encoding='utf-8')
        self.assertIn('SCOPE:', src)
        self.assertIn('NOT a derivation', src)
        for m in ('mutant_bad_sutra_rejected', 'mutant_empty_after_rejected',
                  'mutant_no_steps_rejected', 'mutant_empty_surface_rejected'):
            self.assertIn(m, src, f'mutant theorem {m} present')
        self.assertIn('GENERATED', src, 'generated file says so')


if __name__ == '__main__':
    raise SystemExit(unittest.main())
