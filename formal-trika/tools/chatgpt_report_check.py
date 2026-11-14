#!/usr/bin/env python3
"""chatgpt_report_check.py — validate a ChatGPT acceptance report, not the system.

A report claims "I ran the suite and saw X". This checker verifies the claim
is well-formed and internally consistent: right shape, all 16 known steps
exactly once, tally math matches rows, every FAIL/SKIP carries a reason, no
vibe-words standing in for observations, verdict consistent with rows.
It says NOTHING about whether the live system passes — run the suite for that.

  python3 formal-trika/tools/chatgpt_report_check.py report.json
  exit 0 = report is interpretable. exit 1 = report is theater; send it back.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE.parent / "tests" / "chatgpt_report_schema.json").read_text())
EXPECTED_FORMAT = "svatantrya.chatgpt-acceptance-report/1"

STEP_IDS = ["T0-handshake", "T1-discovery", "T2-identity-known",
            "T3-identity-unknown", "T4-evidence", "T5-formal-trace",
            "T6-gaps-honesty", "T7-unknown-tool", "T8-sitemap", "T9-llms",
            "T10-claim-page", "T11-formal-registry", "T12-second-host",
            "T13-robots", "T14-sitemap-claims", "T15-llms-names-verification"]

VIBE_WORDS = {"looks good", "works", "works fine", "ok", "okay", "fine",
              "good", "passed", "pass", "all good", "seems fine", "yes", "yep"}


def fail(problems, msg):
    problems.append(msg)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: chatgpt_report_check.py <report.json>")
        return 2
    problems: list[str] = []
    try:
        rep = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"FAIL: report is not readable JSON: {e}")
        return 1

    if rep.get("format") != EXPECTED_FORMAT:
        fail(problems, f"wrong format tag: {rep.get('format')!r} (want {EXPECTED_FORMAT!r})")

    for key in ("date", "agent", "connector", "auth", "suite",
                "endpoints", "results", "tally", "anomalies", "verdict"):
        if key not in rep:
            fail(problems, f"missing top-level key: {key}")

    results = rep.get("results", [])
    if not isinstance(results, list):
        fail(problems, "results must be a list")
        results = []
    ids = [r.get("id") for r in results if isinstance(r, dict)]
    if sorted(ids) != sorted(STEP_IDS):
        missing = [i for i in STEP_IDS if i not in ids]
        extra = [i for i in ids if i not in STEP_IDS]
        if missing:
            fail(problems, f"missing steps: {missing}")
        if extra:
            fail(problems, f"unknown steps: {extra}")
        if len(ids) != len(set(ids)):
            fail(problems, "duplicate step ids")

    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for r in results:
        if not isinstance(r, dict):
            fail(problems, "result row must be an object")
            continue
        v = r.get("verdict")
        if v not in counts:
            fail(problems, f"{r.get('id')}: verdict must be PASS/FAIL/SKIP, got {v!r}")
            continue
        counts[v] += 1
        obs = r.get("observed", "")
        if not isinstance(obs, str) or not obs.strip():
            fail(problems, f"{r.get('id')}: observed value required (verbatim, not a vibe)")
        elif obs.strip().lower() in VIBE_WORDS:
            fail(problems, f"{r.get('id')}: {obs.strip()!r} is a vibe, not an observation — paste the actual value")
        if v in ("FAIL", "SKIP") and not str(r.get("detail", "")).strip():
            fail(problems, f"{r.get('id')}: FAIL/SKIP requires a detail (what was seen / why skipped)")

    tally = rep.get("tally", {})
    if not isinstance(tally, dict) or any(
            tally.get(k) != counts[k.upper()] for k in ("pass", "fail", "skip")):
        fail(problems, f"tally {tally} does not match rows {counts} (must add to 16)")

    verdict = rep.get("verdict")
    if verdict == "GREEN" and (counts["FAIL"] or counts["SKIP"]):
        fail(problems, "GREEN requires all 16 PASS")
    elif verdict == "YELLOW" and (counts["FAIL"] or not counts["SKIP"]):
        fail(problems, "YELLOW requires no FAIL and at least one SKIP with reason")
    elif verdict == "RED" and not counts["FAIL"]:
        fail(problems, "RED requires at least one FAIL")
    elif verdict not in ("GREEN", "YELLOW", "RED"):
        fail(problems, f"verdict must be GREEN/YELLOW/RED, got {verdict!r}")

    if problems:
        print("FAIL: report is not interpretable:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"REPORT OK: {counts['PASS']}/{sum(counts.values())} steps, verdict {verdict}, "
          f"agent {rep.get('agent')}, suite {rep.get('suite', {}).get('commit', '?')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
