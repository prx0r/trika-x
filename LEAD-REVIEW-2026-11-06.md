# Lead review — PR #5, 2026-11-06

Reviewed against `review-base-1862bca`, with svread PR #9 reviewed separately.
The PR is an extensive research checkpoint, not yet an independently verified
formalisation, a publication gate or an authorised teaching system.

## Findings and dispositions

1. **The containment source was misattributed.** Tantrasāra 7.9 places five
   subtle elements and eleven faculties in ahaṃkāra; it does not directly
   state the proposed gross-element matrix. 8.85–90 discusses earlier
   qualities and another account. The registry now points to that latter
   passage as an *unreviewed reconstruction*, not a textual proof; the
   original preregistration and historical run remain unchanged. Source:
   [GRETIL Tantrasāra](https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_abhinavagupta-tantrasAra.htm),
   §§7.9, 8.85–90 (electronic prose locators).
2. **An essay compiler could invent proof status.** `--theorems` accepted any
   text and labelled it T/decide-verified. Verse selections were not bound to
   the requested chunk, and node inputs were not rechecked. The compiler now
   requires a matching registry association, verifies selected node and
   ledger bytes, rejects missing/ambiguous/wrong-chunk inputs, and labels
   theorem references as unverified. A registry link still proves neither a
   Lean run nor a source-to-model interpretation. Earlier generated
   `expansion-mala-objectivity-*` drafts and receipts are historical: their
   T/decide-verified labels are **not evidence** of a verified run or textual
   entailment. The graph's theorem nodes are marked unverified.
3. **The review-status check was not a gate.** It filled missing rows in
   memory before checking, and a user-entered reviewer name could promote a
   theorem to Core. Check mode now fails on missing/stale/invalid entries;
   Core promotion is disabled until an authenticated decision tied to exact
   source, model and version can be checked. Names and local JSON alone do
   not prove identity or review.
4. **The expanded source snapshot broke CI.** It contains 28 works, whereas
   CI checked out six from an older revision; the report also hard-coded the
   old six work names. CI now pins the snapshot revision and all 28 works;
   the report reads validated ledger paths from the registry and treats
   repeated bare locators as ambiguous instead of cross-linking them.
5. **Nightly verification masked failures.** Its final result was only the
   last database command's status. Required checks now contribute to the
   exit code; database and Lean skips are explicit. GitHub CI runs Lean;
   this nightly script does not claim to do so.
6. **External model calls and run receipts.** Roboscholar now requires
   explicit opt-in before sending selected argmap text to a provider. Its
   model alias and prompt hash still do not pin a provider build, seed,
   generation parameters or exact response. Existing receipts are records
   of particular outputs, not reproducibility or independent review.

## Rulings on the open method questions

- Treat tier labels as claims requiring independently reviewable evidence;
  checking that a locator exists cannot determine whether a passage entails
  a model. Keep machine-generated material at candidate/reconstruction
  status until authenticated scholarly decisions exist.
- A failing mutant shows sensitivity to a selected perturbation, not that it
  is a meaningful or independent test. A second qualified reviewer should
  assess the positive-to-mutant change and the source interpretation.
- Keep `cut_arith` as an explicitly model-only arithmetic check; do not count
  it as Sanskrit coverage. The generated and listed 36 should eventually
  agree by an independently reviewed member-by-member correspondence, not
  just a matching total. Keep positive-model agreement tests separate from
  negative controls so mutants remain informative.
- Keep the formal registry and passage snapshot distinct: one records
  candidate associations; the other pins source-ledger identities. Neither
  certifies witnesses or justifies adding a work solely to improve coverage.
- Mātr̥kā/nyāsa maps, the E-EMB alternative, and independent textual keys
  remain open for scholarly review. Multiple model replies to a common
  prompt are not independent human evidence.
- MITRA's share-alike terms, the GRETIL e-text's noncommercial terms, and
  rights in individual witnesses/editions require source-specific review
  before redistribution or commercial use. Vidyut outputs are candidates,
  not a sandhi or textual authority.
- A future cross-repository theorem reference should identify the repository,
  commit, relative file and fully qualified declaration; independently bind
  the toolchain/run receipt, source span, interpretation and review decision.
  Do not promote the current free-form `theorem:File :: name` to that role.
- The reported disk pressure needs inspection on the machine concerned; do
  not delete shared checkouts or another agent's work to satisfy this PR.

CI/source checks use pinned bytes. Missing witnesses, rights, authenticated
review, model version provenance and independent scholarly assessment remain
open even if the checks pass.
