# CRUX-WALKTHROUGH-03: are the eleven faculties wombed in ahaṃkāra?

**Status:** machine walkthrough (MACHINE_DRAFT throughout), proving the chain
runs chunk → formal → argument → essay on the finished Tantrasara. Nothing
here is signed, published, or a finding about the texts. Tiers per claim.

## 1 · CHUNK (witness-pinned as far as today allows)

- **tsa08-p04** (Tantrasāra a08, instrument-heap verses; `pt:pid` via
  passages.jsonl @9000e5c8; openpatala work `PTCND_sa_abhinavagupta-tantrasAra`,
  edition Nirnaya Sagara 1918 GRETIL — CANDIDATE-EDITION, witness UNPINNED).
- Argmap premises (R-reconstructed from gold argmap tsa-a08, not new claims):
  v71: "eṣo 'sya ahaṃkārasya karaṇaskandhaḥ — this is of the I-maker:
  instrument-heap" (the heap BELONGS to ahaṃkāra); v73: the sāttvika (lucid)
  portion yields mind + five buddhīndriyas, and generable mind carries
  "all-subtle-birth power" (sarvatanmātrajananasaṃsāmarthyayuktaḥ);
  v75: maker-part is ahaṃkāra alone; the five karmendriyas come "from just
  the lucid I-maker excelling in subtle-part" (udriktatanmātrabhāgaviśiṣṭāt
  tu sāttvikād eva ahaṃkārāt); v79: action-endlessness does not entail
  sense-endlessness (karmānantyam api na indriyānantyam āvahet).
- Supporting: tsa08-p01 (v01–v02, v16): tattva = partial pervasion;
  five principles by power-primacy (cit/ānanda/icchā/jñāna/kriyā-led).

## 2 · FORMAL (checked, inside stated scope)

- `Tattva.lean :: eleven_wombed`: 11 faculties nest inside the ahaṃkāra
  group. Status: T (decide-verified structure; PR #4 corrected the
  faculties to 11-wombed from an earlier miscount — the correction record
  is part of the evidence). `five_gross_elements`, `thirty_six`,
  `all_groups_present`: group sizes 5/11/36 re-earned after correction.
- Honest limits: the Lean model nests by GROUP MEMBERSHIP (finite
  enumeration); the text's relation is GENERATIVE ("from the lucid I-maker",
  "mind begets"). Membership ≠ begetting — the formal claim is weaker
  than the textual one, and the walkthrough does not upgrade it.
  The 0.28 compression ratio stays DOWNGRADED (no second key).

## 3 · ARGUMENT (argmap shape: question / premises / inference / unresolved)

- **Question:** does the text's generative partition (sāttvika→mind+5
  knowing-senses; subtle-excelling→5 doing-senses; both OF ahaṃkāra)
  support modeling the eleven as wombed-in-ahaṃkāra rather than flat?
- **Premises:** (P1) v71: the heap is ahaṃkāra's (T, argmap). (P2) v73:
  lucid portion → mind + 5 jñānendriya; mind itself begets (T, argmap).
  (P3) v75: 5 karmendriya from the same lucid I-maker under the
  subtle-excelling aspect (T, argmap). (P4) v79: senses stay 11 while
  actions are endless — the count is principled, not enumerative drift
  (T, argmap). (P5) Formal: eleven_wombed nests 11 inside ahaṃkāra's
  group (T, decide).
- **Inference (candidate):** the wombed model is textually supported:
  both sense-fives derive from ahaṃkāra under stated aspects, and the
  text blocks the obvious deflation (more actions ≠ more senses).
- **Unresolved:** (a) membership-vs-begetting gap (formal weaker than
  text — recorded, not bridged); (b) manas double role (sibling of the
  five AND begetter — is 5+5+1 the right cut, or 6+5?); (c) TĀ witness
  for the heap passage (UNPINNED); (d) blind-lame verse (v75) read
  once — the "non-leaving of I-formed knowing-doing" premise needs a
  second pass before it carries weight.

## 4 · ESSAY (MACHINE_DRAFT — human disposes; do not publish, quote, or cite)

**Title (working):** *Eleven from one: the I-maker's instrument-heap*

> Abhinavagupta's eighth āhnika defines a category as what pervades only
> some differences — earth the example, running through every world-egg
> (v02, T) [tsa-a08:tsa08-p01]. The faculties get the same treatment in reverse:
> instead of asking what they pervade, the text asks what they come from.
> Answer: the I-maker. "This is of the I-maker: instrument-heap"
> (v71, T) [tsa-a08:tsa08-p04] —
> mind and five knowing-senses from its lucid portion, mind itself
> birth-endowed toward the subtles (v73, T) [tsa-a08:tsa08-p04]; five
> doing-senses from the
> same lucid I-maker under its subtle-excelling aspect [tsa-a08:tsa08-p04
> v75, T]. Eleven,
> no more: though doings are endless, senses are not — action-infinity
> "does not bring sense-infinity" (v79, T) [tsa-a08:tsa08-p04]. The formal model nests eleven
> inside ahaṃkāra's group [eleven_wombed, T] — a membership shadow of the
> text's generative claim, weaker by exactly the begetting relation, which
> is why this essay states the support as partial and keeps (a)–(d) open.

**Claim table (essay-claim/1 shape; tiers CORRECTED 2026-11-06 after PUSHBACK —
argmap-grounded claims are R until verbatim-bound against source bytes):**

| # | Claim | Type | Evidence | Tier | Status |
|---|---|---|---|---|---|
| 1 | heap belongs to ahaṃkāra (v71) | quotation | argmap tsa-a08-v71 | R | reconstructed; banked only as heap-named (thin) |
| 2 | lucid→mind+5 jñānendriya; mind begets (v73) | quotation | argmap tsa-a08-v73 | R | reconstructed; NOT banked — verbatim bind owed |
| 3 | 5 karmendriya from subtle-excelling lucid I-maker (v75) | quotation | argmap tsa-a08-v75 | R | reconstructed; NOT banked — verbatim bind owed |
| 4 | action-endlessness ≠ sense-endlessness (v79) | quotation | argmap tsa-a08-v79 | R | reconstructed; NOT banked — verbatim bind owed |
| 5 | eleven nest in ahaṃkāra group | structural | Tattva.lean eleven_wombed | T | decide-verified, weaker-than-text |
| 6 | wombed model textually supported (partial) | interpretive | 1–5 | R | open; (a)–(d) recorded |

**PUSHBACK (ran 2026-11-06; two families converge):**
- beam-free (opencode-go): v02/v73/v75/v79 unbanked; treating membership as
  textual support promotes R into T. Verdict: hypothesis, not finding.
- deepseek-v4.1-flash (CF): "overbuilt relative to banked evidence";
  strongest counter-reading — "instrument-heap" may be a SET-LABEL, not a
  generative causal claim; p04's banked material (v68–72) concerns
  silver-in-shell derivation, pure-I vimarśa, guna-differentiation, not
  Sāṃkhya-style begetting. Surviving thin reading: v71 names heap, v72
  differentiates by guna — not enough for the generative thesis.
- Resolution ACCEPTED: claims 1–4 relabeled R (were T); essay's "partial"
  caveat kept but prose trimmed of causal verbs until verbatim binds land.
  Verbatim-bind path exists (tsa volume spans) — §5 next step, now load-bearing.
- Tool fix in passing: `pushback.py cf_object` now parses OpenAI-style
  `choices` responses (deepseek returns those, not `result.response`).
- Linker finding: only paras with `[work:target]` bracket markers get
  objected (1/15 paras); claim-table rows are UNCITED — tables need inline
  markers or linker support before PUSHBACK covers them.

## 5 · What this walkthrough proves (and doesn't)

Proves: the chain runs on finished-Tantrasara materials at full depth —
93-unit gold argmap → pinned chunk → checked theorem → tiered draft.
Does not prove: the begetting relation (unformalized), the essay
(unsigned), or the edition (CANDIDATE). Next: verbatim-bind claims 1–4
against source bytes via the tsa volume spans; second pass on v75's
blind-lame premise; manas-cut crux (6+5 vs 5+5+1) as CRUX-04 candidate.
