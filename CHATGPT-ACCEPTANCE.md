# CHATGPT acceptance — run the estate from ChatGPT's side

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
- `formal-trika/tests/test_chatgpt_acceptance.py` — CI wrapper (same pattern
  as `test_mcp_bridge.py`).

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

## Copy-paste prompt for ChatGPT (or any MCP agent)

> Fetch https://raw.githubusercontent.com/prx0r/trika-x/main/formal-trika/tests/chatgpt_acceptance.json
> (use the PR branch path instead when testing a PR). For each step in order,
> perform the request with your MCP tools (initialize / tools/list /
> tools/call) or a plain HTTPS fetch, exactly as specified. For each step,
> report PASS or FAIL with the observed value next to the expected one. Do
> not skip steps. Do not invent tools that are not in the tools/list you
> actually received. At the end, give the tally X/16 and paste any failing
> step's full response. If a pinned verbatim (theorem name, status string) has
> legitimately changed upstream, say so explicitly instead of marking it pass.

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
