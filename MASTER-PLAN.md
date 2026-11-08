# MASTER PLAN — Trika endgame build-out (canonical)

**Canonical plan, 2026-11-06. Supersedes scattered roadmaps for execution
purposes (they remain reference). Owner order: wire it up, test it,
50 tracked todos, realistic goals in logical order, process notes kept.**

## Goal (one line)

One question about a Trika text walks down to a witness and back up to a
signed, DOI'd essay — or a lesson, or a practice — with every link
hash-pinned, decision-tracked, gate-checked, and machine-verified where
machines can verify. Commodity generation; scarce provenance.

## Architecture (the spine + the geometry)

```
witness → chunk → layers → formal → arguments → treeka → essay → teacher/agents/practice
   (openpatala) (translation-work) (formal-trika Lean) (pushing) (Scholar) (satsang/deitybody/nibbanahelp)
```

Formalisation is the proof-carrying **spine** (peer review → teacher →
practice hang off checked models). The Mālinī phonemic-body frontier is
the **geometry engine** it grows into (50 phonemes × loci × Śaktis × 5
maps = the first comparative-formal rung + visual truth).

## Realistic goals (what "done" means per track)

| Track | Done means | Blocked on (not us) |
|---|---|---|
| A openpatala | Queryable populated DB on box; edition pins honest; restore recipe | Witness verification (manuscript eyes) |
| B chunks/layers | 87/87 source records; nodes index; treeka assembler + gaps live | Ingest-side decision writes (other lane) |
| C formal | Coverage climbing per rung (prereg-first); blind pilot run; second keys; applications rung designed | Scholar review (P-TK1), owner decode review (ti/ca), rater-2 (T-C2) |
| D essays | PUSHBACK CLI live-capable; chain integration tested; Zenodo dry-run ready | Model quota (live runs), owner token (Zenodo), worker lane (staleness) |
| E teaching/practice | C1 unit rendered; eligibility gate; paths; day-gate; body-map check; gaps listed | Owner sit-player flip, dīkṣā policy calls |
| F bench | Calibration + sweep + thresholds on CPU; tau when quota allows | Model quota (tau), GPU (COMET/LoRA) |
| G geometry | Schema + readiness + comparison scaffold + reconstruction inventory | E-text fetch rights, translator lane |
| H patala corpus+biblio | Atlas seeds fed into box DB (people/translations/editions live); bibliography referenced not forked; M-index new | Scholar channel (KMT file, NGMPP reels), translator lane (formal stage) |

## Logical order (why this sequence)

1. **A first** — identity grounds everything downstream (no witness work
   without a queryable store).
2. **B second** — nodes + treeka turn the estate from files into a graph
   the rest can query.
3. **C third** — rungs in queue order (heaps → blind → sweep → keys),
   prereg-first always.
4. **F alongside** — CPU calibration needs no one; quota work piles up
   for one funded session.
5. **D fourth** — PUSHBACK/chain/zENODO consume B+C outputs.
6. **E fifth** — practice compiles from D outputs + body truth.
7. **G last** — frontier consumes the whole machine (first customer).
8. **H continuous** — corpus feeds (atlas seeds, M-files, GRETIL) flow
   into the box DB as they land; bibliography grows by reference.
   One system: patalacheckpoints seeds, box DB serves, lanes consume.

## Rules (never violated)

- Prereg before code; corrections are new dated files, history never edited.
- Machine proposes, human disposes. No auto-sign, no auto-publish.
- Tiers on every claim (T/R/E/C/H/X). R never promotes itself.
- Fail-closed: timeouts/blocks/empties are ERRORS, never passes.
- No rung ships without hash + grounds + gate + role.
- Only `decide` proves (inside its finite scope). Heuristic PASS ≠ proof.
- Lanes respected: translation-work ingest + ipvv worker/scholar deploy
  are other lanes — read-only + specs + CLAIMS notes from here.
- Process notes appended same session (this file's companion
  PROCESS-NOTES-*.md). No silent work.

## Scoreboard (2026-11-06 close of autonomous build; verified at push)

- Formal: 107 theorems / 19 refusing mutants / control 11 PASS /
  recognition 26/26 / axiom 107 CLEAN (77 zero-axiom) / TABLE all rows.
- Evidence: 105 entries + 2 exemptions, 0 problems; coverage 8/45 chunks
  (tsa08 full + tsa07-p01 + 6 param/phr/vbt/span stations).
- Treeka: 909 passages keyed; gaps unargued=659, cruxless=70,
  essayless=250, unformalized=864; 13 ambiguous locators recorded.
- DB: postgres live, 444 works / 442 assertions / 121 ext-ids, idempotent
  loader, recipe in bridge README.
- Bench: thresholds/1 NEEDS TUNING (logged); tau pilots logged (null-ish);
  round-trip prototype (uncalibrated); F3 refused by design.
- Practice: C1 unit + eligibility + paths (no-DIY asserted) + day-gate +
  bodymap drift-clean + slang pack + unit→syllabus→score plug PROVEN.
- Live model rails: beam-free ($0, go_beam.py) + CF REST (neurons logged);
  ox-alpha quota untouched; PUSHBACK live on both.
- Pushes: trika-x b730c6d-era → current; svread source-map; ipvv acom/0.2.
- Disk 3.5G free; secrets /root/.env ONLY, repo scans clean.
- Human-gated remainder: witnesses, P-TK1/ti-ca/rater-2, Zenodo token,
  tau-scale, Mutate remainder, F3 pairs, dīkṣā policy, owner flips
  (ledger/trajectory/vis-mode, sit player, catalog migration).

---

## AMENDMENT 2026-11-08 — measured progress since the 11-06 baseline

> **Note (same day, later):** the figures in this amendment were taken at
> ~11:00. Later same-day work raised them (157 theorems, 16/154 chunks, 909
> traces, 94 tests, 95%/3.9G disk). Current numbers live in
> `formal-trika/data/freshness.json` and `MASTERPLAN2.md`; this section is a
> dated snapshot, not a live scoreboard.

*Appended, not rewritten. The 11-06 plan above stands as architecture and
order; this section updates the scoreboard only. Full audit:
`docs/log/REVIEW-2026-11-08.md`. Execution plan: `MASTERPLAN2.md`.*

### What changed (verified on box 2026-11-08)

| Track | 11-06 claim | 11-08 measured | Verdict |
|---|---|---|---|
| A openpatala | 444 works | **555 works / 909 passages / 0 witnesses**; `check.py` GREEN with 2 recorded BLOCKED (conformance: adapters discover nothing; witnesses: 0) | real, honestly gated |
| A identity | — | Abhinavagupta corpus seeded (7 LOST + 4 ATTESTED-UNVERIFIED, reported-status only); 101 ours-translations registered (71 gold-proposed / 30 pending); 122 translation rows | real, human review pending |
| B chunks/layers | 28 works / 154 IDs bridged | unchanged **28 / 154 BYTES_MATCH, witnesses UNPINNED**; `source-map.json` 87 works, **6 bridged / 81 todo** | bridge solid, coverage thin |
| C formal | 107 theorems / 19 mutants | **153 theorems / 151 entries + 2 exemptions**, 0 bad chunk refs, axiom CLEAN (static half); 73 tests green | climbing |
| C coverage | 8/45 chunks | **13/154 passage chunks (8%)**; gap list published | honest, low |
| C traces | — | **13 trace bundles** (12 COMPLETE / 1 PARTIAL with caveat), external verify pack live (curl+sha256 proven) | new, real |
| D essays | PUSHBACK mock | `formal-trika/tools/pushback.py` live (mock/go/cf, opt-in, verbatim shield); Zenodo dry-run only | PUSHBACK done, DOI gated |
| E teaching/practice | C1 unit | Sanskrit surface BUILT + preview-deployed: 10 lessons verbatim, fish recitation rail, lesson/lore-aware chat, `?view=verify` | new, live |
| F bench | tau null-ish | unchanged — tau scale still quota-blocked; CPU calibration ready | blocked on quota |
| H corpus/biblio | seeds | bibliography = DB view; atlas/Abhinavagupta seeds in box DB; refs not fork | real |
| Surface | — | svread live: 50 readable / 55 projections / 504 assets; llms.txt + sitemap + robots + JSON-LD measured, enforced by wiring test | real |

### New standing facts

1. **Checkability is live.** `svread/tools/emit_verify.py` publishes exact
   bytes per chunk; an outsider reproduces every hash with `curl` +
   `sha256sum`, no project code. This is now the moat line.
2. **Honesty gate replaced headline gates.** openpatala `check.py` reports
   PASS/FAIL/BLOCKED; BLOCKED ≠ PASS. Old README counts (1099/247/2181) are
   stale — canonical counts are the box DB and the evidence bundle.
3. **Federation exists.** `federation_gateway.py` multiplexes 98 tools across
   openpatala/formal/scholar/translation/bookfactory/video; PARENT-CONTRACT and
   FORMAL-MCP specs frozen; 8 gateway tests green.
4. **Layer names for callers.** `layer-names.json` maps internal codes to
   public slugs (literal-gloss, argument-map, …); callers never see `l0`.
5. **Docs are now measurable.** MODULES.md (every repo + gate), ROADMAP.md
   (five rungs with done-gates), docs/log/REVIEW-2026-11-08.md (staleness register).

### Corrected open items (supersede 11-06 wording)

- Variety 1 = **PUSHBACK done; Zenodo token still the only gate** (was
  "PUSHBACK + token pending").
- Formal rungs = work the **published gap list** (phr-p05 head → VBT
  clusters → tsa08 remainder); next prereg already exists
  (`PREREGISTRATION-PHR-RUNG.md`).
- Witnesses = still **0 corpus-wide**; WITNESS-OCR is a proposal doc, not a
  wired pipeline. NGMPP eyes remain the only path.
- Hygiene = disk **98% (1.7G)**, branch `box/peer-review-batch` dirty,
  nightly cron still not installed (owner call), R2/Go rotation unconfirmed.

### Rule reaffirmed for the next agent

Only the 11-07/11-08 measured docs are canonical for numbers. Anything older
that quotes a count is reference, not evidence. Never re-quote a headline
without `bytes + hash + where to re-fetch`.
