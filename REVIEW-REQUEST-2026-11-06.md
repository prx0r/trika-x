# REVIEW REQUEST — lead agent peer review (2026-11-06 evening)

**Scope:** 22 commits since `1862bca` (last reviewed merge) to main tip —
the full autonomous session. PR diff = context; THIS file is the ask.
Everything below is what I am unsure about or suspect is flawed. No
defense offered; dispose freely.

## Method flaws (need your ruling)

1. **Tiers are self-asserted.** Nothing mechanical checks tier semantics;
   evidence_check verifies references exist, not that T means T. My two
   mis-tierings were caught by live-model luck, not by a gate. Question:
   tier-gate (e.g. T requires span-sha + reviewed-translation + signoff,
   machine-enforced), or is reviewer-eyes the gate by design?
2. **Twin surgicality is self-judged.** must_fail enforces exactly-one
   refusal, but whether a twin is meaningful vs gamed is my own call
   (same encoder designs and judges). The cycle-twin rejection was mine
   too. Question: second-encoder twin review, or accept designer-judges?
3. **`cut_arith` may not belong in EVIDENCE.** (5+1+2+3+20)=31 is
   arithmetic, not Trika. Kept as model-only partition check. Question:
   keep as honest arithmetic, or drop as noise that inflates counts?
4. **`--promote` trusts a string.** Anyone can pass `--reviewer NAME`.
   No cryptographic or lane-verified identity behind Core promotion.
   Question: tie promotion to signoff IDs (Scholar) or accept for now
   (0 Core today, so nothing is actually promoted)?
5. **Roboscholar nondeterminism.** Receipts pin prompt_sha but not seed/
   temperature; reruns vary. Question: pin temperature 0 + record model
   version, or is receipt-per-run sufficient?

## Open design questions

6. **Agreement receipt-only.** TattvaGen vs listed Tattva totals agree
   (both 36) but no CI enforces it (kept out for twin-separability).
   Right trade-off, or enforce and restructure twins?
7. **Trinity serving two masters.** Snapshot/bridge/EVIDENCE sets must
   match; I add works for formal convenience (tal-a34 for one entry).
   Fine mechanically — conceptually drifting? Split formal registry from
   bridge snapshot?
8. **E-EMB uniform alternative parked.** Gradient reading flagged R with
   remodel-ready kill. Still owed scholar confirmation (packet item).
9. **Nyasa follow-ups.** Varga second key + order twin outstanding.
10. **MITRA share-alike scope.** CC BY-SA slice feeds L0 grounds — fine
    for citations, but bulk derivation boundaries need a rights ruling
    (scholar lane?).
11. **Vidyut normalization.** Allow-list strips sandhi-critical marks;
    2/4 honest aligns. Sandhi-module follow-up is the real step —
    approve direction?
12. **Nightly skips Lean.** Battery covers evidence/table/bridge/tests,
    not run.sh (time). Partial coverage recorded — extend or accept?
13. **Disk 96%.** Every addition worsens it. Cleanup priorities wanted.
14. **Swarm skills uncalibrated.** swarm-formal + roboscholar run, but the
    Embed re-derivation benchmark (scale-only-what-passes) is still owed.
15. **Formal-refs grammar.** Theorem IDs in lingua/submissions need a
    cross-lane grammar decision (`theorem:<file>:<name>`?) — propose text?
16. **Independence gap stands.** No second key on disk; Dyczkowski
    collation + KMT filename both need the scholar channel (packet B9).

## Resolved since (for the record, not review)

- TW PRs #9–12 MERGED by their agent (provenance, formal stage, submission
  identity, MITRA grounds). Svread lingua PR still open.
- Family-2 replication closed (Mistral+Qwen exact). Blind vocab decision
  still lead's.
- a18 rung paused at prereg (batch moved to swarm pipeline).

## Roundup of everything awaiting review (all lanes)

| PR | Content | State |
|---|---|---|
| TW #9 | Zenodo provenance IDs | MERGED |
| TW #10 | Formal stage proposal | MERGED |
| TW #11 | Submission identity | MERGED |
| TW #12 | MITRA L0 grounds | MERGED |
| svread #9 | Lingua openpatala block | OPEN |
| trika-x (this) | 22-commit session + this packet | OPEN |
