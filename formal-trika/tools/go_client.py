#!/usr/bin/env python3
"""go_client.py — the OpenCode Go writer client (muse-spark-1.3 only, one fallback).

Primary:   muse-spark-1.3-contributor   POST {base}/responses        (Responses API)
Fallback:  mimo-v2.6-flash             POST {base}/chat/completions (OpenAI-compatible)

No other models. No llama. Credentials come from the environment or
/root/.opencode-go-env (never committed). Requests carry an
x-opencode-session header and a curl User-Agent — both required by the
gateway (missing session → 400; bot-shaped UA → Cloudflare 1010).

  from go_client import complete
  r = complete("Write one paragraph.", max_tokens=800)
  print(r["text"], r["model"], r["fallback"])

Standard library only. Fail-closed: if both models fail, raise GoError.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ENV_FILE = Path(os.environ.get("OPENCODE_GO_ENV", "/root/.opencode-go-env"))
CACHE = Path(__file__).resolve().parent / ".go-cache"
BASE_DEFAULT = "https://opencode.ai/zen/go/v1"
UA = "curl/8.5.0"

PRIMARY = "muse-spark-1.3-contributor"
FALLBACK = "mimo-v2.6-flash"
ALLOWED = (PRIMARY, FALLBACK)


class GoError(RuntimeError):
    pass


def _load_env() -> None:
    # The 600 vault file is authoritative: a stale OPENCODE_GO_API_KEY in the
    # parent environment must not shadow a rotated key.
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip().startswith("OPENCODE_GO_"):
                os.environ[k.strip()] = v.strip()


def _post(url: str, body: dict, session: str) -> tuple[int, str]:
    key = os.environ.get("OPENCODE_GO_API_KEY")
    if not key:
        raise GoError("OPENCODE_GO_API_KEY missing (env or %s)" % ENV_FILE)
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json",
                 "x-opencode-session": session,
                 "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except urllib.error.URLError as e:
        return 0, f"network: {e}"


def _text_from_responses(d: dict) -> str:
    out = []
    for item in d.get("output", []):
        if item.get("type") != "message":
            continue
        for c in item.get("content", []):
            if c.get("type") in ("output_text", "text"):
                out.append(c.get("text", ""))
    return "\n".join(out).strip()


def _call_responses(model: str, prompt: str, system: str, max_tokens: int,
                    temperature: float, session: str) -> tuple[str, dict]:
    body = {
        "model": model,
        "input": [{"role": "user",
                   "content": [{"type": "input_text", "text": prompt}]}],
        "max_output_tokens": max_tokens,
        "temperature": temperature,
    }
    if system:
        body["instructions"] = system
    st, raw = _post(base() + "/responses", body, session)
    if st != 200:
        raise GoError(f"{model}: HTTP {st}: {raw[:300]}")
    d = json.loads(raw)
    text = _text_from_responses(d)
    if not text:
        raise GoError(f"{model}: empty response (status={d.get('status')})")
    return text, {"usage": d.get("usage", {}), "id": d.get("id"),
                  "status": d.get("status")}


def _call_chat(model: str, prompt: str, system: str, max_tokens: int,
               temperature: float, session: str) -> tuple[str, dict]:
    msgs = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": prompt}]
    body = {"model": model, "messages": msgs,
            "max_tokens": max_tokens, "temperature": temperature}
    st, raw = _post(base() + "/chat/completions", body, session)
    if st != 200:
        raise GoError(f"{model}: HTTP {st}: {raw[:300]}")
    d = json.loads(raw)
    text = (d.get("choices", [{}])[0].get("message", {}) or {}).get("content", "")
    if not text or not text.strip():
        raise GoError(f"{model}: empty response")
    return text.strip(), {"usage": d.get("usage", {}), "id": d.get("id")}


def base() -> str:
    _load_env()
    return (os.environ.get("OPENCODE_GO_BASE_URL") or BASE_DEFAULT).rstrip("/")


def _cache_key(prompt: str, system: str, max_tokens: int, temperature: float) -> str:
    blob = json.dumps([PRIMARY, prompt, system, max_tokens, temperature], ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def complete(prompt: str, *, system: str = "", max_tokens: int = 6000,
             temperature: float = 0.7, cache: bool = True) -> dict:
    """Run one completion. Primary muse-spark-1.3-contributor, fallback mimo-v2.6-flash."""
    _load_env()
    key = _cache_key(prompt, system, max_tokens, temperature)
    cpath = CACHE / (key + ".json")
    if cache and cpath.is_file():
        try:
            d = json.loads(cpath.read_text(encoding="utf-8"))
            d["cached"] = True
            return d
        except ValueError:
            pass
    session = "essaygen-" + uuid.uuid4().hex
    errors = []
    for model, caller, fallback in ((PRIMARY, _call_responses, False),
                                    (FALLBACK, _call_chat, True)):
        try:
            text, meta = caller(model, prompt, system, max_tokens, temperature, session)
            out = {"text": text, "model": model, "fallback": fallback, **meta}
            if cache:
                try:
                    CACHE.mkdir(exist_ok=True)
                    cpath.write_text(json.dumps(out, ensure_ascii=False) + "\n", encoding="utf-8")
                except OSError:
                    pass
            return out
        except (GoError, json.JSONDecodeError, KeyError, TypeError) as e:
            errors.append(str(e))
            time.sleep(1)
    raise GoError("all models failed: " + " | ".join(errors))


if __name__ == "__main__":
    import sys
    r = complete("Reply with exactly: ENGINE OK", max_tokens=32, temperature=0)
    print(r["text"], "| model:", r["model"], "| fallback:", r["fallback"])
