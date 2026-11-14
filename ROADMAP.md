# ROADMAP — from verified library to authoritative Trika source
*Status: CANONICAL. Five rungs with done-gates; 'actually are' verified 2026-11-14.

*2026-11-07. Written after a measured audit (see MODULES.md for current state).
Each rung states the gate that marks it done. Nothing here is claimed done.*

## Where we actually are

- 1034 works identified · 87 with passage ledgers · 72 gold in translation-work
- 50 works readable on the site · 55 with a scholar projection
- 206 Lean theorems · 16/154 chunks formalised · **909 trace bundles** published
- **0 witnesses** — nothing is witness-grade yet
- LLM-legible: llms.txt, sitemap, robots, JSON-LD, formal registry, 909 traces
- **Independently verifiable**: any outsider can confirm our chains with
  `curl` + `sha256sum` and nothing else (proven live)

That last line is the thing nobody else in this space has. "Authoritative"
does not mean "biggest" — it means *checkable*. Everything below extends
checkability to more claims, never adds unverifiable volume.

## The five rungs

### R1 — Make every readable work verifiable ✅ (met 2026-11-08)

*Now:* all **909/909** ledger locators have a trace bundle (236 COMPLETE /
673 PARTIAL, every PARTIAL naming its gaps) and 909 verify packs are published
live. 50 works are readable on the site.
*Remaining:* the public reader still lists traces per work; the new per-claim
pages (see `svread/HANDOVER-SEO-2026-11-08.md`) close the presentation gap.

- Generate a trace for **every chunk in every readable work** (909 passages).
  Most will be PARTIAL (no formal theorem) — that is fine and honest; the
  source + layers + proof hops still verify.
- Publish verify packs for all of them.
*Gate:* `data/traces/index.json` covers ≥90% of passages in readable works,
and every pack reproduces its trace. — **MET: 100% coverage, packs re-verified
at publish time (`emit_traces.py --check`, `emit_verify.py --check` GREEN).**

### R2 — Close the witness column (the thing that makes us citable as primary)

*Now:* witnesses 0. Editions are candidate strings.
*Gap:* no manuscript records. This is the only rung that needs a human with
archive access.

- NGMPP / microfilm verification for the core works (Tantrasāra, Tantrāloka,
  Paramārthasāra, IPVV, Vījanabhairava).
- Record the witness → surrogate → transcription ladder per work, with
  UNKNOWN kept where unknown.
*Gate:* at least one work where `witness.status` is `VERIFIED` with a real
shelfmark, and the trace's source hop cites it.

### R3 — Extend formalisation along the gap list (never by taste)

*Now:* 16/154 chunks formalised (10%).
*Gap:* 138 chunks unformalised; the list is published in `data/formal.json`.

- Work the gap list in order: phr mala rows → VBT clusters → tsa08 remaining.
- Each new theorem: prereg → model → must-fail twin → EVIDENCE → TABLE →
  run receipt. No exceptions.
*Gate:* formal coverage >50% of gold chunks, every theorem with a run receipt,
and the gap list still published (not quietly deleted).

### R4 — Make the chat answer with verifiable citations

*Now:* chat answers from gated passages with citations, but a citation is a
mention, not a verified claim.
*Gap:* no runtime link from an answer to a trace + pack.

- When the chat cites a chunk that has a trace, return the trace URL and the
  pack URL alongside the citation, so the reader can check it in one click.
- Where no trace exists, say so: "unverified — no trace for this chunk".
*Gate:* every chat answer citing a trace-bearing chunk includes a working
verify link; answers citing untraced chunks say "unverified".

### R5 — Earn the inbound links that make Google cite us

*Now:* not indexed at all (`site:svread.pages.dev` = 0 results).
*Gap:* no inbound links, no Search Console, no authority.

- Search Console: verify, submit sitemap, confirm generative-AI setting.
- One link from a recognised Trika resource (academic page, Wikipedia
  external link, Hareesh/tantra.org outreach) — a link earns more than any
  technical file.
- Keep fan-out coverage: one page per question shape, interlinked.
*Gate:* `site:` returns pages; Search Console shows impressions; at least one
external referring domain.

## What NOT to do

- Do not inflate "101 works" into "101 complete translations". 50 are
  readable, 72 are gold at layer level, and every one still says
  machine-proposed until signed.
- Do not claim a witness. Zero exist. Say so.
- Do not add works to improve a coverage number. Coverage is reported with
  denominators and gaps, never as a headline.
- Do not let llms.txt carry claims the data does not back. It now states
  measured counts; keep it that way (`tests/wiring.test.cjs` enforces it).
- Do not build a second identity system. openpatala is the root.

## The one-line definition of done

An outsider, with no account and no code, can take any claim we publish, fetch
its trace and its bytes, recompute the hashes, and see the same numbers we do —
and where we could not verify something, we said so first.
