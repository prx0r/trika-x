# LEAD REVIEW — 2026-11-08 evening session (19 commits, `9ee20e5`→`649f42e`)

*Independent re-run, read-only. Every number below was reproduced on box unless marked UNVERIFIED. No Lean harness, no network/model calls, no writes. Single allowed compiler invocation: `Vbt.lean` + `must_fail.py` twin check — PASS.*

## 1. Findings (reproduced vs claimed)

**F1 — Tests: 79 OK. CONFIRMED.** `python3 -m unittest discover -s formal-trika/tests` → `Ran 79 tests … OK` (formal-trika/tests). Matches claimed 79. (Note: tail output is noisy — decision/treeka diagnostics print during suite; the `OK` line is the verdict.)

**F2 — Formal evidence: 157/155, 16/154 (10%). CONFIRMED.** `evidence_check.py` → `theorems: 157, entries: 155, exemptions: 2`; `direct registry references: 16/154`; covered list includes `vbt:vbt-p01, vbt:vbt-p02` (new). Zero bad chunk refs.

**F3 — All four drift gates green. CONFIRMED.** `table.py --check` rc=0 · `freshness.py --check` → `SHARP` · `federation_pretest.py` → `GREEN (28 expected tools)` · `mcp_catalog.py --check` → `SHARP (104 tools, 8 families)`. The 104-tool count is live-probed, not doc-copied.

**F4 — Essay chain: 6/6 PARTIAL, 0 BROKEN, rc=0. CONFIRMED.** `essay_derive.py` output matches claim verbatim (every essay notes witness UNPINNED + UNVERIFIED theorems and/or CANDIDATE mapping). Zero DERIVED in corpus — see Ruling 3.

**F5 — openpatala GREEN with BLOCKEDs. CONFIRMED with counting note.** `check.py`: PASS api-import/mcp-server/evidence-bundle/db-seeded (555 works); BLOCKED ×3 lines — `conformance`, `adapter-conformance`, `witnesses`. The request says "two recorded BLOCKEDs"; conformance + adapter-conformance are one root cause (adapters discover nothing upstream), so "two" is defensible but the check prints three lines. Language hygiene only. **ADDRESSED with note.**

**F6 — Twin spot-check: PASS. CONFIRMED.** `lean -DwarningAsError=true Vbt.lean` compiles; `must_fail.py --positive Vbt.lean --mutant BrokenVbtSeven.lean --theorem forms_eight` → `PASS … forms_eight is false in mutant`. Runs receipts `ab5dfcc`, `247d897` both present in `formal-trika/runs/runs.jsonl`, both exit 0/0/0 with the expected twin-refusal tails (incl. `BrokenVbtSeven`, `BrokenVbtTwoCoords` in 247d897).

**F7 — History: 19 commits, linear, pushed, clean. CONFIRMED.** `git log --oneline -22`: 19 session commits `9ee20e5`→`649f42e` atop `2c83925` — count exact. Local `box/peer-review-batch` = `origin/box/peer-review-batch` at `649f42e`. `git status`: clean except untracked `REVIEW-REQUEST-2026-11-08.md` (this ask doc itself). No rewrites visible; the disclosed pre-push amend (ochema gitlink) is consistent with a single `b9724e7` entry.

**F8 — ochema gitlink repair: CORRECT. CONFIRMED.** `git ls-files -s formal-trika/imports/ochema | head -2` → `100644` blobs, no `160000` gitlink. Repair as disclosed in process notes §1.

**F9 — Traces 909 (236 COMPLETE / 673 PARTIAL), 0 errors. CONFIRMED.** `trace_all.py --index-only` reproduces exactly; both claimed samples re-VERIFIED with verdicts unchanged (`phrdaya:phr-p01` COMPLETE, `ipvv:chunkA-svatyandya` PARTIAL). Disk 3.7G free (96%) consistent with +2.4G reclaim from ~1.3G. Tier-1 targets were gitignored/rebuildable; freaktown skip (live `vite preview`) logged with reason.

**F10 — Queue/decision/packets numbers. CONFIRMED.** `crux-queue.jsonl` = 882 lines. `decision_check.py` → 87 works, 1 scholar ledger (paramarthasara), 0 layer-accept markers — matches "1/87 + 0/87". `formal-trika/swarm/review-packets/` holds exactly 7 files (1 robo + 6 expansions).

**F11 — Secrets/push hygiene. CLEAR.** Crude secret grep hits are all false positives (`task-`, `ask-`, `SK-verse`, `disk-for-bowtie-*.jpg?w=` URLs). No diary/private material, no witness invention, no signoffs, no history edits. Lanes respected (no translation-work/svread writes observed in stat).

**F12 — Bridge canonicals intact. CONFIRMED (outcome).** `formal-trika/bridge/` holds 23 `chunk-verse-*-2026-11-06.json` files. **But the "byte-identical, therefore deleted" step is UNVERIFIED** — the reruns were removed before commit, no sha256 log kept, `git log --diff-filter=D -- formal-trika/bridge/` is empty. Outcome right, process claim taken on trust. **PARTIAL.**

**F13 — Pushback artifact truncated. PARTIAL.** `formal-trika/swarm/robo-param-p02-2026-11-08-071651.pushback.md:21` ("for these loc") and `:36-37` ("Given the absence of formal entries in the banked" — ends mid-sentence): generator truncation baked into a pushed file. Substance of the honest remainder survives (no formal entries for v15/v16/v18 → claims refused as authority), and the non-canonical labelling + `never edits` footer are intact — but the file is visibly incomplete. Either regenerate or annotate; do not quote the truncated sentences.

**F14 — Treeka refresh cross-validates. CONFIRMED.** Treeka reports `no_formal_reference: 893`; 909 − 16 registry-referenced = 893 exactly — independent agreement with `evidence_check`. Queue head `vbt:vbt-p03` matches process-notes §14. Refresh direction (EVIDENCE→treeka) correct; masking-regression hypothesis would require EVIDENCE itself wrong, backstopped by 0-bad chunk refs.

## 2. Rulings on the 8 method questions

**R1 — Roster semantics: bookkeeping, honestly labelled; NOT formalisation of doctrine.** `formal-trika/control/Vbt.lean:1-16` header explicitly states what the file IS (`decide` roster arithmetic) and IS NOT (no Bhairava-form doctrine, no dhāraṇā claims). The MODEL_CHECKED-only contract holds on the Lean side. The load-bearing move is tier-by-inheritance (R because ARGMAP/L2/C1 are R), and `evidence_check` verifies existence, not semantics (author's own R1 admission). **Ruling: ships as R-tier count-fact only; every citation must carry the R-tier + "registry refs unreviewed" qualifier. ADDRESSED with constraint.**

**R2 — Twin quality: anti-vacuity check, not semantic validation.** Single-roster-deletion twins rule out `True`-trivial theorems (the theorem is load-bearing on its roster — F6 proves this much). They say nothing about whether the roster carves nature. **Ruling: sufficient for R-tier; second-encoder review remains owed and BLOCKS any promotion above R. PARTIAL — blocks promotion, not current tier.**

**R3 — `essay_derive` UNMAPPED=PARTIAL: SOUND taxonomy, weak gate in practice.** Read `formal-trika/tools/essay_derive.py:104-113`: missing `openpatala` block → `problems` → BROKEN; present-but-UNMAPPED → `notes` → PARTIAL. This matches the docstring taxonomy (`:12-15`: PARTIAL = hop present-but-CANDIDATE; BROKEN = hop missing). The line is principled, not generous. **But: 6/6 PARTIAL, 0 DERIVED — the gate currently certifies "honestly incomplete" and has never yet discriminated a green chain. Ruling: rule STANDS; require a first DERIVED exemplar (or per-essay distance-to-DERIVED) before any Variety-1 DOI. OPEN as a milestone, not a defect.**

**R4 — Duplicate-map deletion: outcome CORRECT, step UNVERIFIED.** Regenerating with new dates would have forked identical bytes under two names — deletion was the right call, and the tree confirms exactly the 23 11-06 canonicals. **Ruling: correct; future reruns must log sha256 before deleting (one line in process notes suffices). PARTIAL → procedural fix only.**

**R5 — Treeka refresh honesty: HONEST.** The 893/909 cross-check (F14) is decisive against masking on current evidence. **Ruling: ADDRESSED. Standing recommendation: add a treeka↔EVIDENCE count cross-check to CI so the next refresh proves itself.**

**R6 — Velocity vs depth: right shape for R-tier fencing, wrong shape if mistaken for coverage.** The five rungs bank finite scope boundaries (what the question inventories, what the verse frees, what closes a sequence) — real but narrow. At ~2 chunks per rung, 10% coverage implies a ~150-rung road at this granularity; plan lane appetite accordingly. No doctrine stands touched; nothing in the tree claims otherwise (Vbt.lean NOT-claims, R-tiers, PARTIAL verdicts all agree). **Ruling: proceed, but the next rung should be picked for doctrinal leverage (queue order), not count velocity. No redone work required.**

**R7 — Rejected variant + P-VBT2 split: both CORRECT.** Held L2 spans verify the rejection: `working-l2-vbt-p02.json` v.11 negates `bhairavaḥ` himself (outside the p01 question set) and kalā (from p01's `śabdarāśikalāmayam`) is nowhere negated in v.11–v.12 — the negation set ≠ the question set, as recorded. P-VBT2's three-way split is banked by C1 (`working-c1-vbt-p02.json` SUMMARY: "free of direction, time and counting") + L2 v.14 gloss, exactly as `PREREGISTRATION-VBT2-RUNG.md:16` claims — but note the Sanskrit compound `dikkālakalanonmuktā` does not self-segment; the three-way reading inherits C1/L2 authority (R-tier, declared). Kill criterion recorded. **Ruling: P-VBT2 banked well enough for R; rejection stands permanently. ADDRESSED.**

**R8 — Push safety: SAFE TO HAVE PUSHED, two hygiene notes.** No secrets, no private material, no overclaim in public docs (all PARTIAL/CANDIDATE/R labels intact; no invented witnesses, DOIs, or signoffs). Notes: (a) the truncated pushback file (F13) is public-facing roughness — fix, don't hide; (b) if `REVIEW-REQUEST-2026-11-08.md` itself is pushed, it exposes internal review posture but no secrets — owner's call, currently untracked. **Ruling: nothing must be un-pushed. ADDRESSED.**

## 3. Verdict

**Stands:** all 19 commits' measured claims reproduce (F1–F11, F14). MCP hardening, trace compiler, freshness gate, both rung families with twins + receipts, treeka refresh, propose-loop pilot, disposition ledger, Tier-1 disk reclaim — verified as built.

**Must be redone:** nothing structural. Two small repairs: (a) annotate or regenerate the truncated pushback remainder (F13); (b) adopt the sha256-before-delete one-liner for future reruns (F12/R4).

**Stays blocked and on whom:** P-TK1 / rater-2 / ti-ca / NGMPP witness eyes — scholar lane. Zenodo token / cron install / token rotation / Search Console / dīkṣā policy — owner. svread `emit_verify` publication of the 909 packs, translation-lane decision-trail wiring + chunk↔verse map, bench tau scale (quota) — lanes/quota. Second-encoder twin review — owed before any rung promotes above R (scholar/lead). First DERIVED essay chain — owed before any DOI (machine-buildable, R3).

Highest-severity class (number fails to reproduce): none found. Every claimed number in the request doc reproduced on re-run.
