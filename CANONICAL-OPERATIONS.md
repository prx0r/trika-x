# CANONICAL OPERATIONS — how agents share this box without clobbering each other

*Status: canonical. Two agents are active in this repo as of 2026-11-14.
This file is the contract. When it conflicts with habit, this file wins.
Companion: `OPERATIONS.md` (how to run the machine) and `DOCS.md` (entry map).*

---

## 0. The rule of the box

**One concern per branch. Never touch a branch another agent owns. PR comments
are the coordination channel; dated `docs/log/` notes are the receipt.**
Everything below is procedure for that rule. It was written the day a
7322-file world-recompile landed in a shared working tree — the procedure
exists so that never ships.

## 1. Who owns what (2026-11-14, update on change)

| Branch / PR | Owner | Scope | State |
|---|---|---|---|
| `bridge/trace-refresh-2026-11-14` → PR #15 | swarm agent | trace refresh + re-key + extend (scoped burn refreshes) | OPEN, active (pushed 06:41) |
| `burn/muktabodha` (translation-work) | swarm agent | burn loop: T1–C1 layers for mukta works (ralph pass 227+) | OPEN, loop may still run |
| `pilot/dsp-a18-2026-11-14` → PR #19 | trika-x agent | D-DSP formal pilot + sketch gate | OPEN, awaiting assessor |
| `audit/*`, `ops/*`, `session-receipt-*`, `v1-tracker-*` | trika-x agent | receipts, audits, ops docs | merge when green |
| `main` | owner (merge only) | — | merge clean PRs, never commit direct |

If your name isn't on a row, read that branch, don't write it. Ask in its PR
comments before touching anything it owns.

## 2. The trace pipeline, canonically

Trace bundles are the most clobber-prone artifact in the estate: thousands of
files, two moving upstreams (translation-work layers, svread projections), and
a verifier that fails on any drift. The procedure:

```
1. SCOPE FIRST — name the works: trace_all.py --tw <TW> --works <w1,w2>
   NEVER run trace_all.py without --works on a shared branch. A world
   recompile touches ~8000 files and swamps every review. If you did it by
   accident: `git checkout -- formal-trika/data/traces/` + `git clean -fd
   formal-trika/data/traces/` (bundles are regenerable; the recipe is
   deterministic), then redo scoped.
2. VERIFY BEFORE REFRESH — for each bundle: trace_bundle.py --verify <file>
   --tw <right-checkout>. The right checkout matters: burn-sourced bundles
   verify ONLY against the burn worktree (main checkout lacks those ledgers;
   every bundle will read STALE and you will "fix" nothing).
   Worktree, don't switch: `git worktree add /tmp/tw-burn origin/burn/muktabodha`
   (remove it when done — 455 MB on a 98% disk).
3. REFRESH SCOPED — trace_all.py --tw <TW> --works <drifted-works-only>.
4. RE-VERIFY the refreshed set (expect OK; investigate any STALE individually —
   read the FIRST divergence line, it names the hop).
5. INDEX REBUILD LAST — trace_all.py --tw <TW> --index-only (fast; reads disk).
   NEVER commit bundles without the rebuilt index; NEVER commit the index
   rebuilt from a --works-filtered run (it drops every other work — this
   exact mistake happened: index went 2621 → 293).
6. COMMIT bundles + index together, one commit, message names the works.
7. PUSH to YOUR branch (never the other agent's), PR or PR-comment handoff.
```

**Verify-then-refresh, scoped, index-last, commit-together.** That sentence is
the whole pipeline.

## 3. No-clobber rules (binding)

1. **Check `git status` before any batch op.** A 4-digit changed-file count
   means STOP and re-scope — it never means push.
2. **Never push to a branch another agent owns.** Push to your own
   `trace-refresh-pickup-*`-style branch and PR into theirs, or hand off in
   their PR comments and let them push.
3. **Never force-push a shared branch.** Rebase only your own; if it diverged
   from someone else's work, talk first.
4. **Fetch before push, every time.** The box lags the remote; `git fetch
   origin` is cheaper than a conflicted push.
5. **No direct commits to `main`/`master`, ever** — not even docs, not even
   "trivial". Branch + PR, CI green, merge.
6. **No cross-lane writes.** Read translation-work/svread/ipvv; never write
   their files. Their lanes dispose; file CLAIMS notes, not edits.
7. **Moving upstreams get worktrees, not checkouts.** Never `git checkout`
   a lane repo to another branch mid-session — you will strand someone's
   working tree (including your own future self).
8. **Delete scratch worktrees when done** (`git worktree remove --force`;
   `git worktree prune`). Disk is 98%.

## 4. Handoff protocol (between agents)

When you finish a unit of work another agent consumes, leave a note with
exactly these fields — nothing more is needed, nothing less is enough:

```
BRANCH / PR:   <branch> (+ PR # if opened)
DID:           <commits pushed, one line each>
VERIFIED:      <gates run + results, with numbers>
BLOCKED ON:    <what stops the next step, with file:line or URL>
NEXT:          <the single smallest next action + who should do it>
```

The 2026-11-14 trace handoff ("+1644 bundles, 63 projection-sha refreshes, 2
mukta-m00125 drifted, needs one more refresh pass") is the format reference.
Handoffs go in the consuming PR's comments; receipts go in dated
`docs/log/` files.

## 5. Current shared state (2026-11-14 ~07:00 — re-verify, don't trust)

- PR #15 scope: 1644 burn bundles + 63 refreshed projections. Its index.json
  still reads 909 (pre-burn) — the rebuilder must regenerate it per §2.5.
- Burn loop (translation-work `burn/muktabodha`, ralph pass 227, last push
  06:43, no process running at 07:00): T1–C1 layers for mukta works incl.
  293-bundle m00125. **If the loop restarts, every bundle compiled against
  this state goes stale again** — check `git log origin/burn/muktabodha`
  before any refresh pass.
- m00125 bundles on PR #15 verify STALE against the burn worktree (layers
  moved under them — expected, honest). kularnavatantra likewise (83).
- svread publish gate (`emit_verify.py --check`): GREEN on main. The "blocked
  on 2 m00125" was against PR-#15-branch content, not main.
- `main` is at the audit merge (PR #17). Catalog SHARP 115, freshness SHARP,
  suite 107 OK (see `FINAL-GREEN-RECEIPT-2026-11-14.md`).

## 6. What I deliberately did NOT do (2026-11-14 session)

- Did **not** push the world-recompile (7322 files) anywhere — reset, documented
  here instead. The scoped refresh prescription (§2) is recorded for whoever
  runs it next.
- Did **not** touch PR #15's branch, the burn branch, or any lane repo.
- Did **not** merge anything owned by another agent or under active review.

*Machine proposes, human disposes. The box is shared; act like it.*
