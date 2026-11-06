# NEXT STEPS — sequenced backlog from here (canonical)

**Order logic:** hygiene/autonomy first (nothing rots), coverage second
(formal rungs in queue order), integrations third (other lanes decide),
scale last (quota/GPU/humans). Each item: gate that marks it done +
who/what blocks it. Prereg-before-code and tiers apply to all formal work.

## Phase 1 — Autonomy + hygiene (all autonomous, now)

| # | Step | Done when | Notes |
|---|---|---|---|
| 1.1 | Enable nightly verify cron | log shows 7 green days | script ready at /tmp/nightly-verify.sh → move to trika-x/tools, owner enables (writes cron = owner call) |
| 1.2 | Blind vocab transition indices | vocab.py covers Nat params; --check green; āṇava re-derived blind | resolves recorded VOCAB-GAP (lead-agent decision noted) |
| 1.3 | Mutate remainder (9 files) | sweep + triage logged | needs 4.33.1 transient (~2.9G; check df); resume cmd in process notes |
| 1.4 | EVIDENCE/TABLE/run.sh discipline tests | CI fails on missing entry/reading/harness line | meta-tests: every theorem has all three (evidence_check does 1/3 today) |
| 1.5 | R2 DB backup routine | schema dump (migrations bundle) + seed JSON hashes logged monthly | PG18 dump unreadable on PG15 — bundle migrations+seeds instead (recipe exists) |
| 1.6 | Rotate pasted tokens (R2 + confirm Go) | new tokens, old revoked | both pasted in chat; /root/.env updated after |
| 1.7 | Atlas-seed routine (rerun seed_atlas_biblio on atlas rev change) | people/translations/editions current with seeds | check patalacheckpoints rev monthly; dry-run first |
| 1.8 | M00092/93 TAL split proposal (their lane) | 37 ahnika volume manifests wired | needs translation-work agent review (volumes are their mechanics) |

## Phase 2 — Formal coverage (autonomous, queue order)

| # | Step | Done when |
|---|---|---|
| 2.1 | Nyāsa rung (PHONEMIC-BODY-SPEC → prereg → Lean) | 50 loci regenerate from varga rules + twin refuses; feeds body pages |
| 2.2 | v9 embedding rung (size-key: recursive 5/11 embedding generates subtle+gross counts) | ratio re-earned or claim dropped forever |
| 2.3 | Permutation pair (śabdarāśi↔Mālinī: conservation + non-identity + yugapad) | twin refuses; bridges Recognition idempotence (scholar-reviewed bridge) |
| 2.4 | Krama-time P-PUSH2 (T-pins addendum first: read Q5+sciencetime) | prereg addendum → model → twin |
| 2.5 | Truth A→F gap-proofs (NonEntail re-verified post-E-EGO) | negative results recorded as findings |
| 2.6 | Doubt-stammer→vidyā rung (queue's thinnest row + vicikicchā hits) | prereg → model |
| 2.7 | Blind family-2 (mistral/qwen re-derivation of Upaya or Pramatr) | SAME/DIFFERENT/GAP note → REPLICATED status path |

## Phase 3 — Integrations (spec'd; owning lanes + humans decide)

| # | Step | Owner |
|---|---|---|
| 3.1 | Chunk↔verse map + source_verses fill (CHAIN-GAP) | translation-work/scholar lane |
| 3.2 | Packs evidence_refs + video carry-through + Zenodo openpatala IDs (BACKBONE §5) | factory/translation-work lanes |
| 3.3 | P-TK1 ruling (review pack ready) | scholar |
| 3.4 | T-C2 rater-2 + ti/ca + station full pass (harnesses ready; teacher-stage0 journal is the surface) | owner/scholar |
| 3.5 | Witness verification (NGMPP eyes; candidates file ready) | manuscript check |
| 3.6 | Layer-accept decisions at ingest (checker ready) | translation-work lane |
| 3.7 | Journey-ledger/trajectory/jev/vis-mode | owner go (explicitly gated) |
| 3.8 | Zenodo live publish (dry-run builds) | owner token |
| 3.9 | dīkṣā policy calls (eligibility edge cases, slang register hard cases) | owner |

## Phase 4 — Scale (quota/GPU/data)

| # | Step | Done when |
|---|---|---|
| 4.1 | Tau scale-up (n≥30, Wilson CI) → Phase-1 gate | tau(metric) > tau(chrF) or tuning verdict |
| 4.2 | Coverage/COMET baselines (torch box) | tau table with learned metrics |
| 4.3 | School-conditioned metric + vimarśa discriminator | tau(cond) > tau(not) |
| 4.4 | DA/MQM human gold (śāstric judges) | versioned judgment set exists |
| 4.5 | Persona LoRAs per register (GPU) | outputs pass proof gate |
| 4.6 | Frontier sprints in flipped order: KMT-17 (READY) → ṢaṭSS (fetch M00249) → KuRatnUdd (on acquisition) | first packet: phoneme/loci/Śakti extraction + five-maps diff |
| 4.7 | Triśirobhairava reconstruction (all 5 inputs on disk first) | stemmatic draft + uncertainty ledger |
| 4.8 | L0-as-terms pilot (ONE sūtra-like derivation; grammarian review) | derivation checks; method note |

## What deliberately NOT to do

- Second database / second ledger / second ID scheme (openpatala IS identity).
- Auto-sign, auto-publish, auto-ingest-writes into others' lanes.
- Quota spend on grunt work; GPU-blocked work without a GPU box.
- Treating heuristic PASS, Beautiful Output, or Big Model as proof.
- Editing history, inventing sigla, mixing verse/apparatus, merging tracks.
