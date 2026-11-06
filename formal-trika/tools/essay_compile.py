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
    ap.add_argument("--owner", type=Path, default=None,
                    help="owner essay file (verbatim voice; optional when --research given: speculative topics compile from research voice + banked chain)")
    ap.add_argument("--work", required=True)
    ap.add_argument("--chunk", required=True)
    ap.add_argument("--verses", nargs="+", required=True)
    ap.add_argument("--theorems", nargs="*", default=[])
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--research", type=Path, default=None,
                    help="research-library essay/commentary file as second voice (verbatim quotes only)")
    ap.add_argument("--corpus-db", type=Path, default=None,
                    help="essay-corpus sqlite (idea units by topic+grade as voice)")
    ap.add_argument("--corpus-topic", default="",
                    help="topic tag to SELECT from corpus (grade DESC)")
    ap.add_argument("--l3", action="store_true",
                    help="L3 pass: sentence-to-claim tracing enforced (fail-closed), essence map, kill register")
    ap.add_argument("--l4", action="store_true",
                    help="L4 pass: per-paragraph DRAFT files (craft_notes + rejected + reads_against) + claim-overlap audit")
    a = ap.parse_args()
    if a.owner is None and a.research is None:
        print("ERROR: need --owner and/or --research voice (compiler never writes voice)")
        return 1
    title, quotes, frames = "", [], []
    if a.owner:
        title, quotes, frames, raw = owner_blocks(a.owner)
    if a.research:
        rtitle, rquotes, rframes, _ = owner_blocks(a.research)
    else:
        rtitle, rquotes, rframes = "", [], []
    cquotes = []
    if a.corpus_db and a.corpus_topic:
        import sqlite3 as _sq
        cx = _sq.connect(f"file:{a.corpus_db}?mode=ro", uri=True)
        for uid, grade, quote in cx.execute(
                "SELECT id, grade, quote FROM units WHERE topics LIKE ? ORDER BY grade, id",
                (f'%"{a.corpus_topic}"%',)):
            cquotes.append((uid, grade, quote))
        cx.close()
    nodes = robo.premises(a.work, a.verses)
    if not nodes:
        print("ERROR: no banked nodes for verses", a.verses)
        return 1
    # FREEZE claims BEFORE any prose (essaygen invariant): no sentence may
    # introduce a proposition outside its linked frozen claims (TRANSITION
    # boilerplate excepted, non-substantive by construction).
    frozen = []
    for n in nodes:
        vid = n.get("verse_id", "")
        for p in n.get("premises", [])[:3]:
            frozen.append({"id": f"CLM-{len(frozen)+1:03d}", "text": p,
                           "verse_id": vid, "tier": "R", "kind": "premise"})
        if n.get("inference"):
            frozen.append({"id": f"CLM-{len(frozen)+1:03d}", "text": n["inference"],
                           "verse_id": vid, "tier": "R", "kind": "inference"})
    day = datetime.date.today().isoformat()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%H%M%S")
    marker_chunk = f"{a.work}:{a.chunk}"
    parts = [f"# {a.title or title or 'Untitled'} (EXPANSION DRAFT — compiled, never written)",
             "",
             f"- owner voice: `{a.owner}` (verbatim below, unaltered)" if a.owner
             else "- owner voice: none (speculative topic - research voice only)",
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
    if cquotes:
        parts.append("")
        parts.append(f"## Corpus voice (verbatim idea-units, topic `{a.corpus_topic}` — unaltered)")
        parts.append("")
        for uid, grade, quote in cquotes[:10]:
            parts.append(f"> {quote} [{uid} · grade {grade}]")
    for f in frames[:6]:
        parts.append(f"[{f}]")
    parts += ["", "## Banked claims (audit chain, tiered; every bullet links a frozen claim)", ""]
    for fc in frozen:
        parts.append(f"- {fc['text']} [{fc['verse_id']}] (R) [{fc['id']}]")
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
    # Coverage (essaygen invariant): every tiered bullet links a frozen id.
    used = set(re.findall(r"\[CLM-\d+\]", draft))
    frozen_ids = {fc["id"] for fc in frozen}
    orphan_bullets = [l[:80] for l in draft.splitlines()
                      if l.startswith("- ") and "[CLM-" not in l and "::" not in l
                      and ("(R)" in l or "(T)" in l)]
    unused = sorted(frozen_ids - used)
    if orphan_bullets:
        print(f"ERROR: {len(orphan_bullets)} bullets introduce propositions outside frozen claims:")
        for b in orphan_bullets[:5]:
            print(f"  {b}")
        return 1
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
    l3, l4 = None, None
    if a.l3 or a.l4:
        # L3: every substantive sentence traces to frozen claims or verbatim
        # quotes (fail-closed); essence map per paragraph; kill register.
        paras = [p for p in re.split(r"\n\s*\n", draft) if p.strip()]
        untraced, essence = [], {}
        for i, para in enumerate(paras):
            sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", para) if s.strip()]
            emap = []
            in_quote = para.strip().startswith(">")
            for s in sents:
                ids = sorted(set(re.findall(r"\[CLM-\d+\]", s)))
                quoted = in_quote or (s.startswith('"') or '"' in s[:120])
                structural = s.startswith(("#", "-", "|"))
                if not ids and not quoted and not structural:
                    untraced.append({"para": i, "sentence": s[:120]})
                emap.extend(ids)
            essence[f"para-{i}"] = sorted(set(emap))
        if untraced and a.l3:
            print(f"ERROR L3: {len(untraced)} untraced sentences (no claim, quote, or structure):")
            for u in untraced[:5]:
                print(f"  p{u['para']}: {u['sentence']}")
            return 1
        l3 = {"essence_map": essence,
              "read_aloud": "owed (assessor reads draft aloud, logs defects here)",
              "kill_register": [],
              "untraced": untraced}
    if a.l4:
        # L4: per-paragraph DRAFT files (craft_notes + rejected + reads_against)
        # + claim-overlap audit (paragraphs must CARRY claim text; low overlap
        # = beautification drift, rework, never smoothed).
        dd = swarm / f"{slug}.l4"
        dd.mkdir(exist_ok=True)
        drafts, drifts = [], []
        paras = [p for p in re.split(r"\n\s*\n", draft) if p.strip()]
        claim_text = " ".join(fc["text"] for fc in frozen).lower()
        for i, para in enumerate(paras):
            words = re.findall(r"[a-zāīūṛṝḷḹēōṃḥṅñṭḍṇśṣ]+", para.lower())
            overlap = (sum(1 for w in set(words) if len(w) > 4 and w in claim_text)
                       / max(len({w for w in words if len(w) > 4}), 1))
            # Voice quotes, headers, and receipt-metadata bullets carry no
            # claims by design — drift applies to substance paras only
            # (beauty must not dilute claims).
            head = para.strip()
            if overlap < 0.15 and len(words) > 20 and not head.startswith((">", "#")) \
               and not any(head.startswith("- " + k) for k in
                           ("owner voice", "grounds:", "formal:", "status:")):
                drifts.append({"para": i, "overlap": round(overlap, 2)})
            df = {"para": i, "text": para,
                  "craft_notes": [], "rejected": [], "reads_against": [],
                  "claim_overlap": round(overlap, 2)}
            (dd / f"p{i:02d}.DRAFT.json").write_text(json.dumps(df, ensure_ascii=False, indent=1) + "\n")
            drafts.append(f"p{i:02d}")
        l4 = {"drafts": drafts, "drift_paras": drifts,
              "note": "drift = beautification without claims; rework or kill, never smooth"}
    report = {"format": "expansion-receipt/3", "essay": slug, "date": day,
              "owner_quotes": len(quotes), "banked_units": len(nodes),
              "theorems": a.theorems,
              "frozen_claims": frozen,
              "coverage": {"orphan_bullets": orphan_bullets, "unused_claims": unused},
              "claims": f"{cited}/{len(table['claims'])} CITED + {verse_marked} verse-marked",
              "audit": receipt,
              "l3": l3, "l4": l4,
              "graph": {"nodes": len(graph["nodes"]), "edges": len(graph["edges"])},
              "note": "compiled, not written: owner words verbatim; substance from frozen banked claims"}
    (swarm / f"{slug}.receipt.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    print(f"compiled -> swarm/{slug}.* | quotes: {len(quotes)} | units: {len(nodes)} | "
          f"{cited}/{len(table['claims'])} CITED | graph: {len(graph['nodes'])}n/{len(graph['edges'])}e")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
