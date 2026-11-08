# TOKEN ROTATION CHECKLIST (2026-11-08 — needs owner, ~15 min)

Keys known-pasted in chat on 2026-11-06 (treat as exposed until rotated):

| # | Secret | Where it lives on box | Rotate at | After rotating |
|---|---|---|---|---|
| 1 | R2 (S3-compatible) token | `/root/.r2-env`, `/root/.env` (?) — grep before editing | Cloudflare dashboard → R2 → API tokens | update `/root/.r2-env`, re-run `python3 formal-trika/tools/openpatala_ingest.py --dry-run`-style R2 check; revoke old token |
| 2 | OpenCode Go API key (`opencode_go_api_key`, `sk-fv9GA...uQfTuW`) | vault + `/root/.env` + `/tmp/opencode/hermes-api-key.txt` | OpenCode Go dashboard | update all three locations; `rm` scratch copies in `/tmp/opencode/`; verify one `hermes -z` call |
| 3 | Cloudflare Workers AI token | `/root/.cf-api-token` (0600, 53 bytes) | Cloudflare dashboard → API tokens | replace file, keep 0600; verify `roboscholar` dry path (no model call needed — just auth check) |
| 4 | DashScope key (`SCHOLAR_DASHSCOPE_API_KEY`, if set) | env only | Alibaba Bailian console | update env; verify scholar text path |

Rules: one key at a time (never rotate all at once); verify each consumer
before moving on; `grep -rn <old-prefix> /root --include="*.env" --include="*.txt"`
afterwards to catch scratch copies; revoke — don't just abandon — old tokens.
