# PR DESCRIPTION (draft — update counts + CI run at push time)

*Target: `main`. Source: `box/peer-review-batch`. This branch is one review
unit per PR #7 §5 checkpoint 2: it does not claim a merged release, only a
reviewable diff. Regenerate the numbers below with the commands in §4 before
opening the PR.*

## What this PR is

Eight concerns, in dependency order. Reviewers can take them independently;
nothing later is needed to judge anything earlier.

| # | Concern | Files | Content |
|---|---|---|---|
| 1 | Formal rungs | `formal-trika/control/` (13 files), `formal-trika/tests/` (+5), `TABLE*`, `EVIDENCE.json` | P-PHR4/P-PHR5 (phr-p05), P-VBT1/P-VBT2 + must-fail twins, TABLE readings, EVIDENCE entries; harness receipts in `runs/runs.jsonl` |
| 2 | Trace system | `formal-trika/tools/trace_bundle.py`, `trace_all.py`, `tests/test_trace_bundle.py`, `tests/test_clean_checkout.py` | 909 trace bundles with separated assurance dimensions; full-compare verifier; fixture suite |
| 3 | Treeka + derive | `formal-trika/tools/treeka{,_report}.py`, `essay_derive.py`, `tests/test_treeka_report.py`, `data/treeka.json` | Gap report, essay-derivation audit (6/6 PARTIAL, 0 BROKEN), cross-check test |
| 4 | Essay gate + review flow | `formal-trika/tools/essay_check.py`, `tests/test_essay_check.py`, `formal-trika/swarm/review-packets/` (7) | Forgery-closed gate, READY_FOR_HUMAN_REVIEW wording, queued review packets |
| 5 | MCP federation | `formal-trika/tools/federation_gateway.py`, `tools/mcp_catalog.py`, `tools/federation_pretest.py`, `../../../MCP-OPS.md`, specs | 104 tools / 8 families, machine catalog, guide-prefix tests |
| 6 | Freshness + portability | `formal-trika/tools/freshness.py`, env overrides in lane tools | Canonical-number ledger, drift gate, no hardcoded paths in gated tools |
| 7 | Corpus data (generated) | `formal-trika/data/traces/` (909), `data/crux-queue.jsonl`, `data/treeka.json` | Machine-regenerated indexes; reproduce with the commands in §4, do not review line-by-line |
| 8 | Research mirrors + plans | `formal-trika/imports/` (ochema, geometryofthinking + miners), `*.md` plans/notes/reviews | Frozen reading mirrors with provenance; dated process notes, MASTERPLAN2, SYNERGY-CHAIN, MCP-OPS, STATUS, HANDOVER |

## What this PR explicitly does NOT do

No signoffs. No publication. No witness claims (0 corpus-wide, enforced).
No Core promotions (`review_status`: 0 Core / all Frontier). No auto-anything.
No writes into other lanes. No history rewrites.

## Verification (paste output into the PR body)

```sh
python3 -m unittest discover -s formal-trika/tests        # 80 OK
python3 formal-trika/tools/evidence_check.py              # 157/155, 16/154
python3 formal-trika/tools/table.py --check               # rc=0
python3 formal-trika/tools/freshness.py --check           # SHARP
python3 tools/federation_pretest.py                       # GREEN
python3 tools/mcp_catalog.py --check                      # SHARP (104)
python3 formal-trika/tools/essay_derive.py                 # 6 PARTIAL, 0 BROKEN
python3 formal-trika/tools/essay_check.py --all           # READY_FOR_HUMAN_REVIEW
```

## Regenerate counts (run at push time)

```sh
git diff --numstat origin/main..HEAD | awk '{a+=$1; d+=$2} END {print a, d}'
git diff --name-only origin/main..HEAD | wc -l
git log --oneline origin/main..HEAD | wc -l
```
