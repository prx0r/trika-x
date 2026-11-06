# TEACHER-INTERFACE — what the assessor needs from the formalization (spec, not built)

Endgame role: a teacher that assesses where the diarist is *according to the
system* — breaking down complexity instead of performing certainty. This file
specifies the interface between the formal core and that teacher. Nothing
here runs; it tells future builds what to consume.

## What the teacher asks, and what answers it

| Teacher question | Formal instrument (exists today) | Missing |
|---|---|---|
| What is active in this clause? | abhidhamma factor check (`check_factors.py`, nibbanahelp side; 52-cat vocab + priors in `corpus/abhidhamma/`) + rule R1–R18 transcription | week-2+ decodes; blind re-derivation (BLIND.md) unrun |
| What is contracted right now? | KancukaCorr felt→coordinate map (3 firm rows, 2 explicit unknowns) | ti/ca felt signatures (F-CORR partial); week-2+ T-C1 |
| By what means is this working? | UPAYA-CRITERIA (3 means, experience criteria) | rater-2 agreement (sheet ready, T-C2 UNRESOLVED) |
| Did recognition happen here, or acquisition? | Transitions discriminator + 4-conjunct audit (TREC-AUDIT, 3.0 vs 0.0 pilot) | stabilization evidence (S=0 throughout); follow-up days |
| Which station is talking? | STATION-TABLE (positional criteria) | applied to ~4 moments only; needs systematic pass |
| Is grace in play? | Grace biconditional + T-C3 audit (5/5 kept, pilot) | rater-2 on grace-clauses; kill rule armed |
| What comes next? | ARC-TEMPLATE v1 (affliction → inquiry → recognition-claim) | recurrence test on week-2+ |

## Response discipline (load-bearing)

- Never assert a station, a recognition, or grace. Offer the *reading* with
  scope: "these 3 conjuncts check; stabilization unshown" — not "you recognized".
- Uncertainty is content: `?` marks and UNMAPPED are shown to the diarist,
  never smoothed. The teacher that hides its remainder is a guru-trap.
- Adjudication stays human: the diarist signs every tag (machine proposes).
  The teacher may ask ("is this doubt or inquiry?") but never re-label silently.
- Provenance rides every answer: factor set → check receipt; station →
  STATION-TABLE row; recognition claim → conjunct scores; grace → audit ref;
  doctrine → chunk id (EVIDENCE.json) → witness (openpatala, when bridged).

## Build order (teacher track)

1. Rater-2 pass (unblocks T-C2; unlocks means-advice: āṇava→repeat, śākta→discriminate, śāmbhava→stop-techniquing).
2. Station pass over all 144 moments (unlocks "which station" answers).
3. Crux-queue feed: recurring unmapped/contradictory moments become Treeka cruxes (teacher's curriculum).
4. Relay integration: relay tiers gain `formal_status` (which spans are Lean-checked); teacher cites receipts, never asserts.
5. Journey-day truth: Day N consumes only gated units (no rung ships without hash+decision+gate+signer — endgame invariant).

## Non-goals

No auto-signing, no E2E practice authorization, no initiation logic
(eligibility stays human-review), no claiming the model is the mind.
