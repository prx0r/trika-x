#!/usr/bin/env python3
"""test_mcp_bridge.py — the HTTP bridge proves itself, not asserts itself.

Runs tools/mcp_bridge.py --selftest in a subprocess: real gateway, real HTTP,
real box DB. Exit 0 means ChatGPT's future front door answers, filters to the
read sheaf, refuses writes honestly, enforces limits, and ends sessions.
Skipped only when the box cannot serve (no gateway deps); never faked.
"""
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent.parent / "tools" / "mcp_bridge.py"


class TestMcpBridge(unittest.TestCase):
    def test_bridge_selftest_passes(self):
        r = subprocess.run([sys.executable, str(BRIDGE), "--selftest"],
                           capture_output=True, text=True, timeout=600)
        self.assertEqual(r.returncode, 0,
                         f"bridge selftest failed:\n{r.stdout}\n{r.stderr}")
        self.assertIn("SELFTEST OK", r.stdout)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
