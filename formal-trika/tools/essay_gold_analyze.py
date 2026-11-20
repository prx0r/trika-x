#!/usr/bin/env python3
"""essay_gold_analyze.py — reverse-engineer the structure of a gold-standard essay.

Takes a peer-reviewed essay (PDF or a pdftotext -layout .txt) and emits a
machine-readable skeleton plus a rhetorical feature table, so the essay
factory can learn "what a good chapter does" from real published work
instead of inventing a format.

This tool measures FORM, not truth. It never judges whether a claim is
correct; it reports how the prose is built: section architecture, paragraph
roles, citation density, primary-source quotation discipline, objection /
reply moves, and where the author speaks in the first person.

  python3 tools/essay_gold_analyze.py paper.pdf --out structure.json
  python3 tools/essay_gold_analyze.py paper.txt --title "..." --json

Exit 0 = analysed. Exit 2 = input unreadable (named reason on stderr).
Stdlib only; pdftotext is used only when given a PDF.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Section roles the handbook genre uses. Matched case-insensitively against a
# detected heading; anything unmatched is left as its own role "body".
ROLE_HINTS = [
    ("abstract", ["abstract", "summary"]),
    ("keywords", ["keywords", "key words"]),
    ("abbreviations", ["abbreviation", "abbreviations", "sigla"]),
    ("introduction", ["introduction", "introductory"]),
    ("history", ["historical context", "history", "background", "context"]),
    ("method", ["method", "approach", "rationalization", "philosophical rationalization"]),
    ("interlocutor", ["encountering", "opponents", "interlocutors", "buddhists", "rivals"]),
    ("argument", ["the seed", "the sprout", "causality", "argument", "analysis"]),
    ("case", ["meditator", "desire", "example", "case study"]),
    ("synthesis", ["complex causality", "totality", "synthesis"]),
    ("thesis", ["perfect agent", "autonomous", "agency"]),
    ("conclusion", ["conclusion", "concluding", "closing"]),
    ("references", ["references", "bibliography", "works cited",
                    "primary sources", "secondary sources", "editions",
                    "abbreviations and editions"]),
]

DIACRITICS = set("āīūṛṝḷḹṃḥśṣṭḍṇñṅĀĪŪṚṜḶḸṂḤŚṢṬḌṆÑṄ")

OBJECTION = re.compile(
    r"\b(opponent|objection|objects?|argues? (?:that|saying)|would say|it may be (?:said|argued)|"
    r"one might (?:ask|say|object)|the buddhists? (?:say|argue|maintain|hold)|if .{0,60} then)\b",
    re.I)
REPLY = re.compile(
    r"\b(we reply|the reply|in response|abhinavagupta (?:says|argues|maintains|points out|asks)|"
    r"jayaratha (?:says|writes|asks|tells|adds|maintains)|therefore|hence|thus|it follows|"
    r"so we are forced|the conclusion)\b", re.I)
INFERENCE = re.compile(r"\b(if|then|since|because|therefore|hence|thus|consequently|it follows|must|"
                       r"cannot|could not|impossible|necessarily)\b", re.I)
AUTHOR_CLAIM = re.compile(r"\b(I (?:argue|show|suggest|propose|claim|will demonstrate|have chosen)|"
                          r"this (?:paper|chapter|essay) (?:argues|shows|demonstrates|focuses)|"
                          r"in this (?:paper|chapter)|my (?:aim|argument|focus))\b", re.I)
HEDGE = re.compile(r"\b(perhaps|probably|may|might|seems?|appears?|likely|it is possible|"
                   r"arguably|in some sense|one could)\b", re.I)
CITATION = re.compile(
    r"\((?P<body>[A-Z][^()]{0,120}?\d{4}[a-z]?[^()]{0,40}?)\)")
NARRATIVE_CITE = re.compile(
    r"\b(?:see|cf\.|also see|as noted by|according to)\s+[A-Z][A-Za-z\u0100-\u017f]+"
    r"(?:\s+(?:and|&)\s+[A-Z][A-Za-z\u0100-\u017f]+)?\s*\(?\d{4}", re.I)
VERSE_REF = re.compile(r"\b(?:TĀ|TĀV|ĪPK|ĪPV|ĪPVV|MMK|ŚS|ŚSV|MŚV|MVUT|PHṛ|PTv|ŚD|SK|TS)"
                       r"\s*\d+(?:\.\d+)*[a-d]?\b")
SANSKRIT_QUOTE = re.compile(r"[^\n|]{5,}\|\|")
PAGE_HEADER = re.compile(r"^\s*(?:\d{1,3}\s+.*\s+\d{2,3}|\d{2,3})\s*$")


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        exe = shutil.which("pdftotext")
        if not exe:
            raise SystemExit("essay_gold_analyze: pdftotext not installed")
        r = subprocess.run([exe, "-layout", str(path), "-"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"essay_gold_analyze: pdftotext failed: {r.stderr.strip()}")
        return r.stdout
    return path.read_text(encoding="utf-8", errors="replace")


def clean_lines(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        s = line.rstrip()
        if PAGE_HEADER.match(s):
            continue
        out.append(s)
    return out


def is_heading(s: str) -> bool:
    t = s.strip()
    if not (3 <= len(t) <= 90):
        return False
    if t.endswith((".", ",", ";", ":")):
        return False
    words = t.split()
    if len(words) > 12:
        return False
    if not t[0].isupper():
        return False
    # Headings do not read like a wrapped sentence: keep title-case or short.
    caps = sum(1 for w in words if w[:1].isupper())
    return caps >= max(1, (len(words) + 1) // 2) or len(words) <= 3


def role_of(title: str) -> str:
    low = title.lower()
    for role, hints in ROLE_HINTS:
        for h in hints:
            if h in low:
                return role
    return "body"


def split_sections(lines: list[str]) -> list[dict]:
    heads = []
    for i, line in enumerate(lines):
        if not is_heading(line):
            continue
        prev_blank = i == 0 or not lines[i - 1].strip()
        next_blank = i + 1 >= len(lines) or not lines[i + 1].strip()
        # A named section (Abstract, References, ...) may sit flush against its
        # body text; only unknown short lines demand a blank line on both sides.
        known = role_of(line.strip()) != "body"
        if prev_blank and (next_blank or known):
            heads.append(i)
    # Drop a heading that is immediately followed by another (title/subtitle pairs).
    if not heads:
        heads = [0]
    sections = []
    for j, start in enumerate(heads):
        end = heads[j + 1] if j + 1 < len(heads) else len(lines)
        body = "\n".join(lines[start + 1:end]).strip()
        title = lines[start].strip()
        sections.append({"title": title, "role": role_of(title), "body": body,
                         "start_line": start, "end_line": end})
    return sections


def feats(body: str) -> dict:
    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    words = re.findall(r"\b[\w\u0100-\u017f'-]+\b", body)
    sents = re.split(r"(?<=[.!?])\s+", body)
    diacritic_words = [w for w in words if any(c in DIACRITICS for c in w)]
    return {
        "paragraphs": len(paras),
        "words": len(words),
        "sentences": len([s for s in sents if s.strip()]),
        "questions": body.count("?"),
        "citations_parenthetical": len(CITATION.findall(body)),
        "citations_narrative": len(NARRATIVE_CITE.findall(body)),
        "verse_refs": len(VERSE_REF.findall(body)),
        "sanskrit_quotes_versified": len(SANSKRIT_QUOTE.findall(body)),
        "diacritic_words": len(diacritic_words),
        "diacritic_density": round(len(diacritic_words) / len(words), 4) if words else 0,
        "objection_moves": len(OBJECTION.findall(body)),
        "reply_moves": len(REPLY.findall(body)),
        "inference_markers": len(INFERENCE.findall(body)),
        "author_claims": len(AUTHOR_CLAIM.findall(body)),
        "hedges": len(HEDGES(body)),
    }


def HEDGES(body: str):
    return HEDGE.findall(body)


def paragraph_roles(body: str) -> list[str]:
    roles = []
    for p in re.split(r"\n\s*\n", body):
        p = p.strip()
        if not p:
            continue
        if OBJECTION.search(p) and REPLY.search(p):
            roles.append("objection+reply")
        elif OBJECTION.search(p):
            roles.append("objection")
        elif REPLY.search(p):
            roles.append("inference/reply")
        elif AUTHOR_CLAIM.search(p):
            roles.append("author-thesis")
        elif CITATION.search(p) or NARRATIVE_CITE.search(p):
            roles.append("cited-context")
        else:
            roles.append("exposition")
    return roles


def analyze(text: str, title: str = "") -> dict:
    lines = clean_lines(text)
    raw = "\n".join(lines)
    sections = split_sections(lines)
    out_sections = []
    for s in sections:
        roles = paragraph_roles(s["body"])
        out_sections.append({
            "title": s["title"],
            "role": s["role"],
            "start_line": s["start_line"],
            "end_line": s["end_line"],
            "features": feats(s["body"]),
            "paragraph_roles": {
                r: roles.count(r) for r in sorted(set(roles))
            },
        })
    totals = {}
    for key in ("words", "paragraphs", "citations_parenthetical",
                "citations_narrative", "verse_refs", "sanskrit_quotes_versified",
                "objection_moves", "reply_moves", "inference_markers",
                "author_claims", "questions"):
        totals[key] = sum(s["features"][key] for s in out_sections)
    totals["sections"] = len(out_sections)
    totals["words_per_section"] = (round(totals["words"] / len(out_sections), 1)
                                   if out_sections else 0)
    # Six-move skeleton the chapter actually uses, named for reuse.
    skeleton = []
    for s in out_sections:
        if s["role"] in ("abstract", "keywords", "abbreviations", "references"):
            continue
        skeleton.append({"role": s["role"], "title": s["title"],
                         "words": s["features"]["words"]})
    return {
        "format": "essay-gold-structure/1",
        "note": "FORM only. Roles are heuristic; read them against the text.",
        "title": title,
        "totals": totals,
        "sections": out_sections,
        "skeleton": skeleton,
        "move_vocabulary": {
            "objection": sorted(set(m.lower() for m in OBJECTION.findall(raw))),
            "reply": sorted(set(m.lower() for m in REPLY.findall(raw)))[:20],
        },
    }


def summary(doc: dict) -> str:
    t = doc["totals"]
    lines = [f"title: {doc['title'] or '(unnamed)'}",
             f"sections: {t['sections']}  words: {t['words']}  "
             f"citations: {t['citations_parenthetical']}+{t['citations_narrative']}  "
             f"verse refs: {t['verse_refs']}  objections: {t['objection_moves']}  "
             f"replies: {t['reply_moves']}",
             "", "skeleton:"]
    for s in doc["skeleton"]:
        n = s["words"]
        bar = "#" * max(1, round(n / 60))
        lines.append(f"  {s['role']:<14} {s['title'][:48]:<50} {n:>5}w {bar}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="PDF or pdftotext -layout .txt")
    ap.add_argument("--title", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--json", action="store_true", help="print the JSON document")
    a = ap.parse_args()
    p = Path(a.path)
    if not p.is_file():
        print(f"essay_gold_analyze: no such file: {p}", file=sys.stderr)
        return 2
    try:
        text = read_text(p)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 - report, do not crash
        print(f"essay_gold_analyze: unreadable: {e}", file=sys.stderr)
        return 2
    doc = analyze(text, a.title or p.stem)
    if a.out:
        Path(a.out).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    print(json.dumps(doc, indent=2, ensure_ascii=False) if a.json else summary(doc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
