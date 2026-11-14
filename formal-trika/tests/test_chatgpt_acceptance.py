#!/usr/bin/env python3
"""test_chatgpt_acceptance.py — the ChatGPT-side suite proves itself in CI.

Runs tools/chatgpt_acceptance_run.py (real HTTPS against the live public
surface, no box access): all T0–T15 steps must pass. Slow (~minutes of real
HTTP) by design — this is the outside-in proof the unit suite cannot give.
Same pattern as test_mcp_bridge.py.
"""
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / "tools" / "chatgpt_acceptance_run.py"


class TestChatGPTAcceptance(unittest.TestCase):
    def test_acceptance_suite_passes_live(self):
        r = subprocess.run([sys.executable, str(RUNNER)],
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(r.returncode, 0,
                         f"acceptance suite failed:\n{r.stdout}\n{r.stderr}")
        self.assertIn("16/16", r.stdout)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
