# TABLE-READINGS — hand-written plain-English readings, one per theorem

Format: `## file :: theorem` then one reading paragraph. `tools/table.py`
joins these with the sources into TABLE.md (GENERATED, never hand-edited)
and `--check` fails if any theorem lacks a reading or any reading's theorem
vanished. Write for the blind reader (BLIND.md): what the theorem SAYS,
never why it matters. Scaffolding lemmas marked `[scaffold]`.

## Mala.lean :: count_3
KEY: the tradition counts three malas. Nothing is derived; the list is the claim.

## Pramatr.lean :: eight_combos
Three binary axes make 2^3 = 8 combinations. Arithmetic, not doctrine.

## Pramatr.lean :: seven
Exactly one combination is ill-formed (kārma floating free of both āṇava and māyīya), leaving 7 well-formed rows. The single general rule R1 does all the work.

## Pramatr.lean :: profile
The seven rows carry mala-counts [2,3,1,2,1,2,0] in generation order. An observed shape of this encoding, not a traditional figure.

## Kancuka.lean :: count_5
KEY: the tradition counts five coverings.

## Kancuka.lean :: pairings_distinct
The five hand-set coverings map onto five distinct capacities. Checks the table's non-redundancy, not its truth (the pairings are R-tier gloss).

## Recognition.lean :: recognition_preserves_content
The σ-flip changes no content bits on any of the 64 states.

## Recognition.lean :: recognition_lands_recognized
The σ-flip lands every state in ¬Sv(O).

## Recognition.lean :: recognition_adds_nothing
Content before and after the flip is equal on all states. Removal, not addition.

## AnswerKey.lean :: key_five_kancukas
KEY: five kañcuka names. Tradition's count.

## AnswerKey.lean :: key_thirtysix_tattvas
KEY: thirty-six principles (tsa07-p01 ladder).

## AnswerKey.lean :: key_seven_experients
KEY: seven experients (paramarthasara scheme + tsa08-p03 ladder). The count, not the mapping.

## AnswerKey.lean :: key_five_followers
KEY: five pure-course followers (v17, read this session).

## AnswerKey.lean :: key_hundred_twelve_dharanas
KEY: 112 dhāraṇās (VBT vv24-135 per the lore file).

## Transitions.lean :: trec_preserves_embodiment
De-exclusivizing the 7 positioning bits never touches the 5 embodiment bits, on all 4096 states.

## Transitions.lean :: trec_clears_bondage
After T_rec, bondage (limitation + exhaustive-identification + externalization) holds nowhere.

## Transitions.lean :: trec_retains_limitation
Limitation survives recognition on every state: no destruction of embodiment.

## Transitions.lean :: trec_idempotent
Recognized stays recognized: applying T_rec twice is once. No backslide in the model.

## Transitions.lean :: anava_stuck_exists
Stuck states (exhaustive-identification + bondage) exist in the model. The āṇava pathology, exhibited.

## Transitions.lean :: acquire_is_not_recognition
On every state, acquisition rewrites embodiment while recognition preserves it: learning is provably not recognition here.

## Transitions.lean :: karma_loop_exists
Fully positionally-exclusive pre-recognition states exist. The kārma self-loop, exhibited.

## NonEntail.lean :: aby_not_b
There is a chain-position with A (self-manifest) but without B (first-personality). The first arrow is missing in the model.

## NonEntail.lean :: b_not_c
Ownership without persistence exists in the model.

## NonEntail.lean :: c_not_d
Persisting ownership without one enduring subject exists in the model.

## NonEntail.lean :: d_not_e
One enduring subject without genuine freedom exists in the model.

## NonEntail.lean :: e_not_f
Genuine freedom without one universal consciousness exists in the model.

## NonEntail.lean :: abcde_without_f
The full A–E path without F exists: no earlier contention smuggles the last conclusion.

## NonEntail.lean :: vim7_independent
All 128 combinations of the seven vimarśas occur: their unity is not given in the model.

## NonEntail.lean :: copresence_nontransitive
Co-presence on three points need not transit: U(0,1) and U(1,2) hold while U(0,2) fails.

## NonEntail.lean :: no_global_section
No Boolean triple is pairwise-equal yet jointly-unequal: local coherence does not compose into a global section. (A no-go shape, not a sheaf theorem.)

## NonEntail.lean :: pairwise_satisfiable_xy
Pairwise equality is satisfiable: the no-global-section is about triples, not pairs.

## Conjuncts.lean :: recognition_unique
Exactly 1 of 16 transformation/reidentification/veridicality/stabilization combinations is recognition.

## Conjuncts.lean :: drop_transformation_loses
Without transformation, the remaining three conjuncts never constitute recognition.

## Conjuncts.lean :: drop_reidentification_loses
Without reidentification ("this is that"), no recognition.

## Conjuncts.lean :: drop_veridicality_loses
Without veridicality, no recognition: the load-bearing conjunct.

## Conjuncts.lean :: drop_stabilization_loses
Without stabilization, no recognition.

## Conjuncts.lean :: misidentification_never_recognizes
Identifying a as b when a≠b never counts, however certain. Certainty ≠ recognition.

## Conjuncts.lean :: part_coherent_distinct_tokens
Shared ground with genuinely distinct tokens exists in the model: the participatory reading is coherent.

## Conjuncts.lean :: pi_independent_of_grounds
Token-aperture identity decides nothing about grounds: different types of claim.

## Conjuncts.lean :: siva_requires_axioms
Part without the first Śaiva axiom is never the full recognition.

## Conjuncts.lean :: unus_ambu_not_identity
A symmetric non-identity bond exists (mutual relatedness without numerical identity): 1×1 is not 1=1.

## Memory.lean :: m4_requires_foundation
No well-formed autonoetic memory floats free of retention, continuity, and attribution.

## Memory.lean :: foundations_without_m4_exist
Retention+continuity+attribution can hold without autonoetic memory: foundation without the house.

## Memory.lean :: m4_without_m5
Autonoetic memory without identity-ownership exists: M4 does not entail M5.

## Memory.lean :: sees_without_enacting
Seeing deception without enacting its removal exists (the stream-enterer shape).

## Memory.lean :: no_enacting_without_seeing
Enacting removal without seeing is ill-formed: no removal without seeing.

## Tractatus.lean :: every_context_supported
Each of the two contexts has a support-set.

## Tractatus.lean :: no_universal_support
No single support serves both contexts: support is local. (The ∀D∃Σ ⊭ ∃S∀D shape, finite witness.)

## Tractatus.lean :: rec1_without_rec2
Knowing-without-self-inclusion exists: Rec_1 does not entail Rec_2.

## Tractatus.lean :: rec2_without_fullrec
Knowing one's dependence without ceasing to reify exists: Rec_2 does not entail FullRec.

## Tractatus.lean :: finite_missing
[scaffold] Two values of Fin 4 never cover Fin 4: some fourth value differs from both.

## Tractatus.lean :: fin_two
[scaffold] Every Fin 2 value is 0 or 1. Case-split fuel for the no-self-model proof.

## Tractatus.lean :: no_total_self_model
Every map from a 2-state model to a 4-state observer misses a state. A finite shadow of the no-total-self-model claim, not the philosophical thesis.

## Tractatus.lean :: bit_content_relational
0 means not-1 and 1 means not-0: the bit's whole content is relational. (S itself untouched — H.)

## Tractatus.lean :: suffering_reachable
From manifestation, the suffering terminal is reachable in ≤5 steps: the appropriation path exists.

## Tractatus.lean :: recognition_reachable
From manifestation, the recognition terminal is reachable in ≤5 steps: the reflexive path exists.

## Tractatus.lean :: recognition_needs_reflexive_edge
Without the reflexive edge, recognition is unreachable from manifestation: the edge, not the chain, is load-bearing.

## Coords.lean :: coords_covered_once
The five kañcukas cover the five coordinates exactly once each: contraction is total and non-redundant (as mapped).

## Coords.lean :: restricted_perspective_exists
A restricted perspective (particular knower) exists in the model.

## Coords.lean :: no_unrestricted_perspective
Among admitted states, no perspective floats free of restriction. (Premise-relative, not a metaphysical proof.)

## Coords.lean :: one_raw_invalid_combination
Exactly one of the four raw perspective/restriction combinations is excluded by the wellformedness premise.

## KancukaCorr.lean :: corr_pull_raga
KEY ROW: the pull marker maps to the value coordinate (rāga). Stipulated + evidence-pinned, not derived.

## KancukaCorr.lean :: corr_stall_kala
KEY ROW: the stall marker maps to the action coordinate (kalā). Stipulated + evidence-pinned.

## KancukaCorr.lean :: corr_doubt_vidya
KEY ROW (R): the doubt-stammer maps to the epistemic coordinate (vidyā). Thinnest firm row.

## KancukaCorr.lean :: unknowns_explicit
Push, urgency, and placedness map to nothing: the unknowns are recorded, not forced.

## KancukaCorr.lean :: coverage_partial
Only 3 of 5 coordinates are hit by the map. Full coverage is NOT established here.

## Grace.lean :: readiness_insufficient
No ready-without-grace state flips: readiness alone never suffices in the model.

## Grace.lean :: grace_insufficient_alone
No graced-but-unready state flips: no bypass in the model.

## Grace.lean :: flip_iff_ready_and_grace
Over all 4 states, flip holds exactly where readiness and grace both hold. Represents the report structure, not grace's existence.

## Grace.lean :: both_gaps_exist
Both gaps are inhabited: ready-unflipped and graced-unflipped states exist.

## Upaya.lean :: sambhava_immediate
Śāmbhava reaches from every ready state: immediacy, no preconditions beyond readiness.

## Upaya.lean :: sakta_needs_purity
A ready-but-impure state exists that śāmbhava reaches and śākta does not: purity is load-bearing.

## Upaya.lean :: anava_needs_repetition
One application never suffices, even ready: repetition is load-bearing.

## Upaya.lean :: anava_two_suffice
Two applications suffice wherever readiness holds: the bound on repetition.

## Upaya.lean :: anava_within_sambhava
Whatever āṇava reaches in 2 steps, śāmbhava reaches: ordering recorded as found.

## Upaya.lean :: sakta_within_sambhava
Whatever śākta reaches, śāmbhava reaches: ordering recorded as found.

## Tattva.lean :: five_gross_elements
The 10× magnitude ladder yields exactly five gross elements.

## Tattva.lean :: eleven_wombed
Eleven faculties: five cognitive + five action + mind (7.9 akṣa-ekādaśa reading; corrected from subtle+gross+mind — see source review).

## Tattva.lean :: thirty_six
The ten group-size clauses generate thirty-six principles in total, matching the tradition's count.

## Tattva.lean :: all_groups_present
All ten groups are accounted for exactly once: no orphan, no double-count.

## Tattva.lean :: compression_ratio
The file defines ten groups: the clause count behind the 10/36 compression ratio (computed in RESULTS.md, not proved here).

## EgoOrigin.lean :: sankhya_requires_cause
Every Sāṅkhya-admitted ego-state carries a derivative cause.

## EgoOrigin.lean :: trika_self_grounding_exists
The pure-I state (no cause, with I-feeling and makership, non-rivalled) is admitted: self-reflexive ego is consistent in the model.

## EgoOrigin.lean :: accounts_differ_pureI
The pure-I state is Trika-admitted but not Sāṅkhya-admitted.

## EgoOrigin.lean :: accounts_differ_derivative
A derivative state is Sāṅkhya-admitted but not Trika-admitted: neither admission contains the other.

## EgoOrigin.lean :: nonrivalled_does_work
Every Trika-admitted state is rival-free: the "non-rivalled" clause excludes states, it is not decorative.

## EgoOrigin.lean :: feeling_makership_independent
I-feeling without makership occurs in the model: the two bits are separable here (a model fact, not a textual claim).

## Recognition.lean :: contentEq_sharp
A pair differing in exactly one content field is not content-equal: the equality discriminates.

## AnswerKey.lean :: key_grace_term
KEY: the śaktipāta term is attested (pins the v35 quote to the machine surface).

## Heaps.lean :: heap_has_both_kinds
The heap holds five sense and five action faculties: both kinds present.

## Heaps.lean :: heap_eleven
The heap totals eleven instruments (5+5+1, ladder-consistent).

## Heaps.lean :: guna_threefold
The nature-heap admits exactly three guṇas.

## Heaps.lean :: guna_exhaustive
Each guṇa tags exactly one nature-state: no untagged, none double-tagged.

## Avarana.lean :: course_ascends
Every cross-course adjacent pair strictly ascends in course rank: the covering principle holds where courses differ.

## Avarana.lean :: partial_order_honest
An intra-course adjacent pair exists: within-course order is undetermined, exhibited not forced.

## Application.lean :: unready_unreachable
No flip and no means-reach without readiness: the study-fallback, backed across both models.

## Application.lean :: grace_not_a_means
A graced-but-unready state does not flip: grace is conjunctive with readiness, not a substitute means.

## MalaFuel.lean :: fuel_terminates
Three burn steps from all-unburned reach all-burnt: burning ends.

## MalaFuel.lean :: strength_monotone
Burnt-count never decreases along a burn step: strength is monotone.

## MalaFuel.lean :: grace_ignites
Nothing burns without knowing: ignition needs grace.

## Pratyahara.lean :: ac_vowels
The a-to-C interval is exactly the nine vowels: a generative label for the vowel class.

## Pratyahara.lean :: hal_consonants
The ha-to-L interval holds 34 consonants once markers are excluded.

## Pratyahara.lean :: markers_excluded
No meta-marker belongs to any pratyāhāra: markers mark, never sound.

## Pratyahara.lean :: inventory_43
The sequence carries 43 speech sounds in total.

## Pratyahara.lean :: markers_13
Thirteen distinct marker kinds (Ṇ twice): the meta-alphabet beside the sounds.

## Reversal.lean :: semi_reversed
The page's semivowel order is exactly the alphabet's reversed: va-la-ra-ya mirrors ya-ra-la-va.

## Reversal.lean :: span_reversed
The page's 25-letter span is exactly alphabet ka-to-ma reversed: labials-to-gutturals mirrors gutturals-to-labials.

## TattvaInventory.lean :: named_tattvas_36
Candidate enumeration: 36 named tattvas in conventional descending order (five pure, māyā, five covers, puruṣa, nature, instruments, senses, subtles, gross).

## TattvaInventory.lean :: named_tattvas_unique
No duplicates in the 36-name list.

## TattvaInventory.lean :: named_tattvas_exhaustive
Every constructor of the inventory type appears in the list: the enumeration is complete over its own type.

## TattvaInventory.lean :: pure_count
Five pure principles (māyā and Ananta excluded).

## TattvaInventory.lean :: kancuka_count
Five coverings (kalā included).

## TattvaInventory.lean :: maya_six_count
Māyā plus the five: the six-cover reckoning counts six.

## TattvaInventory.lean :: pure_excludes_maya
Māyā is not among the pure five (placing it there is refused).

## TattvaInventory.lean :: pure_and_kancukas_disjoint
Pure five and coverings five share no member.

## Nyasa.lean :: ka_uniform
Ka-varga shares one Mālinī locus (teeth): the single uniform varga, observed not derived.

## Nyasa.lean :: matrika_total
Fifty distinct phonemes placed in the mātṛkā map: totality.

## Nyasa.lean :: malini_total
Fifty distinct phonemes placed in the Mālinī map: totality.

## Nyasa.lean :: maps_diverge
All fifty loci differ across the two maps: the duality quantified.

## Nyasa.lean :: order_chief
The nādiphānta order differs from śabdarāśi: the chief sequence stands apart.

## Nyasa.lean :: multiset_kept
Both orders hold the same fifty phonemes: conservation.

## Embed.lean :: earth_all5
Earth holds all five subtle substances: the grossest contains all.

## Embed.lean :: ether_sound_only
Ether holds sound alone: the finest contains one.

## Embed.lean :: nesting
Finer substances persist upward: each grosser row includes the next finer.

## Ladder.lean :: chain_trans
Chained resorts compose: leaving rung after rung lands inside the ladder's reach.

## Ladder.lean :: terminal_no_successor
The last means has no next rung: means-independence ends the ladder.

## Ladder.lean :: abandon_strict
Every resort climbs exactly one rung: no leaps, no loops, no staying put.

## TattvaGen.lean :: gen_total
Thirty-six computed from rules: five primacies, five limits, root, dyad, triad, four pentads of five.

## TattvaGen.lean :: pure_distinct
The five primacy powers are pairwise distinct: no collapsed principle.

## TattvaGen.lean :: pentad_uniform
Every modality holds exactly five: uniform derivation, no 6/4 split.

## TattvaGen.lean :: cut_arith
Thirty-one manifest as thirty-six minus five: the cut counts check.
