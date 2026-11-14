#!/usr/bin/env python3
"""chatgpt_acceptance_run.py — execute the ChatGPT-side acceptance suite.

Runs formal-trika/tests/chatgpt_acceptance.json against the LIVE public
surface with zero box access: the same HTTPS calls a ChatGPT connector makes.
Each step reports PASS/FAIL with the observed value. Exit 0 iff all pass.

  python3 formal-trika/tools/chatgpt_acceptance_run.py [--suite PATH] [--only T5]
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SUITE = HERE.parent / "tests" / "chatgpt_acceptance.json"
MCP_HEADERS = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream",
               "MCP-Protocol-Version": "2025-06-18",
               "User-Agent": "svatantrya-acceptance/1 (+https://svatantrya.net)"}
HTTP_HEADERS = {"User-Agent": "svatantrya-acceptance/1 (+https://svatantrya.net)"}


def http_post(url, payload, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers=dict(MCP_HEADERS), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode()
            body = None
            for line in raw.splitlines():
                line = line.strip()
                if line.startswith("data:"):
                    try:
                        body = json.loads(line[5:])
                    except ValueError:
                        pass
            return r.status, body or {"_raw": raw[:200]}
    except urllib.error.HTTPError as e:
        return e.code, {"_http_error": e.code}


def http_get(url, timeout=60):
    req = urllib.request.Request(url, headers=dict(HTTP_HEADERS))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def tool_call(url, name, args, timeout=120):
    code, body = http_post(url, {"jsonrpc": "2.0", "id": 7,
                                 "method": "tools/call",
                                 "params": {"name": name, "arguments": args}},
                           timeout=timeout)
    call, is_err = None, False
    if isinstance(body, dict):
        if "result" in body:
            res = body["result"]
            for c in res.get("content", []) if isinstance(res, dict) else []:
                try:
                    call = json.loads(c.get("text", ""))
                    break
                except (ValueError, AttributeError):
                    call = {"_text": (c.get("text", "") or "")[:200]}
            is_err = bool(res.get("isError", False)) if isinstance(res, dict) else False
        elif "error" in body:
            call, is_err = {"_error": body["error"]}, True
    return {"transport": {"http_status": code},
            "call": call, "isError": is_err}


def resolve(path, ctx):
    """Tiny path language: a.b.c, [n] indexes, '| length' and '| names' suffixes."""
    m = re.match(r"^(.*?)\s*\|\s*(length|names)$", path)
    suffix = None
    if m:
        path, suffix = m.group(1), m.group(2)
    cur = ctx
    for part in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if part.startswith("["):
            cur = cur[int(part[1:-1])] if isinstance(cur, list) else None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
        if cur is None:
            break
    if suffix == "length" and hasattr(cur, "__len__"):
        return len(cur)
    if suffix == "names" and isinstance(cur, list):
        return [t.get("name", t.get("theorem")) for t in cur
                if isinstance(t, dict)]
    return cur


def check_assert(a, ctx):
    op, actual_path = a["op"], a["actual"]
    actual = resolve(actual_path, ctx)
    if op == "exists":
        ok = a.get("expect_exists", True) == (actual is not None)
        return ok, f"{actual_path}={'present' if actual is not None else 'MISSING'}"
    expected = a.get("expect")
    if op == "equals":
        return actual == expected, f"{actual_path}={actual!r} (want {expected!r})"
    if op == "gte":
        return (actual is not None and actual >= expected), f"{actual_path}={actual} (want >= {expected})"
    if op == "regex":
        return (isinstance(actual, str) and re.search(expected, actual) is not None), f"{actual_path} matches /{expected}/"
    if op == "contains":
        ok = (expected in actual) if isinstance(actual, (str, list)) else False
        return ok, f"{actual_path} contains {expected!r}"
    if op == "contains-all":
        missing = [e for e in expected if e not in (actual or [])]
        return not missing, f"missing={missing}" if missing else f"all {len(expected)} present"
    return False, f"unknown op {op}"


def run_step(step):
    req, ctx = step["request"], {}
    if "body" in req:  # MCP JSON-RPC endpoint
        code, body = http_post(req["url"], dict(req["body"], jsonrpc="2.0"), timeout=180)
        ctx = {"transport": {"http_status": code}, "body": body}
    elif "call" in req:
        c = req["call"]
        ctx = tool_call(req["url"], c["name"], c.get("arguments", {}))
    elif "http" in req:
        code, text = http_get(req["http"]["url"])
        body_json = None
        try:
            body_json = json.loads(text)
        except ValueError:
            pass
        ctx = {"http": {"status": code, "body_contains": text, "body_json": body_json}}
    else:
        return False, ["unknown request kind"]
    fails = []
    for a in step.get("assert", []):
        ok, detail = check_assert(a, ctx)
        if not ok:
            fails.append(f"{a['id'] if 'id' in a else a.get('actual')}: {detail}")
    return (not fails), fails


def main():
    ap = sys.argv[1:]
    suite = Path(ap[ap.index("--suite") + 1] if "--suite" in ap else DEFAULT_SUITE)
    only = ap[ap.index("--only") + 1] if "--only" in ap else None
    spec = json.loads(suite.read_text(encoding="utf-8"))
    steps = [s for s in spec["steps"] if only is None or s["id"] == only]
    passed, failed, skipped = [], [], []
    for s in steps:
        if s.get("box_runnable") is False:
            skipped.append(s["id"])
            print("SKIP " + s["id"] + "  " + s["name"]
                  + "  :: requires connected-tool environment (ChatGPT side): "
                  + str(s.get("skip_reason", "no box equivalent")))
            continue
        try:
            ok, detail = run_step(s)
        except Exception as e:  # noqa: BLE001 — a crash is a failed step, never a pass
            ok, detail = False, [f"EXCEPTION {type(e).__name__}: {str(e)[:160]}"]
        (passed if ok else failed).append(s["id"])
        print(("PASS " if ok else "FAIL ") + s["id"] + "  " + s["name"]
              + ("" if ok else "  :: " + " | ".join(detail)))
    total = len(passed) + len(failed) + len(skipped)
    print(f"\n{len(passed)}/{total} passed, {len(skipped)} skipped, {len(failed)} failed")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
