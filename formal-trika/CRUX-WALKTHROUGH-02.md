# CRUX-WALKTHROUGH-02: is the ego derivative or self-reflexive?

**Status:** machine walkthrough (MACHINE_DRAFT throughout), proving the chain
runs chunk → formal → argument → essay. Nothing here is signed, published,
or a finding about the texts. Tiers per claim.

## 1 · CHUNK (pinned)

- **tsa08-p04** (8.65–8.93; `pt:pid:ts:a08:b934ea526829`; openpatala:
  work `tantrasara` / `PTCND_sa_abhinavagupta-tantrasAra`, edition
  Nirnaya Sagara 1918 GRETIL — witness UNPINNED, see bridge/).
- 29 argmap units, 3369 chars, GRETIL source verified against pinned
  snapshot (`bridge_resolve --check --tw` green).

## 2 · THE ARGMAP (T-tier premises, read from gold)

| Verse | Question | Inference (T) |
|---|---|---|
| v65 | Why assume stirring? | Stirring must be assumed between; Sāṃkhya-seen separated guṇa. |
| v66 | Why presiding? | Without presiding, no fixed-man success. |
| v67 | How is mind born? | Guṇa to mind; man-light and object reflect. |
| v68 | How is I-maker born? | Mind-mirror turbid contact breeds self-pride; shell-silver simile. |
| v69 | Why not Sāṃkhya? | We keep I-feeling and makership; Sāṃkhya fits neither. |
| v70 | What is pure I? | Pure I: non-rivalled wonder-formed deliberation. |
| v71 | What is the instrument heap? | I-maker's instrument-heap named. |
| v72 | What is the nature heap? | Threefold nature-heap by guṇa difference. |

Key T-quotes (v68–v70, argmap premises, verbatim):
- "in non-self is self-pride, like silver-pride in shell" (Sāṅkhya account:
  ego = derivative from guṇa-mixture, silver-in-shell illusion)
- "Sāṃkhya's but that does not fit — for he does not wish self's
  I-feeling-nature; but we wish makership too of it" (Abhinavagupta's
  rejection: Sāṅkhya denies I-feeling AND makership)
- "that pure deliberation alone, non-rivalled, own-self-wonder-formed I"
  (Trika correction: ego = vimarśa, self-reflexive, no derivative cause)

## 3 · FORMAL (what exists, what's missing)

**Exists (ARMED, tsa08 work-level):**
- `Kancuka.lean` count_5 + pairings_distinct (5 kañcukas, distinct capacities)
- `Grace.lean` flip_iff_ready_and_grace (v35 śaktipāta, grace as free variable)
- `Transitions.lean` anava_stuck_exists + karma_loop_exists (tsa08-p02 mala)
- `AnswerKey.lean` key_five_kancukas (tradition count)

**Missing (the formal gap this crux identifies):**
No Lean model addresses ego-origin. Specifically absent:
1. A state where ego exists with **no derivative cause** (self-reflexive
   vimarśa) — the Trika position (v70).
2. A state where ego **requires** a derivative cause (guṇa-mixture,
   silver-in-shell) — the Sāṅkhya position (v68).
3. The distinction between them: can self-reflexive ego exist, or is
   ego always derivative?

**What would formalize it (sketch, not built):**
```lean
-- two competing accounts of ego-origin
inductive EgoOrigin where
  | derivative    -- Sāṅkhya: ego = f(mind-mirror, object-contact)
  | selfReflexive -- Trika: ego = vimarśa, non-rivalled, wonder-formed

-- the formal question: can selfReflexive exist without derivative cause?
-- Sāṅkhya says no (ego always requires guṇa-mixture).
-- Trika says yes (pure I is self-grounding).
-- The crux: which account is correct? Lean can check consistency of
-- each account's axioms, but cannot decide which is true about minds.
```

## 4 · ARGUMENT (argmap shape)

- **Question:** Is the ego (ahaṃkāra) derivative (Sāṅkhya: guṇa-mixture,
  silver-in-shell) or self-reflexive (Trika: pure vimarśa, non-rivalled)?
- **Premises:** (P1) v68: ego arises from mind-mirrored object-contact,
  like silver-pride in shell (Sāṅkhya account, T). (P2) v69: Sāṅkhya
  "does not fit" — denies I-feeling AND makership; Abhinavagupta keeps
  both (T). (P3) v70: pure I = non-rivalled wonder-formed deliberation
  (vimarśa) — the Trika correction (T). (P4) The formal gap: no Lean model
  distinguishes these accounts (R, verified: no ego-origin theorems in
  EVIDENCE.json).
- **Inference (candidate):** The crux is real and formalizable. The
  Sāṅkhya account (derivative) and Trika account (self-reflexive) make
  different structural claims about ego's origin. A Lean model could check
  each account's internal consistency, but cannot decide which is true —
  that's the honest boundary (finite models ≠ metaphysical verdicts).
- **Unresolved:** (a) Does the Trika account's "non-rivalled" clause
  do real formal work (exclude rival I-origins) or is it decorative?
  (b) The silver-in-shell simile: is it a claim about ego's *structure*
  (composite, like silver-in-shell) or its *origin* (derivative from
  guṇa-mixture)? (c) v69's "makership" (kartṛtva): is this a separate
  claim from I-feeling (ahaṃ-vimarśa), or the same claim from a
  different angle? (d) The instrument-heap (v71) and nature-heap (v72)
  are named but not formalized — are they ego's *parts* or ego's
  *causes*?

## 5 · ESSAY (MACHINE_DRAFT — human disposes; do not publish, quote, or cite)

**Title (working):** *Silver in the shell: two accounts of where the I comes from*

> Abhinavagupta's eighth āhnika poses a question that Sāṅkhya answers one
> way and Trika answers another: where does the "I" come from? Sāṅkhya says
> it arises from mind-mirrored object-contact — like silver-pride in a
> shell, a derivative illusion [tsa08-p04 v68, T]. Abhinavagupta rejects
> this: "Sāṃkhya's but that does not fit — for he does not wish self's
> I-feeling-nature; but we wish makership too of it" [v69, T]. The Trika
> correction: the pure I is "non-rivalled, own-self-wonder-formed
> deliberation" [v70, T] — self-reflexive, not derivative. The formal
> gap: no Lean model distinguishes these accounts (verified: no ego-origin
> theorems in EVIDENCE.json). What would formalize it: two competing
> `EgoOrigin` accounts (derivative vs self-reflexive), each with internal
> consistency checks — but Lean cannot decide which is true about minds.
> The crux is real, formalizable, and honestly open. What remains
> undetermined: whether "non-rivalled" does formal work or is decorative;
> whether silver-in-shell claims structure or origin; whether makership
> and I-feeling are one claim or two.

**Claim table (essay-claim/1 shape):**

| # | Claim | Type | Evidence | Tier | Status |
|---|---|---|---|---|---|
| 1 | Sāṅkhya: ego = derivative from mind-mirror contact (silver-in-shell) | quotation | argmap tsa08-p04 v68 | T | cited, not verbatim-bound (no audit run) |
| 2 | Abhinavagupta rejects Sāṅkhya (denies I-feeling + makership) | quotation | argmap tsa08-p04 v69 | T | cited |
| 3 | Trika: pure I = non-rivalled vimarśa (self-reflexive) | quotation | argmap tsa08-p04 v70 | T | cited |
| 4 | No Lean model distinguishes these accounts | interpretive | EVIDENCE.json scan (no ego-origin theorems) | R | verified absence, not proof of impossibility |
| 5 | The crux is formalizable (two EgoOrigin accounts) | interpretive | 1–4 + structural analysis | R | open; consistency checks possible, truth not decidable in finite models |

**PUSHBACK (self-review):** Destroy pass — (i) The essay says "no Lean
model distinguishes these accounts" — true of *our* repo, but Thon Ly's
formal-abhidhamma might have ego-related results we haven't checked.
Answer: our EVIDENCE.json covers our repo; the absence claim is scoped
to formal-trika, not the whole estate. (ii) "Silver-in-shell" could be
read as a claim about ego's *structure* (composite) rather than *origin*
(derivative) — the essay flags this as unresolved (b) but leans derivative.
Verdict: keep the lean, note the ambiguity in-line (done). (iii) The
formal sketch (`EgoOrigin` inductive) is R-tier — it's our proposal, not
a root-text claim. Flagged as such. **Honest remainder:** "non-rivalled"
undetermined; makership vs I-feeling undetermined; no truth-decision
possible in finite models; silver-in-shell ambiguity open.

## 6 · What this walkthrough proves (and doesn't)

Proves: the chain runs on a second crux — chunk (tsa08-p04, pinned,
snapshot-verified) → formal (existing ARMED results + identified gap)
→ argument (4 premises, 4 unresolved) → drafted claim table with tiers.
Does not prove: the crux claim (open by design), the texts' metaphysical
position (out of scope), or that the formal sketch is the right model.
Next crux in queue: the doubt-stammer → vidyā rung (T-C1's thinnest
firm row + vicikicchā 1/89 hits), or tsa08-p04's instrument-heap (v71)
if the ego-origin crux needs more depth.
