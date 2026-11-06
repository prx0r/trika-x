# CRUX-01 walked end-to-end: does rāga-kañcuka present as lobha?

**Status:** machine walkthrough (MACHINE_DRAFT throughout), proving the chain
runs chunk → formal → argument → essay. Nothing here is signed, published,
or a finding about the texts. Tiers per claim.

## 1 · CHUNK (witness-pinned as far as today allows)

- **tsa08-p03** (8.39–8.64; `pt:pid` via passages.jsonl; openpatala:
  work `tantrasara` / `PTCND_sa_abhinavagupta-tantrasAra`, edition
  Nirnaya Sagara 1918 GRETIL — witness UNPINNED, see bridge/).
- Argmap premises (R-reconstructed from the gold argmap, not new claims):
  kalā gives partial agency; "rāga functions" in partial agency;
  "now knowing partially, clinging, I do" = the bound-soul formula;
  six-cover reckoning (māyā-six).
- Supporting: tsa08-p02 (mala doctrine; rāga-principle = karma-delimited
  longing), tsa-a08 v35 śaktipāta (grace context, not used in this crux).

## 2 · FORMAL (checked, inside stated scope)

- `KancukaCorr.corr_pull_raga`: pull maps to va. Status: KEY (stipulated),
  evidence-pinned (day-7 #6–8, #22, #35; day-2 #1–2, #6–7; day-4 #1; day-5 #13).
  `decide` verifies the table says it — nothing more.
- T-C1 pilot (`tools/tc1_cooccurrence.py`, 26 arcs, Fisher one-sided
  p=0.0462): lobith-headline arcs co-occur with thina/churn-headline arcs
  above chance; thin/churn never appear without lobha (3/3). Pilot only:
  n small, single diarist, machine-proposed decodes, owner-unreviewed.
- Honest limits (recorded, not footnoted): coverage is 3/5 coords
  (`coverage_partial`); ti/ca felt signatures unestablished; the mapping
  is not derived from the chunk — the chunk constrains the structural
  side only.

## 3 · ARGUMENT (argmap shape: question / premises / inference / unresolved)

- **Question:** does the rāga-kañcuka (structural: partial desire under
  limited agency) present in experience as lobha-cetasika (felt pull)?
- **Premises:** (P1) tsa08-p03: rāga functions *within* partial agency
  (T, argmap). (P2) Decodes: want+blocked co-occur (T-C1 pilot, R+E).
  (P3) Day-7 #18 is the clean instance: "i feel blocked AND i want siva
  consciousness" in one clause (lived, R). (P4) Thon Ly's composition
  discipline: write the mapping as general constraints; the ratio is the
  finding (method, R).
- **Inference (candidate):** rāga presents as lob mitigated: the structural
  restriction (only-so-much agency) is felt as pull toward what agency
  cannot secure. The T-C1 co-occurrence is predicted by, not proof of, this.
- **Unresolved:** (a) direction of explanation (does structure cause feel,
  or one vocabulary redescribe the other?); (b) N-restriction: does the
  mapping survive week-2+ decodes (kill condition armed); (c) thina without
  lobha never observed — is stall-without-pull possible (search the decodes);
  (d) TĀ witness for rāga-as-felt (UNPINNED).

## 4 · ESSAY (MACHINE_DRAFT — human disposes; do not publish, quote, or cite)

**Title (working):** *Wanting under one roof: rāga as the shape of lobha*

> Abhinavagupta's eighth āhnika describes bondage in one formula:
> "knowing partially, clinging, I do" [tsa08-p03, T]. The clause has three
> parts and the day-7 diaries keep producing all three together: partial
> knowing ("my god realisation has dissipated" [day-7 #3, lived]),
> clinging ("theres a craving for the state" [#6, lived]), and a thwarted
> "I do" ("i feel blocked and i want siva consciousness" [#18, lived]).
> The formalization under test maps this structural restriction
> (kalā+rāga active) to the felt pull (lobha) [KancukaCorr.corr_pull_raga,
> KEY not proof; T-C1 p=0.046 pilot]. What the week of decodes suggests —
> no more — is that want and blockage travel together (thin/churn never
> appear without lobha in 26 arcs), exactly as the "partial agency"
> doctrine would predict if rāga is what limitation feels like from
> inside. Against: n=26, one diarist, unreviewed decodes; the ti/ca
> coordinates have no felt signature yet, so the map is known-partial;
> and nothing here distinguishes "structure causes feel" from "two
> vocabularies for one event" — that is the open crux, honestly kept open.

**Claim table (essay-claim/1 shape):**

| # | Claim | Type | Evidence | Tier | Status |
|---|---|---|---|---|---|
| 1 | tsa08-p03 gives kalā→partial agency + rāga functioning | quotation | argmap tsa08-p03 | T | cited, not yet verbatim-bound (no audit run) |
| 2 | want+blocked co-occur above chance (p=0.046) | interpretive + statistical | tc1_cooccurrence.py, 26 arcs, vendored jsonl | E/R | pilot; kill-armed on week-2 |
| 3 | day-7 #18 is a clean want+blocked instance | quotation | play/day-07 L18 | lived (unreviewed) | machine-proposed |
| 4 | rāga presents as lobha | interpretive (reconstruction) | 1–3 + corr_pull_raga (KEY) | R | open crux; alternatives (d) recorded |

**PUSHBACK (self-review):** Destroy pass — (i) p-hacking risk: p=0.046 on
26 arcs with analyst-chosen arc boundaries; answer: boundaries were set
before the test (decode arcs predate tc1), but replication on week-2 with
pre-frozen arcs is required before any upgrade. (ii) The essay's causal
language ("presents as", "travel together") outruns a co-occurrence pilot;
verdict: keep, but every causal verb carries its pilot flag in-line (done
above). (iii) Missing: thina-without-lobha search not yet run — do it on
the vendored set before claiming asymmetry. **Honest remainder:** direction
of explanation open; ti/ca silent; decodes unreviewed; n tiny.

## 5 · What this walkthrough proves (and doesn't)

Proves: the chain RUNS end-to-end on real materials — every link resolves
(chunk id → formal theorem → argument node → drafted claim with tier).
Does not prove: the crux claim (open by design), the decodes (unreviewed),
or the essay (unsigned draft). Next crux in queue: doubt-stammer → vidyā
(T-C1's thinnest firm row + vicikicchā 1/89 hits).
