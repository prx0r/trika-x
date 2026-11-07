#!/usr/bin/env python3
"""seed_abhinavagupta.py — Abhinavagupta corpus completion seed for the box DB.

Loads (into the LOCAL box DB only; never into any repo):
  1. person:abhinavagupta + missing Abhinavagupta translators (Gnoli etc.
     already exist from the atlas seed — skipped by ON CONFLICT).
  2. lost-*/attested-* works rows (finding-aid provenance, NO edition/
     witness/etext claims — a lost work has no manuscript to pin).
  3. assertions: TITLE/AUTHOR/LANGUAGE (observed) + STATUS (reported:
     LOST vs ATTESTED-UNVERIFIED, with basis in the literal).
  4. Tantraloka dossier-equivalent: TITLE/AUTHOR/LANGUAGE assertions +
     KSTS-23 edition row + 5 translation rows from the live-verified
     Nov-6 bibliography (rights UNKNOWN unless stated).
  5. Ours translations: seed:ours:<work>:t0 for every translation-work
     workdir (REGISTRY gold flag -> OURS-GOLD-MACHINE-PROPOSED, else
     OURS-PENDING; human review pending; GATE.json per work is the gate).

Rules (mirror seed_atlas_biblio.py): deterministic seed: ids,
dry-run default, --apply writes with ON CONFLICT DO NOTHING, rights never
upgraded, work_id FKs respected (lost works are new works rows; every
translation/edition references an existing work row), provenance_refs cite
the JSON seed + REGISTRY + Wikipedia finding aid (finding aid only — verify
via Rastogi 1987 / Torella / GRETIL author listing before stronger claims).

Reads (never writes): formal-trika/data/abhinavagupta-corpus.json,
translation-work/REGISTRY.json. Writes ONLY the local box DB.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data" / "abhinavagupta-corpus.json"
TW = Path("/root/translation-work")
DSN_DFT = "postgresql://patala:patala@localhost:5432/openpatala"
SEED = "seed:trika:abhinavagupta-corpus:1"
EVENT = "seed:abhinavagupta-corpus-load"
WIKI = "https://en.wikipedia.org/wiki/Abhinavagupta"


def slug(name: str) -> str:
    import re
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s or "unknown"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dsn", default=DSN_DFT)
    a = ap.parse_args()
    corpus = json.loads(DATA.read_text(encoding="utf-8"))
    reg = json.loads((TW / "REGISTRY.json").read_text(encoding="utf-8"))
    reg_sha = hashlib.sha256((TW / "REGISTRY.json").read_bytes()).hexdigest()
    gold = {w["work"]: bool(w.get("gold")) for w in reg.get("works", [])}
    dirs = sorted(p.name for p in TW.iterdir()
                  if p.is_dir() and (p / "passages.jsonl").exists())
    assert len(dirs) == 87, f"expected 87 ledger works, got {len(dirs)}"

    import psycopg2
    from psycopg2.extras import Json
    cx = psycopg2.connect(a.dsn)
    cur = cx.cursor()
    cur.execute("SELECT id FROM works")
    have_works = {r[0] for r in cur.fetchall()}
    cur.execute("SELECT id FROM people")
    have_people = {r[0] for r in cur.fetchall()}

    plan = {"people": [], "works": [], "assertions": [],
            "editions": [], "translations": [], "skipped": []}

    # 1. people
    for name in corpus["people_extra"]:
        pid = f"person:{slug(name)}"
        if pid not in have_people:
            plan["people"].append((pid, name))

    # 2+3. lost/attested works + assertions
    for w in corpus["works_lost_or_unverified"]:
        wid = w["slug"]
        if wid not in have_works:
            plan["works"].append((wid, w["title"], "TEXT", None,
                                  Json({"finding_aid": WIKI,
                                        "note": w.get("note", ""),
                                        "status": w["status"],
                                        "status_basis": w["status_basis"],
                                        "verify": "Rastogi 1987 / Torella / GRETIL author listing"})))
        base = wid
        plan["assertions"].append(
            (f"SEEDAS_{wid}_title", wid, "TITLE", None, w["title"],
             "observed", [], SEED, None, EVENT))
        plan["assertions"].append(
            (f"SEEDAS_{wid}_author", wid, "AUTHOR", None, "Abhinavagupta",
             "observed", [], SEED, None, EVENT))
        plan["assertions"].append(
            (f"SEEDAS_{wid}_language", wid, "LANGUAGE", None, "sa",
             "observed", [], SEED, None, EVENT))
        plan["assertions"].append(
            (f"SEEDAS_{wid}_status", wid, "STATUS", None,
             f"{w['status']}: {w['status_basis']}",
             "reported", [], SEED, None, EVENT))

    # 4. Tantraloka dossier-equivalent (work row must exist via atlas seed)
    if "tantraloka" not in have_works:
        plan["skipped"].append("tantraloka (no works row — atlas seed missing?)")
    else:
        for pred, lit in (("TITLE", "Tantrāloka"), ("AUTHOR", "Abhinavagupta"),
                          ("LANGUAGE", "sa")):
            plan["assertions"].append(
                (f"SEEDAS_tantraloka_{pred.lower()}", "tantraloka", pred,
                 None, lit, "observed", [], SEED, None, EVENT))
        plan["editions"].append(
            ("seed:trika:tantraloka:e0", "tantraloka",
             corpus["tantraloka_edition"]["title"] + " [edition; prov: trika biblio-abhinavagupta 2026-11-06]",
             [], None))
        for n, t in enumerate(corpus["tantraloka_translations"]):
            if t.get("skip"):
                continue  # atlas-covered (see note); keeps t<N> ids stable
            who = t["translator"]
            pid = f"person:{slug(who)}"
            plan["translations"].append(
                (f"seed:trika:tantraloka:t{n}", "tantraloka", "eng", [pid],
                 "COMPLETE" if t["coverage"] == "COMPLETE" else "PARTIAL",
                 [], [f"trika biblio-abhinavagupta 2026-11-06 ({t['title']})",
                      f"rights: UNKNOWN (link/biblio only, never copy)"]))

    # 5. ours translations for all 101 workdirs
    for d in sorted({w["work"] for w in reg.get("works", [])}):
        if d not in have_works:
            plan["skipped"].append(f"{d} (no works row)")
            continue
        comp = ("OURS-GOLD-MACHINE-PROPOSED" if gold.get(d)
                else "OURS-PENDING")
        plan["translations"].append(
            (f"seed:ours:{d}:t0", d, "eng", ["translation-work"], comp, [],
             [f"translation-work REGISTRY.json sha256:{reg_sha}",
              "human review pending; per-work GATE.json is the gate",
              "machine-proposed layers, never final until signed"]))

    print(f"people: {len(plan['people'])}; works: {len(plan['works'])}; "
          f"assertions: {len(plan['assertions'])}; editions: {len(plan['editions'])}; "
          f"translations: {len(plan['translations'])}; skipped: {plan['skipped']}")
    if not a.apply:
        print("dry-run (no writes). Pass --apply to insert.")
        return 0
    for pid, name in plan["people"]:
        cur.execute("INSERT INTO people (id, preferred_name, external_ids) "
                    "VALUES (%s,%s,'[]'::jsonb) ON CONFLICT (id) DO NOTHING",
                    (pid, name))
    for wid, title, wtype, cur_title, ext in plan["works"]:
        cur.execute("INSERT INTO works (id, preferred_title, work_type, "
                    "current_title_assertion_id, external_ids) "
                    "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING",
                    (wid, title, wtype, cur_title, ext))
    for (i, s, p, o, lit, mode, ev, by, actor, event) in plan["assertions"]:
        cur.execute("INSERT INTO assertions (id, subject_id, predicate_uri, "
                    "object_id, literal, epistemic_mode, evidence_use_ids, "
                    "asserted_by, actor_ref, recorded_at, created_from_event) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s) "
                    "ON CONFLICT (id) DO NOTHING",
                    (i, s, p, o, lit, mode, ev, by, actor, event))
    for eid, wid, title, ext, rights in plan["editions"]:
        cur.execute("INSERT INTO editions (id, work_id, title, external_ids, rights_policy_id) "
                    "VALUES (%s,%s,%s,'[]'::jsonb,NULL) ON CONFLICT (id) DO NOTHING",
                    (eid, wid, title))
    for tid, wid, lang, tr, comp, ext, prov in plan["translations"]:
        cur.execute("INSERT INTO translations (id, work_id, target_language, translator_ids, "
                    "completeness, external_ids, provenance_refs) "
                    "VALUES (%s,%s,%s,%s,%s,'[]'::jsonb,%s) ON CONFLICT (id) DO NOTHING",
                    (tid, wid, lang, tr, comp, prov))
    cx.commit()
    print(f"applied (idempotent). seed={SEED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
