# LEAD PACK — read-first index

> **Current entry point:** Read [the 2026-11-06 peer review](../../docs/log/PEER-REVIEW-2026-11-06.md),
> [the correction to preregistration](../../formal-trika/PREREGISTRATION-2026-11-06.md),
> and [the fresh-checkout run guide](../../formal-trika/README.md) first. The
> historical handover below uses an old machine's paths and reports two Lean
> failures that this review repairs. Its claims about proof keys and ungated
> transitions are superseded; no source-to-essay gate is built by this review.

**For the incoming lead agent. Owner rule: formalizations arise OUT OF the data. Nothing here defines anything. Machine proposes, human disposes.**

Disk is 98% full — this pack is **pointers, not copies**. Every entry is an absolute on-box path. Read in this order. Do not duplicate bytes.

## Read order (30 min)

1. `/root/TRIKA-X-SEEDS.md` (119 lines) — the evidence index. A/B/C/D/E/F/G/H/I sections = the whole map.
2. `/root/trika-x/INDEX.md` — the two reference corpora (Barendregt + Thon Ly) and the 7-rung transfer table.
3. `/root/trika-x/VISION-ARCHITECTURE.md` (390 lines) — the Lean-recognition-stack vision. PROPOSED, asserts nothing built beyond what it cites.
4. `/root/trika-x/formal-trika/PREREGISTRATION.md` + `PREREGISTRATION-RECOGNITION.md` — prereg before code, tiers T/R, predictions P-TK1–4 / R-REC1–8, kill criteria. Never edit; correction = new file.
5. This pack's `LEAD-HANDOVER.md` (top of `lead-pack/`) — mission, tiers, build order, 2 open Lean bugs, what the lead agent owns.

## Folder map

| Folder | What | Key paths inside |
|---|---|---|
| `01-reference-thonly/` | Thon Ly = the METHOD we copy (prereg → controls → mutation → verdicts) | `repos/formal-abhidhamma/`, `repos/thonly-publications/` |
| `02-reference-barendregt/` | Barendregt = the AXIOM STYLE we copy (implicit-spec, AM0) | `papers/barendregt/` (8 PDFs) |
| `03-recognition-formulation/` | Owner's recognition definitions (AM0 σ-flip, 4-conjunct, memory, daimon) | `gochema/library/recognition/` |
| `04-inexternalism-aperture/` | Inexternalism + aperture + sciencetime/mepit/csid (the R-tier readings) | `gochema/library/recognition/aperture/` |
| `05-endgame/` | The machine this plugs into (7 varieties, master sequence, Scholar contract) | `svread/ENDGAME*.md`, `RESOURCES.md`, `endgame/` |
| `06-evidence-gold/` | T-tier ground: gold translations + pushing conjectures + essay kits | `translation-work/`, `ipvv/site/data/pushing/`, kits |
| `07-formal-trika-current/` | What Lean checks TODAY (green + 2 red) | `formal-trika/control/`, `formal-trika/recognition/`, `runs/` |

## Tier discipline (load-bearing, everywhere)

T = root text · R = reconstruction (AM0, inexternalism, all our glosses — never smuggled as T) · E = empirical · C = correspondence · H = hypothesis · X = rejected. An R-rule never promotes itself. Every theorem carries model size (64/4096/128). A finite-model theorem is not a theorem about minds.

## What NOT to do

- No top-down definitions. No uncited mappings. No treating heuristic PASS (sanskritbench, audit) as semantic proof — only `lean decide` counts, inside its scope.
- This pack's `formal-trika/` consumer reads `translation-work/ipvv/gochema` as evidence ONLY. It never writes into those repos. A needed source fix = a CLAIM, not a patch (ipvv Law #1: T1 immutable).
- Do not `cp` PDFs/repos into the pack. Disk 98%. Pointer discipline.
