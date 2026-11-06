#!/usr/bin/env python3
"""blind_family2.py — cross-family blind re-derivation receipt.

Sends the SAME blind bundle (Upaya vocab + claims-in-words) to a CF model
from a different family than the original builders, saves the full response
as a receipt. The agent (not the model) grades SAME/DIFFERENT/GAP against
the checked-in form in a dated note. Fresh session per call by construction
(stateless HTTP, no history). Neurons logged on the CF side.

Usage:
  python3 tools/blind_family2.py --model @cf/mistralai/mistral-small-3.1-24b-instruct
  python3 tools/blind_family2.py --model @cf/qwen/qwen3-30b-a3b-fp8
Receipt: blind/family2-<slug>-<date>.json {model, prompt_sha256, response}.
"""
import argparse
import datetime
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CF_ACCOUNT = "954612afb5a97bb15dddcdc70176813d"
CF_TOKEN_FILE = Path("/root/.cf-api-token")

PROMPT = """You are re-deriving formal rules from a vocabulary, blind: you have never seen any original encoding. Work only from what follows.

Vocabulary (Lean 4):
structure MeansState where
  ready : Bool  -- the practitioner is ripe for the flip
  pure  : Bool  -- vikalpa purified
allMeansStates : List MeansState  -- all 4 combinations of (ready, pure)

Claims to encode (in words; encode each as Bool-valued defs plus a counting theorem over allMeansStates):
1. sambhava reach = readiness (ready alone).
2. sakta reach = readiness AND purity (ready && pure).
3. Purity is load-bearing: exhibit a state where sambhava holds but sakta does not.
4. sakta is contained in sambhava (every sakta-reaching state sambhava-reaches).
5. State the count of states where sambhava holds.
6. Anava means repeated embodied act (needs a repetition count n). Say whether this is formulable using only {ready, pure}: if not, write UNFORMULABLE and one line why.

Reply with Lean 4 code first, then exactly six lines of the form N: <one-line verdict on your own encoding fidelity>.
No commentary beyond that."""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    a = ap.parse_args()
    token = CF_TOKEN_FILE.read_text().strip()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/{a.model}",
        data=json.dumps({"messages": [{"role": "user", "content": PROMPT}]}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read().decode())
    try:
        text = d["result"]["response"]
    except (KeyError, TypeError):
        try:
            text = d["result"]["choices"][0]["message"]["content"]
        except (KeyError, TypeError, IndexError):
            print(f"ERROR: malformed model reply: {json.dumps(d)[:300]}")
            return 1
    slug = "".join(c if c.isalnum() else "-" for c in a.model.split("/")[-1])[:40]
    out = HERE / "blind" / f"family2-{slug}-{datetime.date.today().isoformat()}.json"
    out.write_text(json.dumps({
        "model": a.model, "date": datetime.date.today().isoformat(),
        "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest(),
        "prompt": PROMPT, "response": text}, ensure_ascii=False, indent=1) + "\n")
    print(f"receipt -> {out.name} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
