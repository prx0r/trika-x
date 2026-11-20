# ESSAY GOLD STANDARD — decoding a published chapter into a writing contract

*Derived 2026-11-15 from Mrinal Kaul, “Causal Reasoning in the Trika Philosophy of
Abhinavagupta” (Handbook of Logical Thought in India, Springer 2022, pp. 227–250,
doi:10.1007/978-81-322-2577-5_31). Machine skeleton:
`bridge/essay-gold/kaul-causal-reasoning-2022/structure.json`. Template:
`bridge/essay-gold/kaul-causal-reasoning-2022/template.json`. Tool:
`tools/essay_gold_analyze.py`.*

This is **form decoded, not content copied**. It answers one question the essay
factory has never answered with evidence: *what does a finished, peer-reviewed
essay in our field actually do, section by section?* Everything below is
measured from the text, with the commands to reproduce it.

---

## 1. The measured skeleton

15 blocks, 15,452 words. Body (excluding front matter and references) is
12,788 words across 9 sections. Word shares are of the body.

| # | Role | Section | Words | Share | Verses cited | Objection moves | Reply moves |
|---|---|---|---|---|---|---|---|
| — | abstract | Abstract | 253 | — | 0 | 1 | 0 |
| — | keywords + abbreviations | — | 64 | — | — | — | — |
| 1 | introduction | Introduction | 1,057 | 8.3% | 0 | 1 | 1 |
| 2 | history | Historical Context | 1,276 | 10.0% | 4 | 1 | 6 |
| 3 | method | Philosophical Rationalization of Tantric Sources | 2,755 | 21.5% | 9 | 6 | 7 |
| 4 | interlocutor | Encountering Buddhists | 2,107 | 16.5% | 10 | 8 | 8 |
| 5 | argument | The Seed and the Sprout | 1,680 | 13.1% | 13 | 11 | 13 |
| 6 | case | Meditator’s Desire as Cause | 1,188 | 9.3% | 10 | 2 | 1 |
| 7 | argument | Complex Causality of Totality Factor | 1,573 | 12.3% | 7 | 7 | 9 |
| 8 | thesis | Śiva as the Perfect Agent and His Autonomous Agency | 614 | 4.8% | 6 | 2 | 2 |
| 9 | conclusion | Conclusion | 538 | 4.2% | 0 | 0 | 1 |
| — | references | Primary Sources / Secondary Sources | 2,347 | — | — | — | — |

Corpus totals: **59 verse references, 25 verses quoted in full Sanskrit, 59
narrative citations, 13 parenthetical citations, 35 questions, 211 inference
markers (if/then/because/therefore), 4 explicit author-claims.**

The shape that matters:

```
front matter (abstract · keywords · abbreviations)
  ~40%  context + method           (history + rationalization)
  ~35%  close reading of verses    (interlocutor + two arguments + case)
  ~10%  synthesis                  (totality + agency)
   ~5%  conclusion                  (contribution + desideratum)
references (primary sources, then secondary, author-date)
```

**The thesis is not announced up front.** Only four first-person claim moves,
three of them in the conclusion. The argument is *enacted* by the objection/
reply rhythm and only *named* at the end. This is the opposite of the
announce-then-support shape most machine drafts default to.

---

## 2. The move grammar (the reusable unit)

Every substantive section repeats one four-beat unit, and the counts confirm it:
40 objection moves against 48 reply moves across 9 sections.

```
1. EXPOSITION  state the source position in its own terms
2. OBJECTION   give the rival the strongest form of their argument
3. REPLY       answer from the primary author/commentator, citing a verse
4. CONSEQUENCE draw what follows for the thesis, then hand back to exposition
```

Examples measured in the text:

- *Encountering Buddhists* — 8 objections, 8 replies. The Vijñānavādin and
  Mādhyamika positions are stated first at full strength (store-house
  consciousness, dependent origination), then answered.
- *The Seed and the Sprout* — 11 objections, 13 replies. The densest argument
  section and the most verse citations (13). This is where the thesis is won.
- *Complex Causality of Totality Factor* — 7 objections, 9 replies; the
  sāmagrī debate, resolved by grounding plurality in a single perceiver.

The unit is **adversarial, not expository**. A draft that only summarises the
author is not this genre.

---

## 3. The verse protocol (primary-source discipline)

The chapter references 59 verses and quotes 25 of them in full. The pattern is
consistent:

```
cite in running text        (TĀ 9.13)
quote Sanskrit in full      bījamaṅkura ity asmin satattve hetutadvatoḥ | ...
gloss/translate             “mere succession ... does not constitute causality”
report the commentator      Jayaratha asks whether priority and posteriority
                            are different from the entities ...
analyse the move            what the verse does to the opponent’s position
mark whose translation      “All translations ... are my own, unless indicated”
```

This maps directly onto our layering:

| Gold-essay move | Our lane | Join key |
|---|---|---|
| verse reference | `translation-work` ledger | chunk locator / verse id |
| Sanskrit quote | `t1` / `sanskrit` source bytes | `source_sha256` |
| gloss | `l0` (forks) → `l2` | `l0_ids` |
| commentator’s reading | `argmap` (`uncertainties`, options) | `verse_id` |
| analysis / consequence | `c1` essence + essay prose | claim id |
| translation provenance | T-tier claim `source_edition`, `span_sha256` | `ESSAY-SCHEMA.md` v2 |

The gold paper does **not** hide ambiguity: where Jayaratha’s gloss is weak it
says so (“Jayaratha has resorted to rather unconvincing explanation here”). That
is our `l0` fork / `argmap` uncertainty surfacing in prose — the crown jewel
the endgame plan says is currently invisible.

---

## 4. What our pipeline already has, and what it lacks

`essay_compile.py` today produces an **expansion draft**: owner voice quotes,
frozen claims tiered T/R, formal references, open questions, a receipt. It is
the *skeleton* of a gold essay — the grounds and the claims — but it is not
prose.

| Stage | Gold essay requires | We have | Gap |
|---|---|---|---|
| architecture | 9-role skeleton with word budget | no budget | `template.json` now gives one |
| moves | exposition→objection→reply→consequence | claim bullets | no move planner |
| verse discipline | cite → quote → gloss → analyse | `passage_evidence` + forks | no prose binding |
| citation | 59 narrative vs 13 parenthetical | markers `[CLM-id]` | no author-date layer |
| thesis timing | earned, named in conclusion | claims up front | prose rewrite needed |
| honesty | states what remains a desideratum | `open_questions` | good; keep |

The missing stage is exactly the `v6 prose` stage in `ESSAY-PIPELINE.md`. This
document is its acceptance target: **a draft is ready for human review when it
has the nine-role skeleton, the four-beat moves, and the verse protocol, with
every Sanskrit span still bound to the ledger.**

---

## 5. Mapping onto `ESSAY-SCHEMA.md`

No schema change is needed; the gold essay is the *output* the schema feeds.
Proposed additions (amendment, not edit-in-place):

- `essay.json` gains an optional `plan` block mirrored from `template.json`:
  `{role, title, target_words, moves[], verse_ids[]}` per section. Frozen before
  prose, like `claims` — so drift is measurable.
- `essay_check.py` gains a **shape gate** (advisory first): body words within
  ±30% of the budget; every section has ≥1 objection and ≥1 reply OR a stated
  reason it does not (e.g. conclusion); every quoted Sanskrit span resolves to a
  ledger verse and carries a translation.
- `receipt.json` records `plan_sha256`, so the prose can be checked against the
  plan it claims to follow.

Until that gate exists, this is a target, not an enforced rule — same honesty
convention as the rest of `ESSAY-SCHEMA.md`.

---

## 6. The wider corpus on R2 (what to learn next)

The same bundle format holds a large body of Śaiva/Buddhist scholarship. The
full text lives in Academia.edu “bundles”, each a ZIP with the target paper plus
`more_papers_by_*` or `most_similar_papers_to_this_one/`:

| Bucket | Prefix / shape | Count observed |
|---|---|---|
| `sourcematerial` | `Academia.edu_Bundle_-_*.zip` (+ `new/`) | 82 zips |
| `sanskritree` | `Academia.edu_Bundle_-_*.zip`, Tantraloka packs | 33 zips |
| `source-library` | `tantra/source/classical/*.zip` | 8 zips |

Run the analyzer across them to turn “I think essays look like this” into a
measured distribution:

```sh
# 1. fetch a sample (R2 creds from /root/.r2-env)
# 2. unzip, then point the analyzer at every PDF
cd /root/trika-x/formal-trika
for p in /tmp/gold-corpus/**/*.pdf; do
  python3 tools/essay_gold_analyze.py "$p" --out "${p%.pdf}.structure.json"
done
```

A first pass over 75 extracted PDFs (two bundles) gave a **median of 7 body
sections and ~9,200 words** — shorter than Kaul’s chapter, which is a handbook
chapter, not a journal article. Treat the *pattern* (context → interlocutor →
close reading → synthesis → conclusion, with an objection/reply spine) as the
invariant, and the **word budget as genre-dependent**.

Correctness note: the first corpus pass’s role labels were weak because most
papers use numbered headings (`2.`, `3.`) that carry no role keyword. The
analyzer is honest about this — roles are heuristic. Improve the vocabulary in
`ROLE_HINTS` and re-run; do not read “body” as “no role”.

---

## 7. Limits (do not paper over)

- **FORM only.** This says nothing about whether Kaul’s readings are correct,
  or whether our translations will be. It only says how the prose is built.
- **One gold essay is not a sample.** It is a strong single reference. The R2
  corpus is the way to test which features generalise.
- **Author-date citation is humanities style.** Our ledger binding is stronger
  than a bibliography; keep both, do not collapse them.
- **Rights.** The chapter is copyrighted. Analysis only; cite the DOI; never
  serve the text from svatantrya.net.
- **No auto-write.** The move planner and shape gate are proposals. Prose that
  passes them is still `MACHINE-COMPILED` until a human signs.
