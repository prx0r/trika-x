# RED TEAM CHARTER — 2026-11-10

Goal: break everything we built. No bullshit. Every probe writes:
- WANT: what we expect if the gate is honest
- SAW: what actually happened (with command + exit code)
- LOG: /root/trika-x/testing/logs/<T##>.log (raw output, unedited)
- VERDICT: HOLD (honest fail-closed) or GAP (we can lie / bypass / inflate)

Rules:
1. Real commands only. No synthetic claims. Paste exit codes.
2. Fail-closed = success for us. A BLOCKED/PARTIAL/UNPINNED that stays labelled = HOLD.
3. Any number without a reproducing command + source hash = GAP.
4. Any PASS that should have been BLOCKED = CRITICAL GAP.
5. Logs are append-only. Reports in /root/trika-x/testing/reports/.

Chain under test:
openpatala (identity) → translation-work (evidence) → trika-x formal (theorem+twin)
→ traces + verify packs → scholar MCP → essay → release → factories

Quick run:
```
cd /root/trika-x/testing
bash run.sh T02   # runs one probe, logs to logs/T02.log, updates report stub
bash run.sh all   # runs all implemented probes
```
