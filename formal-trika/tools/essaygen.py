#!/usr/bin/env python3
"""essaygen.py — write a grounded essay from the Tantrasara argmap corpus.

The writer is deliberately narrow: it receives *retrieved* Sanskrit, the
L2/L3 translation, the argmap premises/uncertainties, and a frozen skeleton;
it writes prose around those slots. It may not invent Sanskrit, may not
introduce a verse that is not in the packet, and must mark every doctrinal
sentence with a verse id.

Model routing lives in go_client.py:
  primary  muse-spark-1.3-contributor   (/responses)
  fallback mimo-v2.6-flash             (/chat/completions)

  python3 tools/essaygen.py --work tantrasara-a08 --chunk tsa08-p01 \
    --title "Causality Is Agency" --words 3000 --allow-external-text

Output: swarm/essay-<slug>-<date>.md + .receipt.json
Status: MACHINE-COMPILED. Nothing here signs or publishes.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import go_client  # noqa: E402

TW = Path(os.environ.get("TRANSLATION_WORK", "/root/translation-work"))
SVREAD = Path(os.environ.get("SVREAD_CHECKOUT", "/root/svread"))
NODES = HERE / "data" / "argmap-nodes.jsonl"

SKELETON = [
    ("Abstract", 130),
    ("Introduction", 300),
    ("Historical Context", 350),
    ("Literature and Method", 350),
    ("The Doctrinal Context", 300),
    ("Encountering the Interlocutor", 500),
    ("The Argument I", 600),
    ("The Argument II", 600),
    ("Objections and Replies", 600),
    ("The Synthesis", 320),
    ("Conclusion", 300),
    ("References", 80),
]

SYSTEM = """You are a scholar of Kashmirian Trika Saivism writing a peer-review-grade essay.
You write argumentative prose, not a summary. You give the opponent the strongest form of
their objection, answer from the primary author, and only then state what follows.
You never invent Sanskrit, never invent a verse, never invent a citation.
You treat machine-proposed translations as drafts, not as established readings."""

PROMPT = """Write the essay "{title}" from the GROUND PACKET below.

MOVE GRAMMAR (every substantive section):
1. Exposition: state the position in its own terms.
2. Objection: give the rival the strongest form of their argument.
3. Reply: answer from the primary author/commentator with a cited verse.
4. Consequence: say what follows for the thesis.
Do not announce the thesis at the start; earn it and name it in the Conclusion.

VERSE PROTOCOL (mandatory):
- Quote Sanskrit ONLY from a `sanskrit:` field below, verbatim. Never alter a syllable.
- Give a short gloss using the `l3:` or `l2:` line for that verse.
- After every doctrinal sentence, cite the verse id in square brackets, e.g. [tsa-a08-v13].
- Where the packet lists `uncertainty:`, keep the reading open; do not smooth it.
- Do not cite any work, verse or author not present in the packet.

SHAPE (target {words} words overall):
{shape}

HARD RULES:
- Markdown. One `##` heading per section, in the order above.
- No preamble, no "here is the essay".
- Cite at least 8 secondary sources from LITERATURE as [Author Year, via Kaul 2022].
- Ask at least 10 questions across the essay (argumentative scaffolding, not rhetorical filler).
- Make 4-6 explicit authorial claims ("I argue", "this essay shows").
- End the Conclusion with a desideratum: name what remains unresolved.
- The References section lists the verse ids actually cited, one per line, then a Secondary list.

LITERATURE (secondary; attribute every claim as [Author Year, via Kaul 2022]):
{literature}

GROUND PACKET (Tantrasara primary; {work}:{chunk}):
{ground}

{context}"""



COMPARATIVE_SKELETON = [
    ("Abstract", 140),
    ("Introduction: Two Accounts of the Primary", 380),
    ("The Question Stated", 320),
    ("Being as Primary Cause (Aquinas)", 800),
    ("Consciousness as Primary Cause (Abhinavagupta)", 800),
    ("The Crux: Esse or Cit?", 700),
    ("Mediating Orders: Angels and Tattvas/Deities", 700),
    ("Causation: Creation and Manifestation", 650),
    ("Objection and Disanalogy", 600),
    ("Conclusion", 300),
    ("References", 120),
]

COMPARATIVE_PROMPT = """Write the comparative essay "{title}" from the TWO GROUND PACKETS below.

This is a comparison of two positions, not an identity claim. Your job is to state each
position in its own terms, put them under real pressure, and say exactly where they meet
and where they do not.

MOVE GRAMMAR (every substantive section):
1. Exposition of position A in its own vocabulary.
2. Exposition of position B in its own vocabulary.
3. The strongest objection each poses to the other.
4. Reply, then consequence for the comparison.
Do not announce the thesis early. Earn it; name it in the Conclusion.

CITATION PROTOCOL (mandatory):
- Cite Aquinas as [ST I, q.N, a.M] using ONLY citations present in the packet.
- Cite Abhinavagupta as [tsa-a08-vNN] using ONLY verse ids present in the packet.
- Quote Sanskrit ONLY from a `sanskrit:` field, verbatim. Never invent a verse or a citation.
- Do not import a third author (Hoffman, Levin, Faggin) into this essay.

THE FOUR AXES (address each explicitly):
1. What is primary: being (esse) or consciousness/agency (cit, kartr)?
2. The mediating order: angels as created immaterial substances vs tattvas/saktis/deities
   as levels or powers of one manifestation.
3. Causation: creation ex nihilo and secondary causes vs abhasa/manifestation and svatantrya.
4. Knowledge and naming: analogy of being vs recognition (pratyabhijna) and vimarsa.

MANDATORY DISANALOGY SECTION:
State at least three places where the comparison breaks. Name the temptation to equate
maya with createdness, Siva with ipsum esse, or angels with tattvas, and refuse it unless
the packet supports it.

SHAPE (target {words} words overall):
{shape}

HARD RULES:
- Markdown. One `##` heading per section, in the order above.
- No preamble. No "here is the essay".
- Every doctrinal sentence carries a citation.
- Cite at least 8 secondary sources from LITERATURE as [Author Year, via Kaul 2022].
- Ask at least 10 questions and make 4-6 explicit authorial claims.
- End with a desideratum paragraph.
- References: list the ST citations, the verse ids, and the secondary sources, in labelled groups.

PACKET A — ABHINAVAGUPTA (Tantrasara primary; {work}:{chunk}):
{ground}

PACKET B — AQUINAS ({external_label}):
{external}

LITERATURE (secondary; attribute every claim as [Author Year, via Kaul 2022]):
{literature}

{context}"""

def load_nodes(work: str, chunk: str, verses: list[str]) -> list[dict]:
    out = []
    for line in NODES.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if d.get("work") != work:
            continue
        if verses and d.get("verse_id") not in verses:
            continue
        if not verses and d.get("locator") != chunk:
            continue
        out.append(d)
    return out


def layers_for(work_slug: str, verse_id: str) -> dict:
    try:
        sys.path.insert(0, str(SVREAD / "mcp"))
        import scholar_server as srv
        r = srv.passage_layers({"work": work_slug, "target": verse_id})
        return r.get("layers", {})
    except Exception:
        return {}


def layer(L: dict, key: str):
    v = L.get(key)
    if isinstance(v, dict):
        return v.get("data")
    return v


def one(v: list | None, key: str, default=""):
    if not v:
        return default
    d = v[0]
    return d.get(key, default)


def build_ground(nodes: list[dict], work_slug: str) -> tuple[str, list[str]]:
    lines, cited = [], []
    for n in nodes:
        vid = n["verse_id"]
        cited.append(vid)
        L = layers_for(work_slug, vid)
        src = one(layer(L, "l3"), "sanskrit_cite") or one(layer(L, "l2"), "sanskrit_cite")
        l3 = " ".join(one(layer(L, "l3"), "lines", []) or [])
        l2 = one(layer(L, "l2"), "plain_english")
        t1 = one(layer(L, "t1"), "quick_english")
        lines.append(f"\n[{vid}] speaker: {n.get('speaker','')} | question: {n.get('question','')}")
        if src:
            lines.append(f"  sanskrit: {src}")
        if l3:
            lines.append(f"  l3: {l3}")
        if l2 and l2 != l3:
            lines.append(f"  l2: {l2}")
        if not l3 and not l2 and t1:
            lines.append(f"  t1: {t1}")
        for p in (n.get("premises") or [])[:4]:
            lines.append(f"  premise: {p}")
        if n.get("inference"):
            lines.append(f"  inference: {n['inference']}")
        for u in (n.get("uncertainties") or [])[:3]:
            lines.append(f"  uncertainty: {u}")
    return "\n".join(lines), cited


def polish(text: str) -> str:
    """Remove machine seams before a reader sees the draft."""
    text = re.sub(r"(?im)^>?\s*Draft gloss \((?:after )?l3\):\s*", "> ", text)
    text = re.sub(r"(?im)^\s*Draft gloss \((?:after )?l3\):\s*", "", text)
    text = re.sub(r"\bExposition[:,\s]+(?=[A-Z])", "", text)
    text = re.sub(r"\bExposition[:,\s]+(?=[a-z])", "", text)
    text = re.sub(r"\bObjection,\s*in its strongest form[:,\s]*", "The strongest objection: ", text)
    text = re.sub(r"\bObjection[:,\s]+(?=[A-Z])", "The objection: ", text)
    text = re.sub(r"\bReply[:,\s]+(?=[A-Z])", "The reply: ", text)
    text = re.sub(r"\bConsequence[:,\s]+(?=[A-Z])", "The consequence: ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", default="tantrasara-a08")
    ap.add_argument("--chunk", default="tsa08-p01")
    ap.add_argument("--verses", nargs="*", default=[])
    ap.add_argument("--title", default="Causality Is Agency")
    ap.add_argument("--words", type=int, default=3000)
    ap.add_argument("--context-file", type=Path, default=None,
                    help="optional context (e.g. Tantraloka L2 excerpt); never a claim source")
    ap.add_argument("--external-json", type=Path, default=None,
                    help="comparative packet B: {articles:[{citation,title,text}]}")
    ap.add_argument("--external-label", default="Aquinas, Summa Theologiae")
    ap.add_argument("--comparative", action="store_true")
    ap.add_argument("--literature-json", type=Path, default=None,
                    help="lit-review.json with a prompt_block")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--allow-external-text", action="store_true",
                    help="required: permits sending retrieved corpus excerpts to the model")
    a = ap.parse_args()
    if not a.allow_external_text:
        print("ERROR: --allow-external-text is required before sending corpus text externally",
              file=sys.stderr)
        return 1
    work_slug = a.work.split("-")[0]  # tantrasara-a08 -> tantrasara
    nodes = load_nodes(a.work, a.chunk, a.verses)
    if not nodes:
        print(f"ERROR: no argmap nodes for {a.work}:{a.chunk}", file=sys.stderr)
        return 1
    ground, cited = build_ground(nodes, work_slug)
    context = ""
    if a.context_file and a.context_file.is_file():
        ctx = a.context_file.read_text(encoding="utf-8", errors="replace")[:12000]
        context = ("CONTEXT (Tantraloka / secondary; use for framing only, never quote as "
                   "primary evidence):\n" + ctx)
    external, ext_sources = "", []
    if a.external_json and a.external_json.is_file():
        data = json.loads(a.external_json.read_text(encoding="utf-8"))
        arts = data.get("articles", data) if isinstance(data, dict) else data
        for art in arts:
            cit = art.get("citation", "")
            title = art.get("title", "")
            text = art.get("text", "")
            ext_sources.append({"citation": cit, "title": title,
                                "text_sha256": hashlib.sha256(text.encode()).hexdigest()})
            external += f"\n[{cit}] {title}\n  {text[:1500]}\n"
    literature = ""
    if a.literature_json and a.literature_json.is_file():
        literature = json.loads(a.literature_json.read_text(encoding="utf-8")).get("prompt_block", "")
    comparative = a.comparative or bool(a.external_json)
    skel = COMPARATIVE_SKELETON if comparative else SKELETON
    total = sum(w for _, w in skel)
    shape = "\n".join(f"- {t}: ~{round(w * a.words / total)} words" for t, w in skel)
    if comparative:
        prompt = COMPARATIVE_PROMPT.format(
            title=a.title, words=a.words, shape=shape, work=a.work, chunk=a.chunk,
            ground=ground, context=context, external=external,
            external_label=a.external_label, literature=literature)
    else:
        prompt = PROMPT.format(title=a.title, words=a.words, shape=shape, work=a.work,
                               chunk=a.chunk, ground=ground, context=context,
                               literature=literature)
    print(f"ground: {len(nodes)} verses, prompt {len(prompt)} chars; writing ~{a.words} words")
    try:
        r = go_client.complete(prompt, system=SYSTEM, max_tokens=a.max_tokens,
                               temperature=0.6)
    except go_client.GoError as e:
        print(f"ERROR: writer failed: {e}", file=sys.stderr)
        return 2
    text = polish(r["text"].strip())
    day = datetime.date.today().isoformat()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", a.title.lower()).strip("-")[:48]
    swarm = HERE / "swarm"
    swarm.mkdir(exist_ok=True)
    base = f"essay-{slug}-{day}-{stamp}"
    (swarm / f"{base}.md").write_text(text + "\n", encoding="utf-8")
    found = sorted(set(re.findall(r"\b(?:tsa|tal|ipk|ipv)-[a-z0-9]+-v\d+\b", text)))
    receipt = {
        "format": "essaygen-receipt/1",
        "essay": base,
        "mode": "comparative" if comparative else "single-tradition",
        "date": day,
        "status": "MACHINE-COMPILED",
        "title": a.title,
        "work": a.work,
        "chunk": a.chunk,
        "verses_supplied": cited,
        "verses_cited": found,
        "verse_citation_coverage": round(len(set(found)) / max(1, len(cited)), 3),
        "model": r["model"],
        "fallback_used": r["fallback"],
        "usage": r.get("usage", {}),
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "ground_sha256": hashlib.sha256(ground.encode()).hexdigest(),
        "external_sources": ext_sources,
        "words": len(text.split()),
        "note": ("grounded in retrieved argmap/L2/L3; prose machine-written; "
                 "no human sign-off; witness UNPINNED"),
    }
    (swarm / f"{base}.receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"draft -> swarm/{base}.md ({receipt['words']} words) | "
          f"model {r['model']} (fallback={r['fallback']}) | "
          f"verse coverage {receipt['verse_citation_coverage']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
