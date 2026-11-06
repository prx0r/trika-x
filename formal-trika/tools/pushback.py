#!/usr/bin/env python3
"""pushback.py — D1: cross-model destroy pass over a draft (Variety 1 gate).

Protocol (PUSHBACK kit): each CITED claim becomes an objection; the model
hounds what the banked sources actually say; output = Resolution +
Honest remainder. External providers receive selected claim text. The caller
must opt in with --allow-external-text and shield private or verbatim spans;
a regex cannot guarantee complete redaction. The report never edits the draft.
Tiers ride every objection (T/R/E/C/H/X); R never promotes itself.

Usage:
  python3 formal-trika/tools/pushback.py --draft CRUX-DRAFT.md \
      --refs refs.json --model mock --out report.md
  python3 formal-trika/tools/pushback.py --draft CRUX-DRAFT.md \
      --refs refs.json --model go:beam-free --out report.md
  python3 formal-trika/tools/pushback.py --draft CRUX-DRAFT.md \
      --refs refs.json --model cf:@cf/mistralai/mistral-small-3.1-24b-instruct \
      --out report.md
refs.json: [{kind: chunk, work, target}] for claims.link (svread/mcp).
mock: deterministic templated objections (tests + offline).
go:<id>: OpenCode Go beam-free via /root/scripts/go_beam.py (default worker;
  key ONLY in /root/.env 0600, never in repos).
cf:<id>: Cloudflare Workers AI (token 0600 /root/.cf-api-token; neurons logged).
"""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent

CF_ACCOUNT = "954612afb5a97bb15dddcdc70176813d"
CF_TOKEN_FILE = Path("/root/.cf-api-token")


def draft_sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def mock_object(claim, markers):
    m = ", ".join(markers) if markers else "no markers"
    return (f"OBJECTION — is this what the banked sources say, or a gloss?\n"
            f"Claim: {claim[:220]}\nMarkers: {m}\n"
            f"Banked check (mock): UNVERIFIED — no live model ran.\n"
            f"Resolution: UNRESOLVED (mock).\n"
            f"Honest remainder: everything (mock never resolves).")


def cf_object(model, claim, markers, evidence):
    import urllib.request
    token = CF_TOKEN_FILE.read_text().strip()
    prompt = (
        "You are a hostile peer reviewer of Trika scholarship. Destroy-pass rules: "
        "every cited claim is suspect until the banked evidence below supports it; "
        "tiers matter (T=root text, R=reconstruction — R never promotes itself); "
        "statistics over tiny n are pilots, not findings; name the strongest "
        "counter-reading. Reply in exactly three sections: OBJECTION / "
        "What-banked-sources-say / Honest-remainder.\n\n"
        f"CLAIM UNDER TEST: {claim[:1500]}\nMARKERS: {markers}\n"
        f"BANKED EVIDENCE (only citable ground): {evidence[:2500]}")
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/{model}",
        data=json.dumps({"messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode())
    try:
        return d["result"]["response"]
    except (KeyError, TypeError):
        pass
    try:  # OpenAI-style chat completion shape (e.g. deepseek-v4.1-flash)
        return d["result"]["choices"][0]["message"]["content"]
    except (KeyError, TypeError, IndexError):
        return f"OBJECTION — model call malformed: {json.dumps(d)[:300]}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--draft", type=Path, required=True)
    ap.add_argument("--refs", type=Path, required=True)
    ap.add_argument("--model", default="mock")
    ap.add_argument("--verbatim", default="", help="regex shielding owner-verbatim spans")
    ap.add_argument("--allow-external-text", action="store_true",
                    help="allow selected draft text to be sent to the chosen external model")
    ap.add_argument("--svread", type=Path,
                    default=Path(os.environ.get('SVREAD_CHECKOUT', HERE.parent.parent / 'svread')))
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    if a.model != 'mock' and not a.allow_external_text:
        raise SystemExit('external model calls require --allow-external-text')
    mcp = a.svread / 'mcp'
    if not (mcp / 'claims.py').is_file():
        raise SystemExit('svread claims module unavailable; set --svread or SVREAD_CHECKOUT')
    sys.path.insert(0, str(mcp))
    import claims as claim_table
    text = a.draft.read_text(encoding="utf-8")
    refs = json.loads(a.refs.read_text(encoding="utf-8"))
    table = claim_table.link(text, refs=refs)
    verb = re.compile(a.verbatim) if a.verbatim else None
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    # locator -> formal entries (file :: theorem + kind + tier notes):
    # markers cite locators (work:target), entries are keyed file::theorem.
    loc_index = {}
    for key, e in ev.get("entries", {}).items():
        for c in e.get("chunks", []) or []:
            loc = c.get("locator")
            if not loc:
                continue
            loc_index.setdefault(loc, []).append(
                {"theorem": key, "kind": e.get("kind"),
                 "tier": c.get("tier"), "status": c.get("status"),
                 "note": c.get("note")})
    sections = [f"# PUSHBACK report (machine proposes, human disposes)",
                f"- draft: {a.draft.name} sha256:{draft_sha(text)[:16]}",
                f"- model: {a.model}", f"- claims: {len(table['claims'])}",
                "- This report NEVER edits the draft. Unresolved stays unresolved."]
    n_obj = 0
    for c in table["claims"]:
        if c["citation"] != "CITED":
            sections.append(f"\n## para {c['para']} — UNCITED (no objection; original argument)\n")
            continue
        markers = [lnk["marker"] for lnk in c["links"]]
        paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
        body = paras[c["para"]] if c["para"] < len(paras) else ""
        if verb and verb.search(body):
            sections.append(f"\n## para {c['para']} — VERBATIM-SHIELDED (owner words, not pushed)\n")
            continue
        evpin = {}
        for m in markers:
            loc = m.split(":")[-1]
            evpin[m] = loc_index.get(loc, "no formal entry for locator " + loc)
        if a.model == "mock":
            out = mock_object(body, markers)
        elif a.model.startswith("go:"):
            import os as _os
            _gb = _os.environ.get("GO_BEAM_PATH", "/root/scripts/go_beam.py")
            sys.path.insert(0, os.path.dirname(_gb))
            import go_beam
            out, _use = go_beam.chat(
                [{"role": "system", "content": (
                    "You are a hostile peer reviewer of Trika scholarship. Destroy-pass rules: "
                    "every cited claim is suspect until banked evidence supports it; "
                    "tiers matter (T=root text, R=reconstruction — R never promotes itself); "
                    "statistics over tiny n are pilots, not findings; name the strongest "
                    "counter-reading. Reply in exactly three sections: OBJECTION / "
                    "What-banked-sources-say / Honest-remainder.")},
                 {"role": "user", "content": (
                     f"CLAIM UNDER TEST: {body[:1500]}\nMARKERS: {markers}\n"
                     f"BANKED EVIDENCE (only citable ground): "
                     f"{json.dumps(evpin, ensure_ascii=False)[:2500]}")}],
                model=a.model[3:], session="pushback-formal-trika")
        elif a.model.startswith("cf:"):
            out = cf_object(a.model[3:], body, markers,
                            json.dumps(evpin, ensure_ascii=False))
        else:
            raise SystemExit(f"unknown model {a.model} (mock|go:<id>|cf:<id>)")
        n_obj += 1
        sections.append(f"\n## OBJECTION {n_obj} (para {c['para']}, markers {markers})\n\n{out}\n")
    sections.append(f"\n---\nobjected: {n_obj}; model: {a.model}; "
                    f"limitations: {table.get('limitations', [''])[0]}")
    a.out.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"claims: {len(table['claims'])}, objections: {n_obj}, model: {a.model} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
