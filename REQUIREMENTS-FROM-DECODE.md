# What the Trika-X formulation must include — requirements from the lived decode
*Status: REFERENCE. Formalization requirements; stable reference.

**Date:** 2026-11-06. **Status:** PROPOSED (requirements, not results).
**Evidence:** `nibbanahelp/corpus/abhidhamma/play/day-07.decode.md` — 48 moments,
47/47 abhidhamma-sets POSSIBLE, 1 UNMAPPED, 8 low-confidence. The pattern of
*where it went thin* is the specification below. Rule: formalizations arise
OUT OF this data; tiers per claim (T=root-text, R=reconstruction).

## 0 · What the decode showed

The Abhidhamma layer did its job: moment taxonomy, legal co-arising sets,
rare-factor flags (vicikicchā 1/89 hit exactly on the have-it/feel-it
oscillation), asevana repetition visible on both sides. But its thin spots
cluster — and they cluster on exactly the Trika phenomena:

| Moments | Abhidhamma verdict | What it missed (the Trika demand) |
|---|---|---|
| 6–8, 18, 22, 35 (craving the *state*, "ultimate drug", blocked+want) | lobha+ditthi, legal | *Craving a meditative state* vs *craving an object* — same factors, different structure. Needs the **rāga-kañcuka reading** (partial desire as structural contraction, not just felt pull). |
| 12, 27, 32–33, 39–42 (resolve, surrender, "create conditions for grace", offering) | saddha/viriya/alobha, legal but flat | *Devotion as method* — bhakti orientation, resolve-then-yield sequence, necessary-without-sufficient conditions. Needs **upāya axis + grace as free variable**. |
| 23, 31 ("repeating me siva", seeker-seen-through) | vitakka/vicara/saddha, legal | *Mantra-repetition vs insight-cascade* — same "thought" factors, different means. Needs **āṇava vs śākta means distinction**. |
| 25–31 (maze, levitation, "already happened so nothing can be done") | panna or `?`/thin (26) | *Fatalism inside insight* — is "nothing can be done" ditthi or the truth of grace? The decode couldn't tell. Needs **grace formalized badly enough to test**. |
| 46–48 (lonely → inquiry → "finding myself in you, each time a thrill") | dosa → vitakka → piti+panna+adosa, legal | *The recognition arc itself* — push, inquiry, then thrill-of-reidentification. Abhidhamma names the factors; it cannot say what *flipped*. Needs **T_rec + Part-target** (already have the bones). |
| 11, 44 (evenness claims) | tatramajjhattata / adhimokkha, thin | *Equanimity vs positioning* — is it evenness or self-image? Needs **pramātṛ-level adjudication** (which experient is talking?). |

Summary: the felt side is covered; the **structural/dynamic side is missing**.
Abhidhamma says *what co-arises*; Trika must say *what contracts, what means
operates, what flips, and what is grace*.

## 1 · Required formulation components (7)

### F1 · rāga-kañcuka ↔ lobha correspondence (the deepest bridge)
The decode's recurring weather (lobha+ditthi loops, §§1–2, 4) is *structurally*
partial desire under limited agency: "blocked AND want" (18) = kalā + rāga
firing together. `Coords.lean` already maps kañcukas→coordinates; what is
missing is the **felt↔structural correspondence**: rāga (structural) presents
as lobha (felt); kalā (structural) presents as thina/uddhacca (felt).
- Prediction T-C1: across days 1–7 decodes, lobha-clauses co-occur with
  thina/uddhacca-clauses above chance *within the same process arc*
  (want+blocked travel together). Kill: no co-occurrence → the bridge is poetry.
- Requires per-moment **kañcuka-coordinate annotation** alongside factor sets
  (joint decode format, §3).

### F2 · upāya means axis (mantra ≠ insight)
Moments 23 (japa-repetition) and 30–31 (insight cascade) share vitakka/vicara
but are different *means*: āṇavopāya (uccāra/repetition) vs
śāktopāya (vimerśa-purification) vs śāmbhava (instantaneous, no means).
The decode is blind to means; the formulation must add it as a **per-moment
upāya tag with textual criteria** (which tantra passages define each means —
T-tier pins required before any tagging).
- Prediction T-C2: two raters independently tag japa/insight/instant clauses
  with the criteria; agreement ≥ 0.6 or the criteria are rewritten, not the data.

### F3 · grace (śaktipāta) as free variable
Moments 33 ("create the conditions for grace"), 28 ("levitating out"),
26 ("already happened so nothing can be done"): necessary conditions are
statable, sufficient ones are not — by the diarist's own report. Formalize
honestly: preconditions (surrender/resolve/readiness predicates) are
necessary-but-insufficient; the transition itself takes a **free variable
(grace), unconstrained by the model**. This is falsifiable structure, not fog:
- Prediction T-C3: every grace-clause in days 1–7 weist either (a) sufficient
  conditioned reading (killed — drop the variable there) or (b) residual
  unconditioned step (kept). The variable earns its place clause by clause.
- Kill (global): if zero clauses need it, śaktipāta stays doctrine (T), never
  enters the model (R).

### F4 · T_rec scope discipline (state ≠ recognition)
Moments 6–8 conflate *craving a state* with *recognition*: "the ultimate
drug". The formulation must keep `Transitions.lean`'s discriminator
(acquire-rewrites-content vs trec-preserves-content) live in the decode:
state-craving moments get tagged **acquisition-pattern**, recognition-claim
moments get the 4-conjunct check (`Conjuncts.lean`). Moment 48 passes
transformation + reidentification + veridicality-claim + stabilization —
record it as the day's **candidate T_rec** with scope stated (finite model).
- Prediction T-C4: claimed-recognition clauses across the week satisfy more
  conjuncts on average than state-craving clauses. Kill: no separation.

### F5 · pramātṛ-level adjudication (who is talking?)
Moments 11, 44 (evenness claims), 31 (seeker-seen-through), 9→43 (shame→
restraint): same words, different stations. The 7-experient control
(`Pramatr.lean` TK-C1) must become a **station tag**: is this clause spoken
from sakala (bound), vijñānākala (āṇava-only), mantra-position, or Śiva?
The mantra-triad lesson (P-TK1b: adhvan-positional, not mala-compositional)
applies directly — station is positional, not a moral grade.
- Requires: station criteria in experience-language (a second decode table).

### F6 · bhakti orientation predicate
Devotion appears as method (12, 27, 32), as offering (13, 41), as conviction
(42, 44), as yielding (39). The formulation needs **bhakti as a first-class
orientation**: object (siva/all/guru), direction (offering-up vs pulling-down),
and its upāya role (when is devotion the means vs the fruit?). At minimum a
typed vocabulary; at most, transition rules (offering-up + readiness ⇒
grace-eligible, feeding F3's preconditions).

### F7 · the 46–48 arc as process template
Loneliness-ache → aversion → inquiry → thrill-of-reidentification is a full
process: duḥkha → dosa → vitakka/vicāra → piti+panna+adosa. Candidate for the
first **recognition-worldpack trajectory**: a legal path through the joint
(abhidhamma × trika) state space, replayable against other days. If days 1–6
show the same arc shape with different content, the template is real.

## 2 · Interface: two systems, one moment

| Layer | System | Says | Never says |
|---|---|---|---|
| felt set | Abhidhamma (have) | what co-arises this moment | why / by what means / what flipped |
| coordinates | Trika F1 (new) | which contractions active (K/A/V/T/C) | the feeling (that's L1's job) |
| means | Trika F2 (new) | āṇava/śākta/śāmbhava operative | — |
| flip | Trika F4 (have bones) | T_rec? which conjuncts? | metaphysical verdict |
| station | Trika F5 (new) | which pramātṛ speaks | moral grade |
| grace | Trika F3 (new) | preconditions met? free step? | that grace occurred |

Joint decode line (example, moment 18 re-annotated):
`blocked+want → B:{lobha,thina}+R [PASS] · K:{kala,raga} · means:— · station:sakala · grace:n/a`
The B-side is checked today; K/means/station/grace columns are the
formulation debt this doc specifies.

## 3 · Build order (for the lead agent)

1. F1 correspondence table (rāga↔lobha, kalā↔thina/uddhacca, vidyā↔vicikiccha?,
   niyati/kāla↔? marked unknown — unknowns are findings) + T-C1 test on days 1–7.
2. F2 upāya criteria with T-tier pins + T-C2 agreement test.
3. F4 live discriminator in the decoder (acquisition-pattern vs conjunct-check).
4. F3 grace variable + T-C3 clause audit.
5. F5 station table (second decode table) + F6 bhakti vocabulary.
6. F7 trajectory template once 1–5 exist; cg worldpack after.

## 4 · Non-goals (load-bearing)

No proof that Trika is true; no theorem about minds (finite models only);
no auto-tagging of diary (machine proposes, human disposes — the diarist
adjudicates every `?` and UNMAPPED); no promotion R→T; no new poles until
F1–F4 earn their keep. The Abhidhamma linter stays the consistency floor:
a Trika annotation that requires an illegal factor set is refused, not
reinterpreted.
