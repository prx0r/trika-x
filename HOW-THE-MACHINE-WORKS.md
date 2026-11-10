# How the machine works

*One document that explains the whole estate to a smart stranger. Every
number measured on box 2026-11-10; reproduce with the commands given.*

## The problem

Trika Shaivism has ~555 catalogued works, centuries of commentary, and no
machine-checkable record of who translated what from which bytes. A reader
cannot tell a verified reading from a confident guess, and an AI that quotes
us cannot show its work. This machine exists to fix exactly that — not by
being authoritative, but by being **checkable**: every claim names its
source bytes, its gate status, and a hash anyone can recompute with
`curl` + `sha256sum`, no account, no code.

## The loop (one event order, never mixed)

```
manuscript → openpatala (which work/edition is this? 555 works · 909 passages · 0 witnesses)
  → translation-work (evidence layers T1→L0→argmap→L2→C1→L3→L4, one sha per layer)
  → trika-x formal (theorems in Lean + must-fail twins + EVIDENCE + TABLE)
  → trace bundle + verify pack (bytes + hashes + verdict, per chunk)
  → svread (reader + scholar + chat + claim pages: the checkable surface)
  → scholar MCP → essay (claims → audit → PUSHBACK → human sign; 33 tools)
  → release → Zenodo DOI → factories (video/book; evidence_refs required)
```

Every hop carries **bytes + hash + status + where-to-refetch**. A hop that
cannot name its input fails closed. BLOCKED is never PASS. PARTIAL is never
COMPLETE. R-tier never promotes itself. No auto-sign, auto-publish, or
auto-anything — the machine proposes, a human disposes.

## What "formal" actually proves (and what it doesn't)

The method is ported wholesale from Thon Ly's executable Abhidhamma work
(`lead-pack/01-reference-thonly`: prereg → controls → mutation tests →
verdicts plain; his TK-C2 twin is our must-fail-twin template; his system:
71 Lean files, CI-checked, Zenodo DOI 10.5281/zenodo.23067241).

What trika-x proves today (157 theorems, Lean 4.34.1, receipts exit 0):
finite-model regenerations of traditional counts — e.g. 7 well-formed
experients from 8 mala-axis combos, the five-kañcuka reckoning — inside
explicitly bounded models, **plus** a mutated twin that must fail (an
anti-vacuity check: a model that proves everything proves nothing).

What it does NOT prove: that a reading is true, that a translation is
correct, that any witness exists, or that one doctrine entails another.
Registry references are explicitly "not independently verified entailments"
(`evidence_check.py` says so on every run). Coverage is 16/154 chunks (10%);
authority is 0 Core / 157 Frontier until scholars rule. The twin is a
refusal check, not a semantic validation; second-encoder review blocks any
promotion above R.

This is the same scope discipline as Thon Ly's ("letting the texts lose"):
formalize without smuggling readings. The ratio — rules that regenerate
counts — is the finding. Everything else is honest labels.

## The moat: 909 traces

For every ledger passage there is a `trika-trace/1` bundle: source bytes →
layer hashes → gate verdicts → formal refs → citing essays, hash-pinned
(236 COMPLETE / 673 PARTIAL, every PARTIAL naming its gaps). An outsider
reproduces every hash without our code. The verify packs publish the exact
bytes. This is the one thing no competitor has: checkability without
trusting us.

## The surface: 909 claim pages

One pre-rendered page per trace (`/claim/<work>/<target>/`): answer-first
verdict (≤40 words, machine-enforced), the hashed excerpt (IAST; no
Devanagari or English is ever fabricated — 777 pages withhold honestly),
claim table, what-it-does-NOT-establish, verify steps, hash block, chain
table, citation, provenance. JSON-LD mirrors the visible answer
byte-for-byte; `reviewedBy` stays null until a human signs. Sitemap lists
all 1,919 URLs; robots welcomes indexers and AI crawlers. `llms.txt` is for
agents (Google ignores it — measured, documented, not claimed otherwise).

## The gates (run these; they outrank every doc)

```sh
cd /root/openpatala && python3 check.py            # GREEN + 2 recorded BLOCKED
cd /root/trika-x && python3 -m unittest discover -s formal-trika/tests  # 94 OK
python3 formal-trika/tools/evidence_check.py        # 157/155+2, 0 bad refs
python3 formal-trika/tools/freshness.py --check    # SHARP
python3 tools/mcp_catalog.py --check               # SHARP (104 tools, 8 families)
cd /root/svread && python3 tools/seo_check.py      # 10/10 GREEN
node --test tests/*.cjs                             # 51 pass, 0 fail
python3 -m unittest discover -s mcp -p "test_*.py" # 40 OK
```

MCP, live-proven 2026-11-10 (`trika-x/testing/logs/MCP-live-proof.log`):
handshake → tools/list (5 tools) → `resolve tantrasara` → EXACT hit from
the live DB → health counts match. Federation: 104 tools across 8 families,
dead child fails open, unknown tool errors clean (`-32601`).

## What's openly not done

Formal 10% · 0 Core (needs P-TK1/ti-ca/rater-2) · witnesses 0 (NGMPP eyes) ·
0 DOI (Zenodo token + DERIVED exemplar first) · bench tau scale (quota/GPU) ·
Treeka reader view · Sanskrit slice · N1 exporter · C1–C4 · recipes R1–R8
(consent-gated); R9 movies explicitly NOT YET · Search Console/outreach/
inbound links · chunk↔verse 64 OPEN · decision-trail ingest wiring ·
translation-work proof harness red (their 1-line stdout bug, filed, untouched
— bridge bytes we consume are GREEN) · disk 96% (1.2G reclaim needs owner go)
· geo_measure baseline (no tactic claim licensed without it).

## Where to read next

- Build/deploy/ops: `svread/PRODUCTION.md`
- Execution order: trika-x `MASTERPLAN2.md` (+ `DOCS.md` map)
- Composition rules: `SYNERGY-CHAIN-2026-11-08.md`
- Per-artifact status: trika-x `STATUS.md`
- Red-team evidence: `trika-x/testing/` (20 probes, battery, reports)
- Review contract: re-run the gates above, then rule in a new dated file.
  A number that doesn't reproduce is the highest-severity finding here.
