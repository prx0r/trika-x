# LEAD REVIEW — full peer review of the 2026-11-08 body of work

*Reviewer: lead agent, adversarial mode. Reviewed `main` at `f177d50`, then
raised findings, fixed what was fixable without a human, and re-verified.
This is not a self-congratulation pass: §2 lists five real defects, three of
which were mine and are now corrected in `3cbc877` / `2aeb2bb`.*

## 1. Gates re-run (all reproduced unless noted)

| Gate | Result |
|---|---|
| `unittest discover -s formal-trika/tests` | **94 OK** |
| `evidence_check.py` | 157 theorems · 155 entries + 2 exemptions · 57 chunk refs · 0 bad · **16/154 (10%)** |
| `table.py --check` | rc 0 |
| `freshness.py --check` | **SHARP** (after capturing legitimate drift) |
| `mcp_catalog.py --check` | SHARP, 104 tools / 8 families |
| `federation_pretest.py` | GREEN (28 representative) |
| `axiom_audit.py --check` | CLEAN (static; kernel unverified — stated) |
| `essay_derive.py` | 6 essays, 6 PARTIAL, **0 BROKEN** |
| openpatala `check.py` | GREEN + 2 recorded BLOCKED roots |
| svread CI (`main`) | green (reader: manifest, 4× node --check, node tests, MCP tests) |
| svread **live** | 909 traces, verify packs 200, `verifyFooter` present |

No claimed number failed to reproduce. That is the highest-severity class in
this project and it is clean.

## 2. Findings

### F1 — P-VBT1 counted a map, then spoke as the text (P1, FIXED)

`forms_eight` proves the eight-term ARGMAP roster is eight and distinct —
true. But `TABLE-READINGS.md` called it "the opening question's whole
inventory". The verses name more: v.4 has `śaktisvarūpa` ("power-formed"),
a distinct word from `śaktitraya` in v.3. Whether `bhairavākṛti` is a tenth
option or the locus of the ninefold division is a scholarly call the layers
do not settle.

**Disposition:** prereg/Lean kept (append-only history); added
`formal-trika/PREREGISTRATION-VBT1-CORRECTION-2026-11-08.md`; readings
corrected; Lean header now states the scope limit. Twin still refuses.
This is exactly the "checked means several things" collapse PR #7 §3 named.

### F2 — P-VBT2 the same, smaller (P2, FIXED)

`coords_three` counts C1's three coordinates. v.14
(`dikkālakalanonmuktā deśoddeśāviśeṣinī`) also removes place (`deśa`) and
point (`uddeśa`) — five in the verse. Reading corrected; noted in the same
correction file.

### F3 — Public verify packs said COMPLETE with a BLOCKED gate (P1, FIXED)

141 of 236 `COMPLETE` bundles carry `assurance.chunk_gate = BLOCKED`; 30 more
are `UNKNOWN`. The trika-x bundle separates those dimensions, but the svread
verify-pack manifest published only `verdict`, and the reader renders that
as a bare "COMPLETE" badge. A public reader could not see that the
deterministic gate was blocked.

**Disposition:** `emit_verify.py` now carries `verdict_scope`, `assurance`,
`caveats`, `gaps` in every pack; wording fixed to REGISTERED; new wiring test
asserts the disclosure across packs. Fixed and **redeployed live**.

### F4 — "Published" was repo-true, live-false (P1, FIXED)

909 traces and packs were committed, but the live site still served the old
13 traces and an `app.js` without the R4 footer: svread does not auto-deploy
(CI is integrity-only; `deploy.sh` is manual). The docs said "published".
**Disposition:** deployed; verified live — 909 traces, footer present, packs
return 200 with gate disclosure. Lesson added: a publish claim names the
host and the check that proves it.

### F5 — `essay_derive` accepted verse ids it never checked (P2, FIXED)

Any claim with a `verse_id` passed; only presence was required. Now a claim
citing a verse outside its chunk's ledger range is BROKEN
(`phr-p05-v99` → BROKEN). Unparsable id forms stay a soft note because
verse-id conventions differ across works. Test added.

### F6 — Freshness ledger is not exhaustive (P3, OPEN)

The ledger tracks DB, evidence, bridge, traces, source-map, surface, essays.
It does **not** track: chunk-verse map (105 chunks), crux queue (882),
review packets (7), decision-trail coverage (3/87 ledgers, 2/87 with
layer-accept). Those numbers live only in docs and can rot. Recommend
extending the ledger before the next session quotes them.

### F7 — `phrdaya` ledger spans remain the PR #7 P0 (P1, OPEN, not mine)

`phrdaya/passages.jsonl` still labels `verses: 1-4` while carrying one
sūtra. Unchanged since PR #7. `chunk_verse.py` reports phrdaya OPEN ("span
break inside phr-p01"), which is the honest state. Filed in
`LANE-ASKS-2026-11-08.md`; needs the translation lane + a Sanskrit reviewer.

### F8 — Many root docs still link with loose paths (P3, OPEN)

A repo-wide audit of *markdown link syntax* is clean (0 broken). But many
docs reference `PREREGISTRATION.md`, `TABLE-READINGS.md` etc. as bare text
without a path, which is unverifiable by tooling. Not urgent; worth a sweep.

## 3. What stands (verified, not asserted)

- **Trace system:** 909 bundles, full-compare verify (removed gaps now fail),
  assurance-separated, theorem join on `(work, locator)`, clean-checkout
  fixture suite. Re-verified after the changes.
- **Formal rungs:** 4 theorems added this session (phr-p05 ×2, VBT ×2), each
  with prereg, single-line twin that refuses, EVIDENCE entry, TABLE reading,
  and two harness receipts (`ab5dfcc`, `247d897`) plus `f177d50+dirty`, all
  exit 0/0/0.
- **Essay gate:** forged markers, nonexistent chunks, changed receipts and
  pre-review signoffs all fail closed (7 tests); corpus 6/6
  READY_FOR_HUMAN_REVIEW.
- **MCP:** docs match the live surface; catalog drift gate; guide-prefix test
  would catch the old `book__*` drift.
- **Peer-review debt:** disposition ledger exists; nothing claimed closed
  that is not machine-checked.
- **Hygiene:** no secrets in the public snapshot branch (verified by
  pattern scan of the pushed tree); disk +3.1G; docs reorganized with a
  verified link graph.

## 4. Rulings

- **Tiers:** all new rungs stay **R**. Second-encoder review is still owed
  and still blocks anything above R — `forms_eight`/`coords_three` being
  faithful-to-map rather than faithful-to-text reinforces that block.
- **Velocity:** four finite theorems in a session is fine; the correction
  above is the reminder that count-facts are cheap to produce and easy to
  over-describe. Next rung should be chosen for doctrinal leverage.
- **Publishing:** a "published" claim must name the host and a live check.
  Repo-commit is not publication for svread.
- **Ledger discipline:** every number quoted in a doc should be in
  `freshness.json`; if it cannot be measured by a command, it does not get
  quoted with confidence.

## 5. Verdict

**The body of work stands.** Every headline reproduces; the defects found are
labelling and disclosure defects, not fabricated results, and three of five
are already fixed and deployed. Nothing needs to be un-pushed or un-merged.

**Must be redone:** nothing structural.
**Must be finished by someone else:** the five lane asks, the scholar
rulings, the owner tokens, and the phrdaya span repair (F7).
**Next lead's first job:** extend the freshness ledger (F6), then blind
re-derive the gap-list head (vbt-p03) on a different model family.

*Findings F1–F5 are committed in `3cbc877` (trika-x) and `2aeb2bb` (svread).*
