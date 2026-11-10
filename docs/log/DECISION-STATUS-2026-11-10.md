# DECISION STATUS — owner/scholar asks, measured state 2026-11-10

Update to `DECISION-PACKET-2026-11-06.md` (which stays untouched). For each
ask: DONE, OPEN (exact next action), or BLOCKED. Evidence linked, not asserted.

Owner approved on 2026-11-10: Search Console submit, IndexNow, first inbound
link, cron, token rotation, disk reclaim, Zenodo token, dīkṣā calls, recipe
R1–R8 go-aheads, NGMPP path, "and anything else" (journey/ledger, audio,
outreach). This file records what the box executed vs what needs owner hands.

## DONE by the box (verify, don't trust)

| # | Ask (11-06) | State 11-10 | Evidence |
|---|---|---|---|
| A1 cron | DONE, better than asked | `crontab -l` shows one line `7 3 * * * ... nightly-verify.sh` with `OPENPATALA_DSN` set (DB step runs) + log to `docs/log/nightly-verify.log`; dry-run exit 0; removed a duplicate ownerless line | this repo `tools/nightly-verify.sh`, dry-run log `/tmp/nightly-verify-test.log` |
| Disk reclaim | DONE (partial) | 3.5G → 4.6G free (94%); removed only rebuildable caches (playwright 924M, uv 307M, pycache); `/tmp` live files untouched | `df -h /` |
| IndexNow | READY + 1 accepted | key file live on prod (`/<key>.txt` 200), `svread/tools/indexnow_ping.py` built; single-URL submit HTTP 202; 1916-URL bulk throttled with 403s — retry pending (command recorded below) | svread PR #12 branch |
| SEO build it gates | DONE, live | 909 claim pages, sitemap 1919, seo 10+gates GREEN, deployed + curl-verified | svread PR #12 |

## OPEN — owner hands required (exact actions)

1. **Search Console.** Site is ready (sitemap 1919 live, robots clean, pages served no-JS). Steps for owner: Search Console → Add property → **domain property** (covers all URLs) → verify via **DNS TXT** at registrar → submit `https://svread.pages.dev/sitemap.xml` → URL-inspect `/`, `/about/`, one `/claim/` page → Request indexing. Bing Webmaster: same + verify + submit sitemap (IndexNow key already live).
2. **Token rotation (mint — cannot be done from this box).** Audit 11-10 (names only, values never printed): `/root/.env` holds `OPENCODE_GO_API_KEY`, R2 patala set (`ACCOUNT_ID/API_TOKEN/ACCESS_KEY_ID/SECRET/ENDPOINT`), reader DSN; `/root/.r2-env` holds R2 set + `CF_API_TOKEN`; `/root/.cf-api-token` (53B). All 600 perms, no pasted secrets in svread code. Steps: Cloudflare dashboard → R2 → Manage API tokens → rotate both sets → replace values in place → `python3 svread/tools/emit_discovery.py --check` (no-op sanity) + one `wrangler pages deploy` dry check; opencode provider → rotate Go key → replace `OPENCODE_GO_API_KEY` → confirm with one cheap call. Then confirm here ("rotated") and this item closes.
3. **Zenodo token.** No script found in-repo (docs say dry-run ready — confirm exact command before running). Steps: zenodo.org → account → Applications → new token (deposit:write) → save to `/root/.zenodo-env` (600, never in repo) → dry-run first DOI (Variety-1 essay, only after DERIVED exemplar Q12 + human sign) → confirm DOI resolves.
4. **Outreach (first inbound link).** Nothing sent (needs your voice/relationships). Suggested targets: (a) Hareesh/tantrikstudies.org contact — ask for a resource-page link to one readable claim page; (b) Wikipedia external link on an Abhinavagupta/Tantraloka article — cite the trace URL, not the homepage; (c) an academic colleague working on Trika — request critique, not promotion (a critical link counts the same). Draft opener (adapt, don't blast):
   > "We publish checkable Trika translations — every claim carries source bytes, gate status and recomputable hashes (example: <claim URL>). If you spot an error, the page tells you exactly how to reproduce it. Worth a resource-page link, or corrections welcome either way."
5. **NGMPP witness path.** Candidates file ready (`formal-trika/bridge/witness-candidates.json` — pointers only, never pins; resolver hard-enforces UNPINNED). Steps: decide NGMPP/microfilm channel vs defer; first target should be Tantrasāra or Tantrāloka core (most-cited). Until then witnesses stay 0 and every page keeps saying so — that honesty is the current trust cue.
6. **dīkṣā policy (your call, draft to sign).** Practice compiler holds STUDY-only. Options — **A)** keep STUDY-only indefinitely (safest; no authorization implied); **B)** allow DOABLE units with logged human sign-off per unit; **C)** full practice authorization with eligibility checks (needs rater-2 + scholar concurrence first — not available today, so C is effectively "defer"). Sign one line (A/B/C-defer) and this closes.
7. **Still open from 11-06 (unchanged):** L4 first-verse voices (translation lane waits on 5 Tantrasara verdicts + prior golds); paramarthasara/sivastotravali schedule + diction register; **P-TK1** (scholar); **rater-2** (second human); **ti/ca** (scholar); **PR #9/#10** translation-lane merge calls; **journey go** (spec only — go/no); **audio-render go** (spec + plan ready — go/no).

## Recipes R1–R8: UNFROZEN 2026-11-10 (owner approval recorded)

Standing invariants unchanged (binding): diary is private — consent per use,
scoped, revocable; no auto-publish of personal material ever; sourced means
every claim resolves or it doesn't ship; machine proposes, human disposes.

| Recipe | Readiness | Next action (owner) |
|---|---|---|
| R1 diary → personal essay | READY to pilot: 9 diary entries exist (`nibbanahelp/entries/`), consent rule exists (diarist's call) | **Pick 1–3 entries + the use** (scoped consent for this run only); then compile → audit → PUSHBACK → sign |
| R2 essay → teaching audio | audio lanes exist (R2 svread-audio, aoc patterns — reuse) | pilot after first signed essay exists (none yet) |
| R3 essay → video | factory lanes exist; sealed-mp4 gates exist | pilot after first signed essay |
| R4 journey-linked publishing | journey go still owed (item above) | decide journey go first |
| R5 parables/C2 registers | C2 contract exists; voice direction is lane-owned | pick register + lane review |
| R6 kids books | highest bar (human reads every line aloud) | needs signed source claims first |
| R7 diary year-review book | TEXT-GATE per entry exists as rule | year boundary + scoped consent |
| R8 poem book | compiler law exists (verbatim only) | scoped consent + arrangement pass |
| R9 short movies | explicitly NOT YET | no build — models do not qualify; approval does not override the model-quality gate |

## Retries / repeats (commands, no owner needed)

- IndexNow bulk: `cd /root/svread && python3 tools/indexnow_ping.py --key 3d27af31a3616a8bfdcd8e7f60f19df4` (backs off + retries; rerun tomorrow — today throttled after 1×202).
- Nightly: first green log expected 2026-11-11 ~03:07 UTC at `docs/log/nightly-verify.log`.
- Freshness: `formal-trika/tools/freshness.py --check` must stay SHARP (regenerated 11-10 post-sitemap).

## Explicitly NOT done from the box (needs other hands)

Minting tokens, DNS edits, Google/Bing accounts, outreach relationships,
manuscript eyes, scholar rulings/signatures, lane merges, dīkṣā ruling,
journey/audio go — all named above with the exact next hand movement.
