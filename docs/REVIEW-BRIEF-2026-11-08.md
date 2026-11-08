# REVIEW BRIEF — external agent review packet (2026-11-08)

*This PR exists so an external agent can review the current state without
reading 40 docs. It is deliberately written by the author and therefore
biased: trust the commands in §1, not the prose. Repos are public.*

**Reviewed head:** trika-x `main` @ `1c6f16f` (tag
`checkpoint-2026-11-08-lead-review`). svread `main` @ `2aeb2bb`.

---

## 1. Verify first (5 minutes)

```sh
git clone https://github.com/prx0r/trika-x && cd trika-x
python3 -m unittest discover -s formal-trika/tests        # 94 OK
python3 formal-trika/tools/evidence_check.py              # 157/155, 16/154
python3 formal-trika/tools/freshness.py --check           # SHARP
python3 tools/mcp_catalog.py --check                      # SHARP, 104 tools
python3 formal-trika/tools/essay_derive.py                # 6 PARTIAL, 0 BROKEN
python3 formal-trika/tools/table.py --check && python3 formal-trika/tools/axiom_audit.py --check
```
Note: `freshness.py --check` compares against a ledger captured on the author's
box; in a clean clone, DB/bridge/svread entries will report BLOCKED or drift —
that is expected, not a failure. The static gates (tests, table, evidence's
chunk-ref resolution) are the ones that must pass anywhere.

Then:
```sh
cd ../openpatala && git clone https://github.com/prx0r/openpatala && python3 check.py
cd ../svread && git clone https://github.com/prx0r/svread && node --test tests/*.cjs
str=$(curl -s https://svread.pages.dev/data/traces/index.json | python3 -c 'import json,sys;print(json.load(sys.stdin)["count"])')
echo "live traces: $str   # expect 909"
```

---

## 2. What this PR asks you to review

1. **Is the formal work honest?** `formal-trika/control/*.lean`, preregs in
   `formal-trika/PREREGISTRATION-*.md`, readings in `TABLE-READINGS.md`.
   Every theorem is a finite count over a *held layer* (ARGMAP/C1), tier R,
   with a single-line must-fail twin. The correction at
   `formal-trika/PREREGISTRATION-VBT1-CORRECTION-2026-11-08.md` documents a
   case where the layer and the verse disagree. **Question for you: is
   count-over-layer worth calling formalisation at all, or should the R tier
   be renamed to something less load-bearing?**
2. **Is the trace system sound?** `formal-trika/tools/trace_bundle.py`
   (assurance dimensions), `trace_all.py`, `tests/test_trace_bundle.py`.
   Specifically: it now compares every canonical field on verify, joins
   theorems on `(work, locator)`, and marks formal `REGISTERED` not
   `MODEL_CHECKED`. **Try to break it.**
3. **Is the essay gate actually a gate?** `essay_check.py`,
   `essay_derive.py`, `tests/test_essay_check.py` (7 forgery cases),
   `tests/test_clean_checkout.py`. Known weakness: `essay_derive` checks
   chain existence and verse ranges, not meaning.
4. **Is the publishing claim true?** The live site must show 909 traces, the
   verify footer, and packs carrying `assurance.chunk_gate`. It did not
   before this session — see finding F4 in
   `docs/log/LEAD-REVIEW-2026-11-08-FULL.md`. **Re-check it.**
5. **Lead review:** `docs/log/LEAD-REVIEW-2026-11-08-FULL.md` — 5 findings,
   3 fixed, 2 open. Disagree with any ruling and say why.

Read order: `DOCS.md` → `MASTERPLAN2.md` §0–2, §12, §16–17 → `SYNERGY-CHAIN-2026-11-08.md` §1–2 → the lead review.

---

## 3. NOT DONE — with links

Each of these is a real gap. None is hidden in prose.

### 3a. Blocked on a human (owner)
| Gap | Where | Note |
|---|---|---|
| Zenodo DOI | `docs/log/ENDGAME-RECIPES.md`; `MASTERPLAN2.md` Q12 | token needed; **and a DERIVED essay exemplar first** |
| Token rotation | `ROTATION-CHECKLIST-2026-11-08.md` | R2 / OpenCode Go / Cloudflare keys were pasted in chat |
| **Revoke leaked credentials** | `visuals` dump (excluded from public branch) | `ghp_FFbi…`, Google `AIzaSyA7…`, an OpenRouter key, private keys. Found during publishing. **Assume burned.** |
| Search Console + outreach | `MASTERPLAN2.md` Q16 | site is not indexed; `site:svread.pages.dev` = 0 |
| dīkṣā policy | `MASTERPLAN2.md` Q19 | practice stays STUDY-only until ruled |
| Recipes R1/R7/R8 | `trika-x/ENDGAME-RECIPES.md` | spec only; diary consent paths unbuilt |
| Disk Tier 2/3 | `docs/log/PROCESS-NOTES-2026-11-08.md` §11–12 | kashaudio `.git` 1.1G of committed mp4s; `~/.cache/ms-playwright` 924M |

### 3b. Blocked on the scholar channel
| Gap | Where | Impact |
|---|---|---|
| P-TK1 ruling | `formal-trika/PTK1-REVIEW-PACK.md` | first scholar-signed formal claim |
| rater-2 pass | `formal-trika/T-C2-RATER2-SHEET.md` | T-C2 criteria have no empirical bite yet |
| second-encoder twin review | `docs/log/LEAD-REVIEW-2026-11-08-FULL.md` R2 | **blocks any promotion above R** |
| NGMPP witness path | `formal-trika/bridge/witness-candidates.json` | witnesses are 0 corpus-wide |
| KMT filename + Dyczkowski collation | `docs/log/DECISION-PACKET-2026-11-06.md` §9 | frontier sprints blocked |

### 3c. Blocked on other lanes (I filed asks; they dispose)
| Gap | Where | Ask file |
|---|---|---|
| `phrdaya` ledger spans (PR #7 P0) | `translation-work/phrdaya/passages.jsonl` | `LANE-ASKS-2026-11-08.md` §2 |
| svread formalized/MODEL_CHECKED | fixed in `svread` this session; re-audit | same file §3 |
| sanskritbench result_id | fixed in `box/diagnostics-v2`; **lane must re-pin** | same file §1 |
| openpatala read-only check | fixed in `box/check-readonly`; **lane must merge** | same file §4 |
| ipvv two-sources-v2 | ready in `box/two-sources-v2`; **lane must merge** | same file §5 |
| translation decision trail | ready in `box/decision-trail`; phrdaya rows written | process notes §18 |
| video `evidence_refs` | `videofactory` lane | `MASTERPLAN2.md` Q17 |
| nibbanahelp N1 exporter | `nibbanahelp` lane | `MASTERPLAN2.md` Q18 |
| syllabus C1–C4 | satsang practice lane | `MASTERPLAN2.md` Q19 |

### 3d. Blocked on quota / GPU
| Gap | Where | Note |
|---|---|---|
| tau scale-up (n≥30, Wilson) | `sanskritbench` | 3×3 smoke returned all-undefined (run `54b08b41`) |
| gate calibration tuning | `formal-trika/data/calibration-gate-v1.txt` | false-PASS on truncated text = **0.885** |
| COMET / learned metrics | — | needs torch/GPU box |
| continuous propose loop | `formal-trika/tools/roboscholar.py` | 1 pilot only |
| ML grammar tab | `svread` Sanskrit view | Vidyut/ByT5 need toolchain |

---

## 4. MESSY — needs tidying or a decision

| # | Mess | Where | Suggested |
|---|---|---|---|
| M1 | `phrdaya` ledger claims 1–4 sūtras, holds 1 | `translation-work/phrdaya/passages.jsonl` | lane + Sanskrit reviewer; until then every phr trace inherits the flaw |
| M2 | translation-work `check.py` fails 20 pre-existing items | `translation-work` s01–s20 proof files | not mine, untouched; lane must triage |
| M3 | "COMPLETE" trace verdict name still implies finality | `trace_bundle.py` | renamed semantics are in `assurance`; consider `LINKS_COMPLETE` |
| M4 | freshness ledger is not exhaustive | `formal-trika/data/freshness.json` | add chunk-verse (105), crux queue (882), packets (8), decision coverage (3/87, 2/87) |
| M5 | ~27 root docs still large even after the tidy | `DOCS.md` §2 | consider `docs/spec/` next |
| M6 | many docs cite bare filenames without paths | repo-wide | markdown links are clean (0 broken); bare refs are unverifiable |
| M7 | decision coverage is 3/87 ledgers, 2/87 layer-accept | `decision_check.py` | needs ingest adoption across works, not a tool |
| M8 | chunk↔verse: 23 CLOSED / 64 OPEN | `formal-trika/bridge/chunk-verse-map.json` | 64 need manifests or verse-id fixes in the lane |
| M9 | 153MB verify packs in svread | `svread/data/verify/` | consider R2 hosting + pointer; repo is heavy |
| M10 | deploy is manual and easy to forget | `svread/deploy.sh` | add a CI deploy job or a release checklist |
| M11 | 15:49 swarm expansion runs committed as data | `formal-trika/swarm/` | historical; no one should rebuild on them |

---

## 5. NEEDS INSIGHT — open design questions

1. **Can count-facts ever leave R?** If a verse says "ninefold" and we prove
   `length = 9` over a roster, is that a theorem about the text? PR #7 says no.
   If no, what *would* a legitimate T-tier formalisation look like — and does
   the grammatical-relations model PR #7 demands have a tractable encoding?
2. **Trace completeness semantics.** Is the right answer `LINKS_COMPLETE` /
   `SPAN_VERIFIED` / `REVIEWED` as separate booleans, or one status lattice?
3. **DERIVED essay definition.** What exactly must be true before an essay is
   DERIVED — chain only, or chain + verified spans + reviewed claims? This
   gates the DOI.
4. **Split formal registry from bridge snapshot?** (PR #7 R7, unresolved.)
5. **Tau without a GPU box.** Is chrF + gate + a small human gold set enough
   to claim calibration, or is tau theater without learned metrics?
6. **Rights at scale.** MITRA share-alike and GRETIL non-commercial both feed
   L0 grounds. What is the bulk-derivation boundary? (PR #7 R10.)
7. **Publishing architecture.** 153MB of packs in git will not scale to the
   full corpus. R2 + signed manifests? Content-addressed CDN?
8. **Where does the teacher live?** nibbanahelp prototype vs Scholar accounts —
   one consent model or two?

---

## 6. Links index

- trika-x: https://github.com/prx0r/trika-x (main @ `1c6f16f`)
- openpatala: https://github.com/prx0r/openpatala · branch `box/check-readonly`
- svread: https://github.com/prx0r/svread (main @ `2aeb2bb`) · live https://svread.pages.dev
- translation-work: https://github.com/prx0r/translation-work · branch `box/decision-trail`
- sanskritbench: https://github.com/prx0r/sanskritbench · branch `box/diagnostics-v2`
- ipvv: https://github.com/prx0r/ipvv · branch `box/two-sources-v2`
- visuals (snapshot, secrets excluded): https://github.com/prx0r/visuals · branch `box/workspace-snapshot-2026-11-08`
- Live verification entry: https://svread.pages.dev/?view=verify

*If a claim here does not reproduce, that is the finding. Say so loudly.*
