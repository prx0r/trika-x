# VALIDATED RESULTS — 2026-11-14 (full end-to-end test pass)

*Every number below was produced by running the command shown, on this box,
this session. Nothing is remembered or copied from a doc. Lean = 4.34.1
(commit 5045d005), box DB = live postgres.*

## Formal verification (the centre stage)

| Harness | Result | Command |
|---|---|---|
| Lean control (positives + must-fail twins) | **53 PASS / 0 FAIL** | `sh formal-trika/control/run.sh` |
| Lean recognition | **26 passed / 0 failed** | `sh formal-trika/recognition/run.sh` |
| EVIDENCE registry | **157 theorems · 155 entries · 2 exemptions · 0 problems** | `tools/evidence_check.py` |
| Passage coverage | **16/154 chunks (10%)**, gap list published | `tools/evidence_check.py` |
| TABLE readings | **rc=0** | `tools/table.py --check` |
| Axiom audit | **CLEAN (static)** — no sorry/axiom/native_decide | `tools/axiom_audit.py --check` |
| Full test suite | **103 tests OK** | `python3 -m unittest discover -s formal-trika/tests` |

Each control/recognition line is a theorem that PASSED *and* a hand-written
mutant that was REQUIRED to fail (anti-vacuity). A green run means the checker
bites, not just compiles. This is the machine-checked spine ChatGPT will read.

## ChatGPT front door (bridge, this branch)

| Check | Result | Command |
|---|---|---|
| Bridge selftest | **OK, sheaf=25 tools** | `tools/mcp_bridge.py --selftest` |
| End-to-end over HTTP | **8/8 checks passed** | `tools/bridge_e2e.py` |
| Public layer legend | T1→draft-translation, L0→literal-gloss, ARGMAP→argument-map … | (in e2e) |
| Read sheaf served | 25 of 112, **87 withheld** (writes need OAuth) | (in e2e) |
| Real passage evidence | bodhapancadasika/bod-p01-v01 → 9474 B, layers + projection_sha256 | (in e2e) |
| Real formal trace | tantrasara-a08/tsa08-p03 → **verdict COMPLETE**, Lean theorems returned | (in e2e) |
| Write refusal | `video__vf_launch` → -32001 unauthorized (honest) | (in e2e) |
| Layer roundtrip | **9/9** codes↔public names | `layer_names.py` |

The E2E runs the actual gateway + actual box DB + actual Lean trace, over
real HTTP (POST/GET/DELETE), not mocks. `formal__trace` returns theorems with
`status: ARGMAP-PINNED`, `run_bound: false` — correctly labelled as registry
references, not per-declaration proven (the honesty the trace spec demands).

## Essay pipeline

| Check | Result |
|---|---|
| `essay_derive` | 6 essays, **PARTIAL=6, BROKEN=0** (honest: no essay claims full derivability yet) |
| `essay_check` tests | **14/14 OK** (span+digest+edition binding) |
| `pushback.py` | CLI live (mock/go/cf), verbatim shield, never edits |

## Identity root (openpatala)

| Check | Result |
|---|---|
| `check.py --status` | **GREEN** + 2 recorded BLOCKED (adapters discover nothing; witnesses 0) |
| Box DB | works **1034** · passages 909 · assertions 1559 · people 20 · witnesses **0** |
| Source-map resolve | bodhapancadasika/tantrasara-a08/paramarthasara/ipvv all present (87 works) |
| Honest UNRESOLVED | non-key work → UNRESOLVED "draft-only downstream" (correct) |

## Recorded drift (NOT laundered — fail-closed)

`freshness.py --check` = **DRIFT**, and that is the honest state:
- openpatala works **555→1034**, editions 102→581, etexts 87→566 — an ingest
  with no provenance receipt; the ledger is NOT rewritten until the lane says
  which loader ran. Passages/assertions unchanged, so identity of existing
  rows is intact.
- svread manifest 7078→11109 assets (their lane).
Formal numbers MATCH (157/155) — no drift there.

## What "live" means right now

- **Lean + traces + passage evidence: live and tested** via the gateway and
  bridge (this branch). An agent can call `formal__trace` and get real,
  machine-checked theorem rows today.
- **Public over the internet: NOT YET.** The bridge binds 127.0.0.1; exposing
  it needs the tunnel (owner) + OAuth for writes (worker lane). Read sheaf is
  ready to face ChatGPT the moment the tunnel exists.
- **Registry says 109/scholar 38; live is 112/scholar 41** — svread lane
  refresh owed before the connector shows the full surface.

*Machine proposes, human disposes. BLOCKED is never PASS. Every number above
is reproducible by the command in its row.*
