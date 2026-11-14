#!/usr/bin/env python3
"""test_chatgpt_acceptance.py — the ChatGPT-side suites prove themselves in CI.

Runs tools/chatgpt_acceptance_run.py (real HTTPS against the live public
surface, no box access). Raw suite: all T0–T15 steps must pass. Connected
suite: every step skips with a reason on a box (no connected-tool
environment); the skip path itself must be clean. Slow (~minutes of real
HTTP) by design — this is the outside-in proof the unit suite cannot give.
Same pattern as test_mcp_bridge.py.
"""
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / "tools" / "chatgpt_acceptance_run.py"
CONNECTED = HERE / "chatgpt_connected_acceptance.json"


class TestChatGPTAcceptance(unittest.TestCase):
    def test_acceptance_suite_passes_live(self):
        r = subprocess.run([sys.executable, str(RUNNER)],
                           capture_output=True, text=True, timeout=900)
        self.assertEqual(r.returncode, 0,
                         f"acceptance suite failed:\n{r.stdout}\n{r.stderr}")
        self.assertIn("16/16", r.stdout)

    def test_connected_suite_skips_cleanly_without_chatgpt(self):
        r = subprocess.run([sys.executable, str(RUNNER), "--suite", str(CONNECTED)],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0,
                         f"connected suite must skip, never fail:\n{r.stdout}\n{r.stderr}")
        self.assertIn("5 skipped", r.stdout)
        self.assertNotIn("FAIL", r.stdout)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
