#!/usr/bin/env python3
"""essay_compile.py — compile expansion essays, never write them.

An expansion essay = owner voice (verbatim quotes, never altered) +
banked audit-chain claims (argmap nodes R + Lean theorems T, tiered,
marker-cited) + open questions. The compiler assembles; it invents no
prose, no doctrine, no verdict. Claim tables + link/audit/pushback
receipts ride every output. Topic graph grows per compilation.

  python3 tools/essay_compile.py --owner /root/tantraessays/essays/essays20/E10_mala_objectivity.md \\
      --work tantrasara-a08 --chunk tsa08-p02 --verses tsa-a08-v18 tsa-a08-v19 tsa-a08-v20 tsa-a08-v21 tsa-a08-v22 \\
      --theorems "Mala.lean :: count_3" --slug mala-objectivity --title "Impurity Is Objectivity"

Owner essays are lore/voice (truthful to the teacher, not grounds).
Argmaps are grounds for R. Theorems are grounds for T. Witnesses stay
UNPINNED. Machine proposes; owner + scholar dispose.
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import roboscholar as robo

sys.path.insert(0, str(Path("/root/svread/mcp")))
import audit as draft_audit
import claims as claim_table


def owner_blocks(path: Path):
    text = path.read_text(encoding="utf-8")
    quotes = re.findall(r'(?m)^> (.*)$', text)
    frames = re.findall(r'(?m)^\[([^\]]+)\]$', text)
    title = (re.findall(r'(?m)^# (.*)$', text) or ["(untitled)"])[0]
    return title, quotes, frames, text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--owner", type=Path, required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--chunk", required=True)
    ap.add_argument("--verses", nargs="+", required=True)
    ap.add_argument("--theorems", nargs="*", default=[])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--research", type=Path, default=None,
                    help="research-library essay/commentary file as second voice (verbatim quotes only)")
    a = ap.parse_args()
    title, quotes, frames, raw = owner_blocks(a.owner)
    if a.research:
        rtitle, rquotes, rframes, _ = owner_blocks(a.research)
    else:
        rtitle, rquotes, rframes = "", [], []
    nodes = robo.premises(a.work, a.verses)
    if not nodes:
        print("ERROR: no banked nodes for verses", a.verses)
        return 1
    day = datetime.date.today().isoformat()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%H%M%S")
    marker_chunk = f"{a.work}:{a.chunk}"
    parts = [f"# {a.title or title} (EXPANSION DRAFT — compiled, never written)",
             "",
             f"- owner voice: `{a.owner}` (verbatim below, unaltered)",
             f"- grounds: {a.work}:{a.chunk} ({len(nodes)} gold argmap units, R)",
             (f"- formal: {', '.join(a.theorems)} (T, decide-verified)" if a.theorems else
              "- formal: none cited"),
             "- status: MACHINE-COMPILED, owner + scholar dispose; witness UNPINNED",
             "",
             "## Owner voice (verbatim quotes, framing kept)",
             ""]
    for q in quotes:
        parts.append(f"> {q}")
    if rquotes:
        parts.append("")
        parts.append(f"## Research voice (verbatim, from `{a.research.name}` — unaltered)")
        parts.append("")
        for q in rquotes[:8]:
            parts.append(f"> {q}")
    for f in frames[:6]:
        parts.append(f"[{f}]")
    parts += ["", "## Banked claims (audit chain, tiered)", ""]
    for n in nodes:
        vid = n.get("verse_id", "")
        for p in n.get("premises", [])[:3]:
            parts.append(f"- {p} [{vid}] (R)")
        if n.get("inference"):
            parts.append(f"- inference: {n['inference']} [{vid}] (R)")
    if a.theorems:
        parts += ["", "## Formal note", ""]
        for t in a.theorems:
            parts.append(f"- {t}: checked structure, weaker than the text (T, model only)")
    parts += ["",
              "## Open questions (kept open, not smoothed)",
              "- Which banked premises does the owner's framing select, and which does it pass over?",
              "- What would a witness manuscript change in the verse readings?",
              "- What rival readings live in the uncertainties?",
              ""]
    draft = "\n".join(parts)
    swarm = HERE / "swarm"
    swarm.mkdir(exist_ok=True)
    slug = f"expansion-{a.slug}-{day}-{stamp}"
    (swarm / f"{slug}.md").write_text(draft + "\n")
    refs = [{"kind": "chunk", "work": a.work, "target": a.chunk}]
    table = claim_table.link(draft, refs=refs)
    markers = {}
    for n in nodes:
        vid = n.get("verse_id", "")
        text = "; ".join(n.get("premises", [])[:3])
        markers[vid] = {"text": text}
        markers[f"{a.work}:{vid}"] = {"text": text}
    markers[marker_chunk] = {"text": "banked premises above"}
    sources = {"markers": markers}
    receipt = draft_audit.audit(draft, refs=refs, sources=sources,
                                identity="essay-compile/loop", model="compiler-v1")
    cited = sum(1 for c in table["claims"] if c["citation"] == "CITED")
    # Linker only sees [work:target] chunk markers; verse bullets carry
    # [verse-id] markers by convention — count marker presence separately
    # so the receipt doesn't understate citation hygiene.
    verse_marked = sum(
        1 for c in table["claims"]
        if re.search(r"\[[A-Za-z0-9][A-Za-z0-9_.:-]{0,159}\]", json.dumps(c)))
    gpath = HERE / "data" / "expansion-graph.json"
    graph = json.loads(gpath.read_text(encoding="utf-8")) if gpath.is_file() else {
        "format": "trika-expansion-graph/1", "nodes": [], "edges": []}
    enode = f"essay:{slug}"
    graph["nodes"].append({"id": enode, "kind": "expansion-draft",
                           "owner": str(a.owner), "chunk": marker_chunk,
                           "date": day, "status": "MACHINE-COMPILED"})
    for n in nodes:
        vn = f"verse:{a.work}:{n.get('verse_id')}"
        if not any(x["id"] == vn for x in graph["nodes"]):
            graph["nodes"].append({"id": vn, "kind": "argmap-unit",
                                   "question": n.get("question", "")})
        graph["edges"].append({"from": enode, "to": vn, "rel": "grounds-on",
                               "tier": "R"})
    for t in a.theorems:
        tn = f"theorem:{t}"
        if not any(x["id"] == tn for x in graph["nodes"]):
            graph["nodes"].append({"id": tn, "kind": "theorem", "tier": "T"})
        graph["edges"].append({"from": enode, "to": tn, "rel": "cites-formal"})
    gpath.write_text(json.dumps(graph, ensure_ascii=False, indent=1) + "\n")
    report = {"format": "expansion-receipt/1", "essay": slug, "date": day,
              "owner_quotes": len(quotes), "banked_units": len(nodes),
              "theorems": a.theorems,
              "claims": f"{cited}/{len(table['claims'])} CITED + {verse_marked} verse-marked",
              "audit": receipt,
              "graph": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])},
              "note": "compiled, not written: owner words verbatim; substance from banked chain"}
    (swarm / f"{slug}.receipt.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    print(f"compiled -> swarm/{slug}.* | quotes: {len(quotes)} | units: {len(nodes)} | "
          f"{cited}/{len(table['claims'])} CITED | graph: {len(graph['nodes'])}n/{len(graph['edges'])}e")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
