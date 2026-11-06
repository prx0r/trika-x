#!/usr/bin/env python3
"""seed_atlas_biblio.py — feed patalacheckpoints atlas depth into the box DB.

Reads patalacheckpoints/data/atlas/audited.ts (verified Trika entries:
editions/textSources, translations, people) and seeds box openpatala
tables (people, editions, translations). The box DB won the one-system
verdict (only populated store); this is the migration, not a fork.

Rules: work_id must already exist in works (never invents identity);
deterministic IDs (seed:atlas:<slug>:p/e/t<N>); dry-run default;
--apply writes with ON CONFLICT DO NOTHING (idempotent reruns).
Rights: translations inherit source record rights where known, else
UNKNOWN (never upgraded). Provenance_refs cite the atlas file + rev.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ATLAS = Path(os.environ.get("PATALA_CHECKPOINTS", "/root/patalacheckpoints")) / "data" / "atlas" / "audited.ts"

DSN = os.environ.get("OPENPATALA_DSN", "dbname=openpatala user=patala password=patala host=127.0.0.1")


def git_rev(p: Path) -> str:
    import subprocess
    try:
        return subprocess.run(["git", "-C", str(p), "rev-parse", "--short", "HEAD"],
                              capture_output=True, check=True, text=True).stdout.strip()
    except Exception:
        return "UNKNOWN"


def split_entries(text: str) -> list:
    """Top-level {...} blocks of the exported array (brace matching)."""
    start = text.find("[")
    blocks, depth, cur = [], 0, None
    for i, ch in enumerate(text[start:]):
        if ch == "{":
            if depth == 0:
                cur = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and cur is not None:
                blocks.append(text[start + cur:start + i + 1])
                cur = None
    return blocks


def strs(block: str, key: str) -> list:
    m = re.search(key + r"\s*:\s*\[([^\]]*)\]", block)
    if not m:
        return []
    return re.findall(r'"([^"]*)"', m.group(1))


def field(block: str, key: str) -> str:
    m = re.search(key + r'\s*:\s*"([^"]*)"', block)
    return m.group(1) if m else ""


def objarray(block: str, key: str) -> list:
    m = re.search(key + r"\s*:\s*\[", block)
    if not m:
        return []
    i, depth, objs, cur = m.end(), 1, [], None
    while i < len(block) and depth > 0:
        ch = block[i]
        if ch == "{":
            if depth == 1:
                cur = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 1 and cur is not None:
                objs.append(block[cur:i + 1])
                cur = None
        elif ch == "]" and depth == 1:
            break
        i += 1
    out = []
    for o in objs:
        d = {}
        for k in re.findall(r"(\w+)\s*:", o):
            d[k] = field(o, k)
        d["_raw"] = o
        out.append(d)
    return out


def slug(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    text = ATLAS.read_text(encoding="utf-8")
    blocks = split_entries(text)
    entries = []
    for b in blocks:
        wid = field(b, "id")
        if not wid:
            continue
        entries.append({"id": wid, "work": field(b, "work"),
                        "verified": "verified: true" in b,
                        "textSources": objarray(b, "textSources"),
                        "translations": objarray(b, "translations")})
    import psycopg2
    cx = psycopg2.connect(DSN)
    cur = cx.cursor()
    cur.execute("SELECT id FROM works")
    have = {r[0] for r in cur.fetchall()}
    prov = f"atlas audited.ts @{git_rev(ATLAS.parent.parent.parent)}"
    people, editions, translations, skipped = {}, [], [], []
    for e in entries:
        if e["id"] not in have:
            skipped.append(e["id"] + " (no works row)")
            continue
        for n, t in enumerate(e["textSources"]):
            editions.append({"id": f"seed:atlas:{e['id']}:e{n}",
                            "work_id": e["id"], "title": t.get("provider", ""),
                            "url": t.get("url", ""), "tier": t.get("tier", ""),
                            "coverage": t.get("coverage", ""), "type": t.get("type", "")})
        for n, t in enumerate(e["translations"]):
            for who in [t.get("translator", "")]:
                if who:
                    people.setdefault(slug(who), who)
            translations.append({"id": f"seed:atlas:{e['id']}:t{n}", "work_id": e["id"],
                                 "lang": t.get("language", ""), "translator": t.get("translator", ""),
                                 "coverage": t.get("coverage", ""), "type": t.get("type", ""),
                                 "url": t.get("url", ""), "tier": t.get("tier", "")})
    print(f"entries: {len(entries)}; people: {len(people)}; editions: {len(editions)}; "
          f"translations: {len(translations)}; skipped: {skipped}")
    if not a.apply:
        print("dry-run (no writes). Pass --apply to insert.")
        return 0
    for pid, name in sorted(people.items()):
        cur.execute("INSERT INTO people (id, preferred_name, external_ids) VALUES (%s,%s,'[]'::jsonb) "
                    "ON CONFLICT (id) DO NOTHING", (f"person:{pid}", name))
    for e in editions:
        cur.execute("INSERT INTO editions (id, work_id, title, external_ids, rights_policy_id) "
                    "VALUES (%s,%s,%s,'[]'::jsonb,NULL) ON CONFLICT (id) DO NOTHING",
                    (e["id"], e["work_id"],
                     f"{e['title']} [{e['type']}/{e['coverage']}] {e['url']} (tier {e['tier']}; {prov})".strip()))
    for t in translations:
        tr = [f"person:{slug(t['translator'])}"] if t["translator"] else []
        cur.execute("INSERT INTO translations (id, work_id, target_language, translator_ids, completeness, external_ids, provenance_refs) "
                    "VALUES (%s,%s,%s,%s,%s,'[]'::jsonb,%s) ON CONFLICT (id) DO NOTHING",
                    (t["id"], t["work_id"], t["lang"] or "eng", tr,
                     "COMPLETE" if t.get("coverage") == "complete" else "PARTIAL",
                     [prov, t["url"]]))
    cx.commit()
    print(f"applied (idempotent). provenance: {prov}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
