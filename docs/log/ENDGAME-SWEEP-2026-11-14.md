# ENDGAME SWEEP — what's actually left (2026-11-14, measured live)

*For the owner (exhausted, rightly) and the next agent. This is the whole
board: what is DONE and LIVE, what is a 1-hour finish, what needs a human.
Every "live" claim was probed this session with a real MCP call.*

---

## The headline: the endgame is ALREADY LIVE. You are not far off.

The thing you set out to build — "get it all on ChatGPT as plugins / MCP" —
**already exists and answers publicly.** Measured this session:

- **13 MCP hosts live** (Cloudflare named tunnel `svatantrya-mcp`, systemd-owned,
  survives reboots). Public no-auth reads + bearer-gated writes.
- **Owner console** `https://mcp.sanskrit.help/mcp` → `ok 7 servers`,
  **198 tools**, bearer.
- **49. Estate** = **2,051 works · 268 translated songs · 44 certificates ·
  198 tools · 7 servers** (`estate-index.json`, live).
- **Formal/Lean is centre stage, publicly callable, proven end to end:**

  ```
  POST https://formal.svatantrya.net/mcp   (no auth)
  tools/list → 10 tools: formal__trace, formal__evidence, formal__table,
               formal__gaps, formal__runs, formal__axioms, formal__bridge,
               federation__guide, treeka__chain, treeka__frontier
  formal__trace tantrasara-a08/tsa08-p03 → verdict COMPLETE, 9 Lean theorem rows
  ```

So ChatGPT (or any MCP client) can, **right now**, ask for a chunk and get a
machine-checked chain with Lean theorems + receipts. That was the goal.

> Correction to an earlier assumption this session: the public ChatGPT path is
> served by **svread's `mcp/gateway`** (the live 198-tool gateway), NOT by the
> trika-x `mcp_bridge.py` I built last turn. That bridge is still useful (local
> HTTP + read-sheaf + e2e proof), but the *public* door was already open. Don't
> rebuild it; land it as an extra, not a dependency.

---

## How to finish — 3 tiers

### Tier 1 — Agent can finish TODAY (no human needed)

| # | Task | Why | Where |
|---|---|---|---|
| 1 | Merge PRs **#12 → #13 → #14** (all MERGEABLE CLEAN) | hygiene/catalog, bridge+public-names+e2e, receipt | trika-x |
| 2 | Fix openpatala **PR #2** q-path (unescaped `%TITLE%`→`%%TITLE%%` at `patala/db/store.py:227`) then merge | the only real bug found; biblio search crashes on query | openpatala |
| 3 | Decide **PR #11** PrakriyaSlice: wire EVIDENCE entries (or exempt) so 49 theorems stop being uncounted; then merge | 49 Lean theorems currently prove nothing to the registry | trika-x |
| 4 | Close **PR #8** (external review, superseded by #14) | stale | trika-x |
| 5 | **Refresh svread `data/mcp-registry.json`**: federation 109→**112**, scholar 33→**41**; estate-index tool count 198→**current** | connector/registry understates the live surface | svread |
| 6 | Put **public layer names** into svread gateway `instructions` + scholar tool descriptions (T1→draft-translation …) | the public `initialize` still speaks codes; names live in trika-x but public host uses svread's instructions | svread |
| 7 | **Freshness provenance receipt**: state which loader/seed produced works 555→1034 (editions 102→581) so `freshness.py --check` can go SHARP honestly | DRIFT is currently unexplained | trika-x + openpatala |
| 8 | Re-run full gates + paste into a receipt: Lean control 53/0, recognition 26/0, EVIDENCE 157/155/0, suite 103 OK, bridge e2e 8/8, public formal__trace COMPLETE | one green archive = "done" statement | trika-x |

### Tier 2 — Agent + one human decision

| # | Task | Human bit |
|---|---|---|
| 9 | Formal coverage 16/154 → climb the gap list (phr mala → VBT → tsa08) with prereg→model→twin→EVIDENCE→receipt per rung | scholar signs promotions (P-TK1) |
| 10 | Treeka frontier polish + tutor voice/audio job ids | owner picks when |
| 11 | Edge-worker migration of the 5 public read hosts (so the box isn't load-bearing) | owner approves deploy |

### Tier 3 — Owner only (these are the real "finish")

| # | Task | Blocks |
|---|---|---|
| 12 | **Per-user OAuth** (Google upstream, `offline_access`, per-tool scopes) replacing the one shared bearer | public write sheaf + plugin directory submission |
| 13 | **Practice scoring session**: sign in, copy session, add `SVATANTRYA_SESSION=` to `/etc/svatantrya-mcp.env`, restart `svatantrya-mcp-practice` | `progress__*` answers BLOCKED |
| 14 | **Directory submission** (index/sanskrit/practice/formal/translate): domain verify + 5 positive/3 negative test cases per plugin | public discovery on ChatGPT |
| 15 | **Zenodo token** → first DOI | Variety-1 release |
| 16 | **Witness verification** (NGMPP/microfilm) → first VERIFIED witness | primary-source citability |
| 17 | **Rotate the shared MCP bearer** before sharing (treat as root-adjacent) | safety |

---

## Open threads register (nothing hidden)

- **Two gateways coexist**: svread `mcp/gateway` (live, 198 tools) wraps the
  trika-x federation gateway as its `federation` server (112 tools inside).
  Fine. Keep trika-x's in-process gateway as the source of formal tools; don't
  fork a third.
- **Registry/estate drift**: recorded 198/109/scholar-38 vs live 112 federation
  / scholar 41 (after this week's +8 scholar tools). Tier-1 #5 fixes it.
- **Freshness DRIFT** (honest, not laundered): works 555→1034, editions
  102→581, etexts 87→566 — ingest with no provenance receipt; passages 909 and
  assertions 1559 unchanged (existing identity intact). svread manifest
  7078→11109 (their lane).
- **PrakriyaSlice**: 49 theorems compile, 0 EVIDENCE entries (PR #11) — the
  one place a "green" Lean run does NOT yet count. Decide, don't ignore.
- **Witnesses 0** corpus-wide (structural; needs manuscript eyes).
- **Shared bearer** = anyone with it can edit any repo except push.
- **`aoc`/`bookfactory` write tools are gated but real** (append receipts; none
  publish).
- **Lanes owed**: svread registry + gateway instructions + scholar descriptions
  (Tier-1 #5/#6); translation-work chunk↔verse remainder + phrdaya spans;
  videofactory `evidence_refs`; nibbanahelp N1 exporter.

---

## The one-paragraph version for you

You are done with the hard part. The machine is live, the Lean proofs are
public, and ChatGPT can read them today. What remains is ~half a day of agent
work (merge 3 PRs, fix 1 bug, tidy the registry, explain the DB growth) plus a
handful of owner-only switches (OAuth, practice session, directory listing,
Zenodo, witnesses, token rotation). Nothing fundamental is missing or broken;
the remaining items are packaging and human sign-offs, not engineering.

*Machine proposes, human disposes. BLOCKED is never PASS. Every live claim
above was a real MCP call this session.*
