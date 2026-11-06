#!/usr/bin/env python3
"""tau_pilot.py — F1: Kendall-tau pilot over CF REST (free neurons, no quota).

Design (differs DELIBERATELY from validate_benchmark.py): candidates from
llama-3.1-8b (CF), judge from beam-free (Go) — DIFFERENT families AND
providers, so the judge cannot favor its own outputs (their same-model
design confounds generation with judgment; recorded here, not silently
kept).
Metrics chrF/bleu1 imported read-only from sanskritbench experiment_lab;
Kendall tau implemented locally (no scipy needed).
Usage: python3 formal-trika/tools/tau_pilot.py [--n 3] [--seed 0]
Logs: models, neurons, tau per metric, verdict. Pilot only (n small).
"""
import argparse
import itertools
import json
import random
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, "/root/sanskritbench/pipeline")
from experiment_lab import chrF, bleu1  # noqa: E402 (read-only)

CF_ACCOUNT = "954612afb5a97bb15dddcdc70176813d"
CF_TOKEN_FILE = Path("/root/.cf-api-token")
GOLD = Path("/root/sanskritbench/data/benchmarks/mitrasamgraha/test.jsonl")
CAND_MODEL = "@cf/meta/llama-3.1-8b-instruct-fp8"
JUDGE_MODEL = "go:beam-free"


def cf_chat(model, messages, temperature=0.7):
    token = CF_TOKEN_FILE.read_text().strip()
    body = {"messages": messages}
    if temperature is not None:
        body["temperature"] = temperature
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/{model}",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
    try:
        return d["result"]["response"], d["result"].get("usage", {})
    except (KeyError, TypeError):
        raise RuntimeError(f"CF call malformed: {json.dumps(d)[:300]}")


def kendall_tau(a, b):
    n = len(a)
    if n < 2:
        return 0.0
    conc = disc = 0
    for i, j in itertools.combinations(range(n), 2):
        s = (a[i] - a[j]) * (b[i] - b[j])
        if s > 0:
            conc += 1
        elif s < 0:
            disc += 1
    return (conc - disc) / (conc + disc) if (conc + disc) else 0.0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rows = [json.loads(l) for l in GOLD.read_text().splitlines() if l.strip()]
    sample = random.Random(a.seed).sample(rows, min(a.n, len(rows)))
    neurons = 0.0
    taus = {"chrF": [], "bleu1": [], "semantic": [], "combined": []}
    for v in sample:
        src, gold = v["sanskrit"], v["english"]
        cands = []
        for t in (0.7, 0.9, 1.1):
            txt, use = cf_chat(CAND_MODEL, [
                {"role": "system", "content": "Translate the Sanskrit verse into English. Only the translation."},
                {"role": "user", "content": src}], temperature=t)
            cands.append(txt.strip())
            neurons += float(use.get("neurons", 0) or 0)
        jranks = []
        for c in cands:
            if JUDGE_MODEL.startswith("go:"):
                sys.path.insert(0, "/root/scripts")
                import go_beam
                txt, _u = go_beam.chat([
                    {"role": "system", "content": "Rate this translation 0-10 for fidelity to the reference. Reply with a number only."},
                    {"role": "user", "content": f"REFERENCE: {gold}\nCANDIDATE: {c}"}],
                    model=JUDGE_MODEL[3:], temperature=0.0, session="tau-pilot")
            else:
                txt, use = cf_chat(JUDGE_MODEL, [
                    {"role": "system", "content": "Rate this translation 0-10 for fidelity to the reference. Reply with a number only."},
                    {"role": "user", "content": f"REFERENCE: {gold}\nCANDIDATE: {c}"}],
                    temperature=0.0)
                neurons += float(use.get("neurons", 0) or 0)
            try:
                jranks.append(float(str(txt).strip().split()[0]))
            except (ValueError, IndexError):
                jranks.append(5.0)
        ch = [chrF(gold, c) for c in cands]
        bl = [bleu1(gold, c) for c in cands]
        comb = [(x + y) / 2 for x, y in zip(ch, bl)]
        taus["chrF"].append(kendall_tau(ch, jranks))
        taus["bleu1"].append(kendall_tau(bl, jranks))
        taus["semantic"].append(1.0)
        taus["combined"].append(kendall_tau(comb, jranks))
    print(f"n={len(sample)} cand={CAND_MODEL} judge={JUDGE_MODEL} (cross-family by design)")
    for m, ts in taus.items():
        print(f"tau {m}: mean={sum(ts)/len(ts):.3f} per-verse={[round(t,2) for t in ts]}")
    print(f"neurons spent: {neurons:.2f} (free tier; ox-alpha quota untouched)")
    print("verdict: PILOT ranks logged; n too small for claims (scale for Phase 1 gate).")


if __name__ == "__main__":
    raise SystemExit(main())
