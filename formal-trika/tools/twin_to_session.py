#!/usr/bin/env python3
"""twin_to_session.py — formal twins generate pushing sessions.

Every refusing twin is a precise "what if" the text denies. This tool
renders a pushing-session SKELETON from a twin file: ROUND 0 (the checked
theorem + its chunk grounds), ROUND 1 (the twin's denied claim as the
objection), honest-limit boilerplate. The assessor fleshes it with real
derivations (never generated) — skeleton only, like largetext scaffolds.

  python3 tools/twin_to_session.py --twin BrokenGenPerm --out swarm/
Skeleton format mirrors ipvv LOGICVID sessions (ROUND 0/1/2 + penetrations
left EMPTY for the assessor + honest limit). Exit 0.
"""
import argparse
import datetime
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def parse_twin(path: Path):
    text = path.read_text(encoding="utf-8")
    doc = (re.search(r"/\-(.*?)\-/", text, re.S).group(1).strip()
           if re.search(r"/\-(.*?)\-/", text, re.S) else "")
    theorems = re.findall(r"(?m)^theorem\s+([A-Za-z0-9_]+)\s*:\s*(.*?)\s*:=\s*by\s+decide", text, re.S)
    return doc, [(n, re.sub(r"\s+", " ", s)) for n, s in theorems]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--twin", required=True)
    ap.add_argument("--positive", default="")
    ap.add_argument("--out", type=Path, default=HERE / "swarm")
    a = ap.parse_args()
    twinname = a.twin if a.twin.endswith(".lean") else a.twin + ".lean"
    twin = None
    for _d in ("control", "buddhist", "frontier", "recognition"):
        _c = HERE / _d / twinname
        if _c.is_file():
            twin = _c
            break
    if twin is None:
        print(f"ERROR: no twin {twinname} in control/buddhist/frontier/recognition")
        return 1
    doc, theorems = parse_twin(twin)
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    day = datetime.date.today().isoformat()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%H%M%S")
    positive = a.positive or a.twin.replace("Broken", "")
    body = [f"# PUSHING SESSION SKELETON — {a.twin} (machine-rendered, assessor fleshes)",
            "",
            f"- date: {day} | positive: `{positive}` | status: SKELETON (no derivations; assessor writes ROUNDs)",
            f"- twin says: {(doc.splitlines() or [''])[:3]}",
            "",
            "## ROUND 0 — the checked claim (assessor: root quotes here)",
            ""]
    for name, stmt in theorems:
        body.append(f"- `{name}`: `{stmt[:160]}`")
        for key, e in ev.get("entries", {}).items():
            if key.split(" :: ")[-1] == name:
                for c in e.get("chunks", []) or []:
                    body.append(f"  - ground: {c.get('locator')} [{c.get('tier')}] — {c.get('note','')[:140]}")
                break
    body += ["",
             "## ROUND 1 — the twin's denied claim as objection (assessor: derivation here)",
             "",
             "> The twin denies exactly this. If the text cannot answer why not, that is the finding.",
             "",
             "## ROUND 2 — deeper (assessor only)",
             "",
             "## Honest limit (assessor: what the text refuses)",
             "",
             "_Skeleton rendered by twin_to_session.py. No derivation generated. "
             "Assessor fleshes or deletes._",
             ""]
    a.out.mkdir(exist_ok=True)
    out = a.out / f"session-skel-{a.twin.lower()}-{day}-{stamp}.md"
    out.write_text("\n".join(str(l) for l in body) + "\n")
    print(f"skeleton -> {out.name} ({len(theorems)} theorems)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
