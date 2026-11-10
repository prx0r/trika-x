# PUBLISH PATH — draft to DOI (measured 2026-11-10)

How an essay (or enquiry-derived draft) gets published, step by step with
the command or click for each. Machine steps are done or runnable; human
steps are named with who must act. Nothing auto-publishes, ever.

## Inventory (what exists today)

| Item | Where | Machine state 11-10 |
|---|---|---|
| 6 expansion essays (tsa08-p01/p02/p03, tal-a34-p01) | trika-x `formal-trika/swarm/expansion-*.md` | claims PARTIAL (2–5 structural blocks each); mock PUSHBACK filed; **live cross-family PUSHBACK filed 11-10** (`*.pushback-live.md`, deepseek, 8–9 claims → 1 objection each) |
| robo drafts (tsa08-p02 today, tsa08-p01/p04, param-p02 earlier) | same dir (`robo-*.md` + receipts) | claims + audit receipts filed; param-p02 has pushback |
| 22 ipvv essays | ipvv `site/data/essays/*.md` | published as web pages (no DOI); audit state per essay varies |
| 115 pushing probes | svread `data/pushing.json` + ipvv corpus | live enquiries with hound verdicts (probes, not essays) |
| Scholar workspace drafts | svread MCP (`save_document`, 56 work projections) | account-scoped, unreviewed until requested |

## The 7 steps (Variety-1 closure)

1. **Draft exists** — machine (roboscholar/expansion) or human (Scholar UI, `save_document`). Done for items above.
2. **Claim table** — `essay_derive.py` / `claims.link`. Done (all PARTIAL, blocks named).
3. **Audit** — `audit_draft` (quotes vs supplied sources). Done via roboscholar receipts; run `scholar: audit_draft` for Scholar-UI drafts.
4. **PUSHBACK destroy pass** — mock (deterministic, offline) + live cross-family (opt-in quota). **Done 11-10 for all 6 expansions + param-p02.** Reports never edit drafts.
5. **Human sign-off** — `POST /api/scholar/signoffs` in a logged-in Scholar session: pick the exact document revision, declare rights, `confirm_submission: true`. Creates `signoff:<uuid>` bound to the snapshot sha. **OWNER/SCHOLAR ACTION. Non-delegable by design.**
6. **Bridge** — signed payload (HMAC, `scholar-bridge/v1`) → git identity (frozen revision + signoff id). Semi-automatic after step 5; needs the worker route + a committer.
7. **Zenodo DOI** — needs (a) owner token → `/root/.zenodo-env` (600, never in repo), (b) DERIVED exemplar first (Q12 gate), (c) human-approved licence (recommend CC BY 4.0 for signed essays, author decides). Then: build bundle (exact revision + trace packs + receipts + rights file) → dry-run → publish → record DOI back into the essay projection. **Token + licence = owner; bundle + submit = machine once token exists.**

Recommended first candidate: `expansion-node1-tattva` (fewest blocks: 2) — but the scholar picks; smallest-blocking is a machine heuristic, not a quality judgment.

## Zenodo metadata template (fill at release time)

```json
{
  "title": "<essay title> — Svatantrya Scholar essay",
  "creators": [{"name": "<signing scholar>", "affiliation": "independent scholar"}],
  "description": "Machine-proposed draft, human-signed. Assurance at signing: <witness UNPINNED / formal UNBOUND / review SIGNED / publication AUTHORIZED>. Verify: <trace URLs>. Method: <repo + rev>.",
  "license": "<author-chosen, e.g. cc-by-4.0>",
  "related_identifiers": [{"relation": "isSupplementTo", "identifier": "<trace bundle URL>"}],
  "version": "doc-rev-<n>+git-<sha>"
}
```

## Enquiry pathways (pushing/chat) → essays

Pushing probes and chat threads are *inputs*, not publications: a probe with a GEM/RESOLVED verdict + a scholar's decision can seed an essay draft (`draft_with_qwen` with `consent_to_ai`, excerpt-capped), which then enters step 2 above. Nothing flows automatically; the scholar's explicit selection is the gate every time (MCP enforces it).

## What I did 2026-11-10

Mock PUSHBACK on all 6 expansions (baseline, offline) + live deepseek PUSHBACK on all 6 + robo draft cycle on tsa08-p02 (2/3 cited, 23 checks). All reports filed next to their drafts. Awaiting: scholar triage of objections → sign-off → token → DOI.
