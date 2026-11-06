# G1 — phonemic-body mapping spec (formal; seed key identified)

**Date:** 2026-11-06. This spec turns BRAINSTORM Idea 1 (nyāsa rung)
into a buildable rung. No Lean yet (prereg first, per discipline).

## Relation (from TRANSLATION_FRONTIER doc §"extra schema", adopted verbatim shape)

```json
{"relation_type": "phonemic_body_mapping", "passage": "<chunk:verse>",
 "phoneme": "<iast>", "sequence": "malini|shabdarashi",
 "body_locus": "<locus>", "shakti": "<name|null>",
 "iconography": {"colour": null, "arms": null, "attributes": []},
 "geometry": null, "pitha": null,
 "source_status": "explicit|apparatus|reconstructed",
 "confidence": "high|med|low"}
```

## Seed KEY DATA (found, peer-reviewed, frozen — this session)

`sanskrithelp/public/memory/data/matrika_body_map.json`
(sha-pinned via bodymap_check.py; mirrors byte-identical):
16 vowels (iast/devanāgarī/locus/group + TĀ 15.117–118 spans) + 7 vargas
(ka/ṭa/pavarga/nava…, per-phoneme loci + TĀ 15.118 spans) + apparatus
variants per entry (NEVER used for install) + `ta_15_aṅganyāsa_crosswalk`
(a SECOND map — the independent key!) + claims_policy
(practice_scaffold_not_medical) + canonical/frozen 2026-10-06 with
2026-10-05 peer review on record.

## Rung design (for the prereg)

- Alphabet: 50 phonemes (16 + varga members). Loci from the map.
- General rules (R): varga→limb (ONE rule per varga, e.g. ka-varga →
  right upper limb, 5 rows each); vowels→head-16; direction duality
  (sṛṣṭi/saṃhāra both installable, TĀ-15 units); nādiphānta order chief
  among mixings (TĀ-15 ~102).
- Three-nyāsa character (nibbanahelp trika/ta15_nyasa, TĀ 15/115cd–145):
  Mātṛkā = feminine, alphabetical order; Mālinī = feminine, seeds
  (vowels/bīja) mixed with matrices (consonants/yoni) — cf. MV 3.36
  bhinna-yoni verbatim; śabdarāśi = male, Assembly of Sounds, fifty
  Bhairavas. The pair/triple structure constrains the permutation rung
  (Idea 2): same 50, typed orders, yugapad coexistence.
- ORDER key (verified 2026-11-06): MV 3.36–41 (MIRI M00160, CC BY-NC) —
  na→pha with loci; TĀ-15 GRETIL text same skeleton, 5 reading variants
  logged (data/mv3-malini-vv36-41.json). malini_order.json == MV order.
- Theorems: totality (50/50 placed), varga-uniformity (same varga →
  same limb), crosswalk agreement (map vs crosswalk: SAME loci where
  both speak — second key!), chief-order (nādiphānta ≠ śabdarāśi order,
  same multiset).
- Mutants: drop a varga rule (uniformity refuses); swap two loci
  (totality holds, uniformity refuses — surgical); collapse crosswalk
  (agreement refuses).
- Kill: twin checks; T-contradiction (GRETIL variants in apparatus —
  apparatus readings NEVER override verse-literal; a verse-literal
  contradiction kills the rule, an apparatus-only one is recorded).
- Scope: installation MAPPING only (no siddhi/fruit claims, no medical
  claims per claims_policy, no mātṛ-future metaphysics).

## Feeds

Visualizations (verified rules → body pages), G3 five-maps diff (rule-set
diff), G4 Triśirobhairava (constraint check: which map's rules generate
the quoted fragment?).
