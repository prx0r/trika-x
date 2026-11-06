#!/usr/bin/env python3
"""roboscholar.py — the roboscholar loop: model drafts, harness checks.

One command runs a machine-proposed essay draft through the full local
verification family and files the receipt. No backend, no signoff, no
publish — those stay human/account acts. Free-tier model only.

  python3 tools/roboscholar.py --model @cf/qwen/qwen3-30b-a3b-fp8 --work tantrasara-a08 --chunk tsa08-p04

Steps: (1) Qwen drafts from banked argmap premises (transmission packet:
what it is, moves, traps — never the conclusion); (2) claims.link builds
the claim table; (3) audit.audit checks quotes vs supplied sources;
(4) pushback.py mock files mechanical issues. Draft lands in
formal-trika/swarm/ labeled machine-proposed; receipt JSON beside it.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CF_ACCOUNT = "954612afb5a97bb15dddcdc70176813d"
CF_TOKEN_FILE = Path("/root/.cf-api-token")
SVREAD = Path(os.environ.get("SVREAD_CHECKOUT", HERE.parent.parent / "svread"))
sys.path.insert(0, str(SVREAD / "mcp"))
import audit as draft_audit
import claims as claim_table


def premises(workdir: str, verses: list) -> list:
    out = []
    for line in (HERE / "data" / "argmap-nodes.jsonl").open(encoding="utf-8"):
        d = json.loads(line)
        if d.get("source_file", "").startswith(workdir + "/") and d.get("verse_id") in verses:
            out.append(d)
    return out


def cf_chat(model: str, prompt: str) -> str:
    token = CF_TOKEN_FILE.read_text().strip()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/{model}",
        data=json.dumps({"messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read().decode())
    try:
        return d["result"]["response"]
    except (KeyError, TypeError):
        return d["result"]["choices"][0]["message"]["content"]


PROMPT_TMPL = """You draft one essay paragraph plus claim bullets from GIVEN premises only. Machine-proposed, never canonical.

Chunk: {chunk} (gold argmap, machine-proposed translation; edition CANDIDATE, witness UNKNOWN).
Banked premises (quote or paraphrase these, invent nothing):
{premises}

Rules: tier every claim R (reconstruction); cite [verse-id] bracket markers (e.g. [tsa-a08-v71]) after each claim; quote short EXACT fragments (copy verbatim, max 12 words) when quoting premises; state open questions; no doctrine beyond the premises; no T-tier; no witness claims; no verdict on the manas cut.
Traps: group membership is not begetting; counts are not causes; the verses list instruments, they do not narrate creation.
Reply: paragraph, then bullets of the form `- claim [marker] (tier)`."""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="@cf/qwen/qwen3-30b-a3b-fp8")
    ap.add_argument("--work", default="tantrasara-a08")
    ap.add_argument("--chunk", default="tsa08-p04")
    ap.add_argument("--verses", nargs="+",
                    default=["tsa-a08-v71", "tsa-a08-v73", "tsa-a08-v75", "tsa-a08-v79"])
    a = ap.parse_args()
    nodes = premises(a.work, a.verses)
    if not nodes:
        print("ERROR: no banked premises for verses", a.verses)
        return 1
    banked = "\n".join(f"- {n['verse_id']}: {'; '.join(n.get('premises', [])[:3])}" for n in nodes)
    prompt = PROMPT_TMPL.format(chunk=f"{a.work}:{a.chunk}", premises=banked)
    draft = cf_chat(a.model, prompt)
    if not draft or not draft.strip():
        print("ERROR: empty model reply (fail-closed, not data)")
        return 1
    day = datetime.date.today().isoformat()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%H%M%S")
    swarm = HERE / "swarm"
    swarm.mkdir(exist_ok=True)
    slug = f"robo-{a.chunk}-{day}-{stamp}"
    (swarm / f"{slug}.md").write_text(
        f"# ROBOSCHOLAR DRAFT (machine-proposed, never canonical)\n\n"
        f"- model: {a.model}\n- chunk: {a.work}:{a.chunk}\n"
        f"- prompt_sha256: {hashlib.sha256(prompt.encode()).hexdigest()}\n\n{draft}\n")
    refs = [{"kind": "chunk", "work": a.work, "target": a.chunk}]
    table = claim_table.link(draft, refs=refs)
    # Verse-level sources: the model cites verse ids, so each cited verse
    # gets its banked premises as its source (R-grounds, labeled as such).
    markers = {}
    for n in nodes:
        vid = n.get("verse_id", "")
        text = "; ".join(n.get("premises", [])[:3])
        markers[vid] = {"text": text}
        markers[f"{a.work}:{vid}"] = {"text": text}
    markers[f"{a.work}:{a.chunk}"] = {"text": banked}
    sources = {"markers": markers}
    receipt = draft_audit.audit(draft, refs=refs, sources=sources,
                                identity="roboscholar/loop", model=a.model)
    cited = sum(1 for c in table["claims"] if c["citation"] == "CITED")
    report = {"format": "roboscholar-receipt/1", "model": a.model, "date": day,
              "chunk": f"{a.work}:{a.chunk}",
              "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
              "claims": f"{cited}/{len(table['claims'])} CITED",
              "audit": receipt,
              "note": ("supplied sources are argmap excerpts (R-grounds), not "
                       "authenticated bundles; quotes bind prose to premises only")}
    (swarm / f"{slug}.receipt.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    print(f"draft+receipt -> swarm/{slug}.* | {cited}/{len(table['claims'])} CITED | "
          f"audit checks: {len(receipt.get('checks', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
