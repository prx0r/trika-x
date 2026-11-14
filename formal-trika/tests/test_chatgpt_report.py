#!/usr/bin/env python3
"""test_chatgpt_report.py — the report checker is itself checked.

A good report (all 16 steps, concrete observations, tally adds to 16, verdict
consistent) must pass. Reports with missing steps, tally mismatch, vibe-words
instead of observations, or verdict/row contradictions must fail. Pure logic,
no network: fast and deterministic.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE.parent / "tools" / "chatgpt_report_check.py"

STEPS = ["T0-handshake", "T1-discovery", "T2-identity-known",
         "T3-identity-unknown", "T4-evidence", "T5-formal-trace",
         "T6-gaps-honesty", "T7-unknown-tool", "T8-sitemap", "T9-llms",
         "T10-claim-page", "T11-formal-registry", "T12-second-host",
         "T13-robots", "T14-sitemap-claims", "T15-llms-names-verification"]


def good_report():
    return {
        "format": "svatantrya.chatgpt-acceptance-report/1",
        "date": "2026-11-14",
        "agent": "test-harness",
        "connector": "native MCP",
        "auth": "none",
        "suite": {"commit": "test", "branch": "main"},
        "endpoints": {"mcp": "https://mcp.svatantrya.net/mcp",
                      "formal": "https://formal.svatantrya.net/mcp",
                      "site": "https://svatantrya.net"},
        "results": [{"id": s, "verdict": "PASS",
                     "observed": "2025-06-18" if s == "T0-handshake" else "51 tools incl formal__trace"}
                    for s in STEPS],
        "tally": {"pass": 16, "fail": 0, "skip": 0},
        "anomalies": [],
        "verdict": "GREEN",
    }


def run_checker(rep):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(rep, f)
        path = f.name
    r = subprocess.run([sys.executable, str(CHECKER), path],
                       capture_output=True, text=True, timeout=60)
    return r


class TestChatGPTReport(unittest.TestCase):
    def test_good_report_passes(self):
        r = run_checker(good_report())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("REPORT OK", r.stdout)

    def test_missing_step_fails(self):
        rep = good_report()
        rep["results"] = rep["results"][:-1]
        rep["tally"] = {"pass": 15, "fail": 0, "skip": 0}
        self.assertNotEqual(run_checker(rep).returncode, 0)

    def test_tally_mismatch_fails(self):
        rep = good_report()
        rep["tally"] = {"pass": 15, "fail": 1, "skip": 0}
        self.assertNotEqual(run_checker(rep).returncode, 0)

    def test_vibe_word_fails(self):
        rep = good_report()
        rep["results"][0]["observed"] = "looks good"
        r = run_checker(rep)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("vibe", r.stdout)

    def test_green_with_fail_fails(self):
        rep = good_report()
        rep["results"][0]["verdict"] = "FAIL"
        rep["results"][0]["detail"] = "protocolVersion was 2024-11-05"
        r = run_checker(rep)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("GREEN requires", r.stdout)

    def test_fail_without_detail_fails(self):
        rep = good_report()
        rep["results"][0]["verdict"] = "FAIL"
        if "detail" in rep["results"][0]:
            del rep["results"][0]["detail"]
        rep["tally"] = {"pass": 15, "fail": 1, "skip": 0}
        rep["verdict"] = "RED"
        r = run_checker(rep)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("requires a detail", r.stdout)

    def test_yellow_with_skip_passes(self):
        rep = good_report()
        rep["results"][-1]["verdict"] = "SKIP"
        rep["results"][-1]["observed"] = "connector has no raw HTTP fetch"
        rep["results"][-1]["detail"] = "no raw fetch in this connector; T13-T15 need curl"
        rep["tally"] = {"pass": 15, "fail": 0, "skip": 1}
        rep["verdict"] = "YELLOW"
        r = run_checker(rep)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
