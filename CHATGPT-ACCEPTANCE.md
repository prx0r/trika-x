# CHATGPT acceptance — run the estate from ChatGPT's side
*Status: CANONICAL. ChatGPT-side acceptance (raw T0–T15 + connected T16–T20), report protocol; measured 2026-11-14.*

This directory holds an acceptance suite ChatGPT itself executes, using only
what ChatGPT can reach: the public MCP endpoint plus public HTTPS. No box
access, no credentials, no code checkout. If all 16 steps pass from ChatGPT's
side, the public surface does what the repo claims. If any step fails, the
step's assertion names the exact divergence — fix the system or the pinned
expectation deliberately, never the other way round.

## Files

- `formal-trika/tests/chatgpt_acceptance.json` — the machine-readable suite
  (T0–T15). Pinned verbatims are snapshots measured live 2026-11-14.
- `formal-trika/tools/chatgpt_acceptance_run.py` — the reference runner
  (stdlib only). Proves the spec is executable, not prose:
  `python3 formal-trika/tools/chatgpt_acceptance_run.py` → `16/16`.
- `formal-trika/tests/chatgpt_connected_acceptance.json` — T16–T20 for
  connected ChatGPT sessions (native plugin tools, no raw RPC). Steps carry
  `"box_runnable": false` and SKIP with their reason outside ChatGPT.
- `formal-trika/tests/test_chatgpt_acceptance.py` — CI wrapper: raw suite
  must pass live; connected suite must skip cleanly (same pattern as
  `test_mcp_bridge.py`).

## What it covers

| Step | What ChatGPT checks |
|---|---|
| T0 | MCP handshake negotiates `2025-06-18` |
| T1 | `tools/list` exposes the verification surface (≥50 tools, named tools present) |
| T2–T3 | Identity resolves known works (`EXACT`) and admits unknown ones (`NONE`, never invented) |
| T4 | Passage evidence returns layers + verifiable `projection_sha256` |
| T5 | `formal__trace` returns COMPLETE with named Lean theorems |
| T6 | Gap report admits incompleteness *with denominators* |
| T7 | Unknown tool fails closed, transport intact |
| T8–T11 | Sitemap, llms.txt, claim JSON-LD honesty states, formal registry JSON — all live |
| T12 | A second host serves the same protocol (no single-endpoint theater) |
| T13–T15 | GEO: robots names AI crawlers + sitemap; sitemap exposes claim pages; llms.txt names the verification path |

## Two execution modes (read this first — added 2026-11-14)

ChatGPT sessions differ in what they can reach. The suite comes in two files
for the two realities, same verdict contract in both:

| Mode | File | Who runs it | Transport |
|---|---|---|---|
| **raw-rpc** T0–T15 | `formal-trika/tests/chatgpt_acceptance.json` | any agent with HTTPS (box runner, other agents, CI) | raw JSON-RPC POST + plain GET |
| **connected-tool** T16–T20 | `formal-trika/tests/chatgpt_connected_acceptance.json` | ChatGPT with the Svatantrya plugin connected | native connected tools; NO raw RPC needed |

Measured 2026-11-14: **raw mode is green end-to-end (16/16) from a box
runner.** Connected mode has exactly one PARTIAL observation on record (T18
evidence hash via plugin) and has **never completed a full pass** — a
connected ChatGPT session had no generic JSON-RPC tools/list/call transport
and no page fetch. T19 (connected formal trace) is the single most valuable
unrun check in the estate: if it returns COMPLETE with named theorems, the
whole chain is proven from inside ChatGPT itself.

Run the reference runner with `--suite` to pick a file; steps marked
`"box_runnable": false` SKIP with their reason instead of failing.

## Copy-paste prompt for ChatGPT (or any MCP agent) — raw mode

> Fetch https://raw.githubusercontent.com/prx0r/trika-x/main/formal-trika/tests/chatgpt_acceptance.json
> (use the PR branch path instead when testing a PR). For each step in order,
> perform the request with your MCP tools (initialize / tools/list /
> tools/call) or a plain HTTPS fetch, exactly as specified. For each step,
> report PASS or FAIL with the observed value next to the expected one. Do
> not skip steps. Do not invent tools that are not in the tools/list you
> actually received. At the end, give the tally X/16 and paste any failing
> step's full response. If a pinned verbatim (theorem name, status string) has
> legitimately changed upstream, say so explicitly instead of marking it pass.

## Copy-paste prompt for ChatGPT (connected mode — use this one)

> You have the Svatantrya plugin connected (native tools, no raw JSON-RPC).
> Fetch https://raw.githubusercontent.com/prx0r/trika-x/chatgpt-acceptance-suite/formal-trika/tests/chatgpt_connected_acceptance.json
> (use `main` instead of the branch name once merged). For steps T16–T20 in
> order, perform each step with your connected Svatantrya tools; where no
> connected equivalent exists, say NOT_RUNNABLE with the reason instead of
> inventing a call. For each step report PASS / FAIL / SKIP with the observed
> value next to the expected one. At the end give the tally, fill the report
> template below (same shape as the raw-mode one, format tag
> `svatantrya.chatgpt-acceptance-report/1`), and flag T19 explicitly: a
> COMPLETE formal trace from inside ChatGPT is a first, and a FAIL there is
> the highest-priority finding in this program.

## Rules for maintainers

1. Pinned values are snapshots, not constants. Counts legitimately grow
   (`gte`); names and status strings must match exactly — a mismatch is a
   finding, not noise.
2. Never loosen an assertion to turn red green. Fix the system, or update the
   pin in a reviewed commit with the new measured value and date.
3. The suite runs against LIVE endpoints. A red step after a deploy means the
   deploy changed the surface — check the diff before anything else.
4. Google-side indexing (Search Console, plugin directory) is owner-gated and
   deliberately NOT in this suite. What an unauthenticated agent can verify
   is in; what needs an owner account is listed in `../70-v1-tracker.md` style
   queue docs, not faked here.
5. Known GEO improvement (svread lane, not this repo): `llms.txt` names the
   verification path but does not yet point agents at the live MCP endpoint
   URL. Filed as a lane note; the suite asserts what exists today.

## Reporting back — so results are interpretable, not vibes

A test without a readable report is noise. Every ChatGPT run MUST return two
things: (a) a filled copy of the report template below, and (b) the same
content as JSON matching `formal-trika/tests/chatgpt_report_schema.json`
(validate it here first with `python3 formal-trika/tools/chatgpt_report_check.py report.json`).

### Copy-paste report template (ChatGPT fills this in, verbatim values only)

```
CHATGPT ACCEPTANCE REPORT — <date>
Suite commit: <trika-x sha the JSON was fetched from, or branch@sha>
Agent: <model + mode, e.g. ChatGPT-5 + MCP connector "Svatantrya">
Connector/tools used: <native MCP tools / plugin name / manual curl>
Auth used: none | bearer(owner) — writes were/were not attempted: ...

PER-STEP (one line each, observed value REQUIRED — "works"/"looks good" is not an observation):
T0-handshake:    PASS/FAIL/SKIP — observed: <protocolVersion echoed>
T1-discovery:    PASS/FAIL/SKIP — observed: <N tools; named-tool check result>
T2-known:        PASS/FAIL/SKIP — observed: <status + entity id>
T3-unknown:      PASS/FAIL/SKIP — observed: <status value returned>
T4-evidence:     PASS/FAIL/SKIP — observed: <bytes; has layers true/false; sha pattern ok true/false>
T5-trace:        PASS/FAIL/SKIP — observed: <verdict; theorem count; first theorem name>
T6-gaps:         PASS/FAIL/SKIP — observed: <total=N; gaps count>
T7-unknown-tool: PASS/FAIL/SKIP — observed: <HTTP code; error text, first 120 chars>
T8-sitemap:      PASS/FAIL/SKIP — observed: <HTTP code>
T9-llms:         PASS/FAIL/SKIP — observed: <HTTP code>
T10-claim:       PASS/FAIL/SKIP — observed: <HTTP code; UNPINNED present true/false>
T11-registry:    PASS/FAIL/SKIP — observed: <HTTP code; parseable true/false>
T12-2nd-host:    PASS/FAIL/SKIP — observed: <tool count on formal host>
T13-robots:      PASS/FAIL/SKIP — observed: <GPTBot listed true/false; sitemap ref true/false>
T14-claims:      PASS/FAIL/SKIP — observed: <claim URL found true/false>
T15-llms-names:  PASS/FAIL/SKIP — observed: <formal__trace named true/false>

TALLY: <pass>/<fail>/<skip> out of 16. Must add to 16.
ANOMALIES (anything surprising, even if steps passed): <free text, or "none">
VERDICT: GREEN (all pass) | YELLOW (no FAIL, ≥1 SKIP with reason each) | RED (≥1 FAIL)
```

SKIP is allowed only with a reason in the observed field (e.g. "connector
lacks raw HTTP fetch; T8–T11 unverifiable from here"). A SKIP without a
reason is a FAIL of the report, not of the system.

### Interpretation guide — what each outcome means, and what to do

| Outcome | Meaning | Action |
|---|---|---|
| T0 FAIL | endpoint down, protocol changed, or network blocked | check `curl` handshake manually; check systemd/tunnel status; do not merge/deploy anything until green |
| T1 count drop / tool missing | surface changed (tool added/removed/renamed) or child down (FailOpen excluded it) | diff live `tools/list` vs pin; if a child is down, fix the child; update pin deliberately if the change is intended |
| T2 FAIL | identity regression — resolver no longer resolves a known work | investigate openpatala immediately; nothing downstream is trustworthy until this is green |
| T3 anything but NONE | **critical**: resolver invents entities or errors opaquely | stop; investigate before any merge/deploy touching identity |
| T4 FAIL | evidence pipeline changed (projection format, layers key, missing sha) | diff against projection source; svread lane if content moved, trika-x lane if the contract moved |
| T5 verdict ≠ COMPLETE | data changed (new theorems? gaps closed?) or formal service issue | compare theorem list to pin; check `formal__runs` / harness; a newly COMPLETE chunk is good news to record, not a failure to hide |
| T5 theorems differ | registry changed (new rung promoted, entry edited) | verify against EVIDENCE.json on main; update pin with date if legitimate |
| T6 gaps empty | suspicious: either coverage completed (verify independently via treeka!) or gap reporting broke | do NOT celebrate without the independent check |
| T7 transport ≠ 200 or no clean error | transport regression | critical: the fail-closed contract is broken; fix before anything else |
| T8–T11 FAIL | svread surface/deploy issue, not trika-x logic | check deploy status + manifest; the trika-x side is likely fine |
| T12 FAIL | second host down or diverged | check formal host health independently; single-host dependence is a finding |
| T13–T15 FAIL | robots/sitemap/llms.txt changed or undeployed | check svread deploy + emitter; counts move, names should not |
| Verdict GREEN | all 16 pass | surface matches the repo; safe to cite this run as provenance |
| Verdict YELLOW | no FAIL but SKIP(s) with reasons | record what ChatGPT could not exercise (e.g. no raw HTTP); re-run those steps another way |
| Verdict RED | ≥1 FAIL | do not describe the surface as verified; fix per the row above, re-run, attach both reports |

### How we tell "system changed" from "test rot"

- The pin carries the date it was measured (`pinned 2026-11-14` in the
  suite). A mismatch against a pin older than the last relevant deploy is
  *expected drift until proven otherwise* — check deploys first, code second.
- Counts use `gte` (growth is normal). Only names, status strings, and
  structural shapes use exact match — those changing is always a finding.
- The reference runner (`chatgpt_acceptance_run.py`) is the tiebreaker: if
  the runner passes from here and ChatGPT reports FAIL, the difference is in
  ChatGPT's path (connector, caching, tool naming) — record exactly which,
  it matters for real users too.
