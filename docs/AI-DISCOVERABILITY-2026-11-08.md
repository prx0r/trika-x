# AI DISCOVERABILITY — research notes + plan (2026-11-08)

*Research notes. The executable plan is `svread/SEO-GEO-PLAN-2026-11-08.md`.*

*Goal: make svread's claims useful to Google AI (AI Overviews / AI Mode) and
ChatGPT **without** a custom MCP connector. Research-backed, with sources.*

---

## 0. The one finding that governs everything

**GEO cannot create discoverability.** The 2026 critical survey (40 studies)
concludes: *"already-retrieved content can causally alter its citation or
use, but no reviewed technique shows [improved] retrieval probability."*
(arXiv:2607.14035 §Abstract.)

Translation: no amount of rewriting gets us into the candidate set. **Being
indexed and snippet-eligible is the gate** (Google says this verbatim:
*"a page must be indexed and eligible to be shown in Google Search with a
snippet… there are no additional requirements"*). Everything below is
optimisation *after* that gate. Today `site:svread.pages.dev` = 0, so the
gate is shut and no GEO tactic can matter yet.

Two stages, both measurable:
- **Stage A — retrieval visibility**: are we in the candidate pool at all?
  (indexing, ranking, entity presence)
- **Stage B — citation visibility / absorption**: given two candidates, which
  gets cited, and how much of its language survives into the answer?

---

## 1. What the papers say (and what each means for us)

| Source | Finding | What it means for us |
|---|---|---|
| **GEO** — arXiv:2311.09735 (KDD'24) | 9 tactics on 10k queries. Best: **Quotation Addition** (+41% position-adjusted words), **Cite Sources**, **Statistics Addition**. Keyword stuffing **hurts** (−). | We are almost perfectly built for the winners: we have quotations (Sanskrit spans), citations (source bytes + hashes), and statistics (counts, verdicts). Do **not** keyword-stuff. |
| **Critical survey** — arXiv:2607.14035 (2026) | Terminology inconsistent; evidence narrow; retrieval ≠ citation. Proposes visibility vector (discoverability, citation, absorption, economics). | Adopt their vector. Never report "cited" as "useful". Our ontology already separates these — align it to theirs. |
| **What Gets Cited** — arXiv:2605.25517 (SIGIR'26) | 252k paired trials: **content completeness and trust cues** dominate; **formatting-only edits barely move anything**. | Our differentiator IS a trust cue (hashes, verdicts, limits). Surface it *in the text*, not just in JSON. |
| **GEO-SFE** — arXiv:2603.29979 | Structure at three levels (macro/meso/micro) lifts citation 17.3%. | One page per claim; clean H2s; one answer per section; no 10-question pages. |
| **Citation Selection → Absorption** — arXiv:2604.25707 | 602 prompts across ChatGPT/Google/Perplexity. High-influence pages are *longer, more structured, richer in extractable evidence (definitions, numbers, comparisons, steps)*. ChatGPT cites fewer but absorbs more. | Give extractable units: definition, count, hash, comparison, procedure. |
| **Understanding ChatGPT Citations** — arXiv:2610.15382 | Retrieval ≠ citation. Rewritten queries, run-to-run variance. **Hostname- and entity-level presence matter**, not just exact URLs. | Build a clear entity (consistent name, About, sameAs). Measure at host level. |
| **LIVE-GEO** — arXiv:2611.01126 | Tests whether GEO gains survive on the live web. | We must measure in the wild, not in a toy context. |
| **GEO-PTBR replication** — 2026 | Effects **do not reproduce** across engines; keyword stuffing −9.8%, *easy-to-understand −5.4%*. Some tactics are net negative. | Treat every tactic as a hypothesis with a kill criterion. Do not dumb down the Sanskrit. |
| **Google AI features docs** (Search Central) | Indexed + snippet-eligible; no special schema/markup; no `llms.txt` requirement. | SEO fundamentals first. Schema helps understanding, not eligibility. |
| **llms.txt v2** (Howard, rev. 2026-08) | Adds `rel=alternate type=text/markdown` and `rel=describedby`; per-path scoping. Google's Mueller: no AI system uses llms.txt; 2026 data shows no citation uplift. | Keep llms.txt for **agents**, not for Google. Zero cost, zero Google benefit. |

---

## 2. GitHub tools worth reading (not necessarily vendoring)

| Repo | Use |
|---|---|
| `GEO-optim/GEO` | Reference implementation + GEO-Bench (10k queries, HF `GEO-Optim/geo-bench`). The evaluation harness to copy, not the content rewriting. |
| `glad-lab/geobench` | Unified re-evaluation of 9 GEO methods; good for comparing tactics honestly. |
| `cxcscmu/AutoGEO` (ICLR'26) | Learns engine preference rules and rewrites. Useful to *understand* what engines reward; risky to apply blindly (PT-BR shows non-replication). |
| `AIcling/agentic_geo` | Content-adaptive strategy selection; same caveat. |
| `geo-team-red/geo-optimizer` (Go) | Clean taxonomy of strategies: Structure / Schema / AnswerFirst / Authority / FAQ. Steal the taxonomy. |
| `duducat2026/geo-optimizer` | Crawl-and-score across 11 engines + index check. Useful shape for a **self-audit** script. |
| `agentmarkup.dev` CLI | Generates llms.txt, markdown mirrors, JSON-LD, AI-crawler robots, `_headers`, and gates CI. Directly reusable as a build step. |
| `NicoAcosta/llm-seo` | Agent skill: 5-phase checklist. Good as the audit checklist. |
| `afdocs.dev` checks | Weighted, practical discoverability checks (llms.txt, markdown availability, directives). Test our site against it. |
| `modelcontextprotocol/*` | Only if we later do the MCP route (out of scope for this doc). |

---

## 3. The plan for svread (no MCP, no connector)

### Phase A — get into the index (the actual blocker)
1. **Server-rendered, per-claim HTML.** One URL per chunk: `/claim/<work>/<target>`. Content in **initial HTML**, no JS. (Google reads the first response; our reader is JS-heavy today.)
2. **Sitemap** with `<lastmod>`; submit in Search Console. Existing sitemap lists 10 lessons; it needs the claim pages.
3. **robots.txt** allow Googlebot, Bingbot, OAI-SearchBot, GPTBot, ClaudeBot, PerplexityBot. Keep `Google-Extended` a separate decision (training ≠ inclusion).
4. **IndexNow** ping for Bing/Copilot.
5. **Entity clarity:** one canonical site name + About page + `sameAs` (GitHub, DOI, Wikidata if any). ChatGPT study says hostname/entity presence matters more than exact URL.

### Phase B — be the citable candidate (tactics that fit our assets)
6. **Answer-first blocks.** Each claim page opens with one sentence stating the claim and its status, e.g. *"Tantrasāra 8.3: all deterministic checks pass; the 36-tattva count is model-checked inside a finite model; no manuscript witness is verified (0 corpus-wide)."*
7. **Statistics Addition (safe form).** We already have real numbers — 157 theorems, 16/154 chunks, 909 traces, 0 witnesses. Use them. Never invent statistics; that is the PT-BR failure mode.
8. **Quotation Addition.** Lead with the Sanskrit span as a `<blockquote cite>` plus the translation. This is the single strongest documented tactic and it is literally our data.
9. **Cite Sources.** Link the edition (GRETIL/KSTS) with its licence, and the exact bytes. Note rights honestly (GRETIL is NC).
10. **Extractable units.** Definition block, count table, comparison table (claim vs what would falsify it), and the verification procedure as numbered steps — the four things the absorption paper says high-influence pages have.
11. **Schema.org:** `Dataset` for the corpus, `Article`/`Claim` graph per page, `FAQPage` where a page genuinely answers questions, `Speakable` on the answer-first paragraph. Remember: schema helps understanding, **not** eligibility.
12. **Honesty as a trust cue.** State the limits *in the text*: R-tier, UNPINNED witnesses, gate BLOCKED where true. The "What Gets Cited" result is that trust cues matter; a page that states its own limits is the strongest cue we have that nobody else in this niche has.

### Phase C — agent lane (cheap, non-Google)
13. `llms.txt` + `llms-full.txt` + `.md` mirrors + `rel=alternate` (v2 spec). Costs a build step; helps Claude/Cursor/agentic tools; **does not** help Google.
14. Add `/.well-known/ai-catalog.json`-style capability description pointing at the trace index and packs.

### Phase D — measure (or it is astrology)
15. **GEO-Bench-shaped harness of our own:** 50–100 real questions a reader would ask ("what does tantrasāra say about the 36 tattvas", "is the svread translation of X verifiable"). Run weekly across ChatGPT web search, Google AI Mode (via SERP), Perplexity.
16. Record per run: **retrieved? cited? absorbed?** (presence of our phrasing), at **hostname and exact-URL** level. Two runs minimum — the ChatGPT study shows run-to-run variance is large.
17. Kill criteria per tactic: if a change does not lift citation rate over 3 runs beyond the noise band, revert it. PT-BR says several popular tactics are negative.

---

## 4. What NOT to do
- Do not keyword-stuff (−9.8% measured).
- Do not "simplify" the Sanskrit into plain English to please an optimiser (easy-to-understand was **negative** in replication).
- Do not claim `llms.txt` improves Google citation (it does not; 2026 data).
- Do not treat "ChatGPT mentioned us" as verification. That is `MODEL_CITED`, a weaker class than `SOURCE_READ`, far weaker than `TASK_VERIFIED`.
- Do not publish a "statistics addition" we cannot source. Every number on a page must come from `freshness.json` or a trace.

---

## 5. Immediate next actions (ordered)

| # | Action | Effort | Depends on |
|---|---|---|---|
| 1 | Generate `/claim/<work>/<target>` HTML from the 909 traces (server-rendered, answer-first, span + hash + verdict + limits) | 1 day | — |
| 2 | Add them to `sitemap.xml` with `lastmod`; robots allow the AI crawlers | 1 hour | 1 |
| 3 | Owner: Search Console verify + sitemap submit; IndexNow key | 15 min | 2 |
| 4 | Entity block: About + `sameAs` + consistent name | 2 hours | — |
| 5 | `agentmarkup`-style build step: llms.txt / llms-full.txt / .md mirrors / JSON-LD / `_headers` | half day | 1 |
| 6 | Measurement harness (50 questions × 3 engines × 2 runs) with host-level + URL-level scoring | 1 day | 3 |
| 7 | First tactic experiment: answer-first vs current, measured | 1 week of runs | 6 |

**Definition of done for the whole plan:** a stranger's AI search cites a
specific svread claim page, and that page's own text tells the reader the
claim's status and how to check it. Citation without the status is worse than
silence.
