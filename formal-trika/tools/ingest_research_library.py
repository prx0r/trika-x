#!/usr/bin/env python3
"""ingest_research_library.py — research essays + commentary into the topic graph.

Read-only over /root/projects/research-library (canonical; damn/ mirror
untouched). Ingests: essay collection A-H (tiers + thesis), commentary
nodes/NODEs/STAGEs (file nodes, grade R default), the 20-claim concordance
(claim nodes with [T]/[R]/[C] grades mapped to tiers), concept-deepdives
(topic nodes), claimants (external voices). Edges: feeds, grounds-on,
disputes (tensions), quotes.

Grades: [exact]/[T] -> T, [R] -> R, [C] -> C, mixed -> tier list.
Commentary analyses default R (never T — analyses aren't quotations).
Owner voice files stay verbatim-only inputs for essay_compile --research.

  python3 tools/ingest_research_library.py [--root PATH]
Appends to data/expansion-graph.json (dedupe by node id). Exit 0 + counts.
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
GRAPH = HERE / "data" / "expansion-graph.json"
GRADE = {"exact": "T", "T": "T", "R": "R", "C": "C"}


def parse_concordance(root: Path):
    text = (root / "CONCORDANCE-Ratie-IPK-Solms.md").read_text(encoding="utf-8")
    rows = []
    for line in text.splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|(.+)\|\s*$", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) < 7 or cells[0].startswith("Claim"):
            continue
        grades = sorted({GRADE[g] for g in re.findall(r"\[(exact|T|R|C)\]", cells[6]) if g in GRADE})
        rows.append({"n": m.group(1), "claim": cells[0], "ipk": cells[1],
                     "ratie": cells[2], "solms": cells[3], "ipvv": cells[4],
                     "xref": cells[5], "tiers": grades or ["R"]})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path("/root/projects/research-library"))
    a = ap.parse_args()
    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.is_file() else {
        "format": "trika-expansion-graph/1", "nodes": [], "edges": []}
    seen = {n["id"] for n in graph["nodes"]}
    nn = ne = 0

    def add_node(nid, kind, **kw):
        nonlocal nn
        if nid not in seen:
            graph["nodes"].append({"id": nid, "kind": kind, **kw})
            seen.add(nid)
            nn += 1

    def add_edge(frm, to, rel, **kw):
        nonlocal ne
        e = {"from": frm, "to": to, "rel": rel, **kw}
        if e not in graph["edges"]:
            graph["edges"].append(e)
            ne += 1

    essays = {
        "essay:A": ("The Greek Daimon Stream", "mythic/participatory", ["T"]),
        "essay:B": ("The Buddhist Stream", "structural/soteriological", ["T"]),
        "essay:C": ("The IPK-IPVV-Ratié Razor", "pure recognition", ["T"]),
        "essay:D": ("The Speculative Solms/Valence Thesis", "felt-is-primary", ["R", "C"]),
        "essay:E": ("Consciousness-Fundamental + Aperture + Frontier", "push", ["C"]),
        "essay:F": ("The Reflexion Debate", "formal dialectic", ["R"]),
        "essay:G": ("The IPVV Translation Work", "unique contribution", ["T"]),
        "essay:H": ("The Comparative Web", "parallels", ["C"]),
    }
    for eid, (title, reg, tiers) in essays.items():
        add_node(eid, "research-essay", title=title, register=reg, tiers=tiers,
                 status="ASSIGNED (THREE-ESSAYS/collection framing)")
        add_edge(eid, "thesis:recognition-felt", "argues", tiers=tiers)
    add_node("thesis:recognition-felt", "thesis",
             title="Recognition = the felt re-cognition of the self")
    for fp in sorted(a.root.glob("COMMENTARY-*.md")) + sorted(a.root.glob("ESSAY-*.md")):
        add_node(f"commentary:{fp.stem}", "commentary", file=str(fp), tiers=["R"])
        add_edge(f"commentary:{fp.stem}", "thesis:recognition-felt", "supports", tiers=["R"])
    for fp in sorted((a.root / "concept-deepdives").glob("*.md")):
        topic = fp.stem.replace("whattheheckis", "").replace("what-the-heck-is-", "").replace("-", " ")
        add_node(f"topic:{fp.stem}", "topic", title=topic, file=str(fp))
    for fp in sorted((a.root / "claimants").glob("*.md")):
        if fp.name == "claimants-catalog.md":
            continue
        add_node(f"voice:{fp.stem}", "external-voice", file=str(fp))
    for row in parse_concordance(a.root):
        cid = f"concordance:{row['n']}"
        add_node(cid, "concordance-claim", claim=row["claim"], ipk=row["ipk"],
                 ratie=row["ratie"], solms=row["solms"], ipvv=row["ipvv"],
                 xref=row["xref"], tiers=row["tiers"])
        add_edge(cid, "thesis:recognition-felt", "grounds", tiers=row["tiers"])
        add_edge("essay:C", cid, "cites")
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=1) + "\n")
    print(f"research-library ingested: +{nn} nodes, +{ne} edges "
          f"(total {len(graph['nodes'])}n/{len(graph['edges'])}e)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
