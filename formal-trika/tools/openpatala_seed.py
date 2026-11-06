#!/usr/bin/env python3
"""openpatala_seed.py — load box-available JSON seeds into the local openpatala DB.

Sources (all read-only, all hash-pinned upstream):
  - openpatala/data/translation-availability.json (260 works)
  - openpatala/data/gold/*.json (gold work dossiers: works/assertions/ids/events)
  - openpatala/data/evidence/evidence-bundle.json (if loadable)

Idempotent: every insert is ON CONFLICT DO NOTHING keyed by stable IDs.
Writes ONLY the local box database (default postgresql://patala:patala@
localhost:5432/openpatala); never writes into any repo. Run:
  python3 formal-trika/tools/openpatala_seed.py [--dsn DSN]
Prints per-table inserted/skipped counts (this run) + totals.
"""
import argparse
import json
import sys
from pathlib import Path

OPENPATALA = Path("/root/openpatala/data")


def upsert(cur, table, cols, rows, raw=None):
    from psycopg2.extras import Json
    raw = raw or {}
    ins = skipped = 0
    slots = ["%s" if i not in raw else raw[i] for i in range(len(cols))]
    col0 = cols[0]
    q = (f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(slots)}) "
         f"ON CONFLICT ({col0}) DO NOTHING RETURNING {col0}")

    def adapt(v):
        if isinstance(v, dict):
            return Json(v)
        return v  # lists pass through as ARRAY, scalars as-is

    for r in rows:
        vals = [adapt(v) for i, v in enumerate(r) if i not in raw]
        cur.execute(q, vals)
        if cur.fetchone():
            ins += 1
        else:
            skipped += 1
    return ins, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dsn", default="postgresql://patala:patala@localhost:5432/openpatala")
    a = ap.parse_args()
    import psycopg2
    con = psycopg2.connect(a.dsn)
    cur = con.cursor()
    rep = {}

    avail = json.loads((OPENPATALA / "translation-availability.json").read_text())
    works_rows = []
    for key, v in avail.get("works", {}).items():
        works_rows.append((key, key, "TEXT", None,
                           {"availability": {k: v.get(k) for k in
                                             ("has_english", "languages", "coverage", "missing",
                                              "translations", "copyright_hint") if k in v}}))
    rep["works_availability"] = upsert(cur, "works",
                                       ["id", "preferred_title", "work_type",
                                        "current_title_assertion_id", "external_ids"],
                                       works_rows)

    n_dossiers = 0
    w2, as2, ei2, ev2 = [], [], [], []
    for fp in sorted((OPENPATALA / "gold").glob("*.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(d, dict) or "work_id" not in d:
            continue
        n_dossiers += 1
        w2.append((d["work_id"], d.get("title", d["work_id"]),
                   d.get("work_type", "TEXT"), None, []))
        for x in d.get("assertions", []) or []:
            as2.append((x.get("id"), d["work_id"], x.get("predicate"),
                        x.get("object_id"), x.get("literal"),
                        x.get("epistemic_mode", "observed"), [], x.get("asserted_by"),
                        None, x.get("asserted_at"), "NOW", "ACTIVE",
                        "seed:gold-dossier-load", None))
        for x in d.get("external_identifiers", []) or []:
            ei2.append((x.get("id"), d["work_id"], x.get("scheme"),
                        x.get("value", x.get("identifier")), None, None))
        # Dossier events are ID+type stubs (occurred_at null, no payload/
        # schema). Loading them would fabricate event content, so they are
        # SKIPPED by design. The events table is reserved for real pipeline
        # events with full payloads. Decision recorded 2026-11-06.
        n_stub_events = len(d.get("events", []) or [])
    rep["dossiers"] = n_dossiers
    rep["dossiers"] = n_dossiers
    rep["works_dossiers"] = upsert(cur, "works",
                                   ["id", "preferred_title", "work_type",
                                    "current_title_assertion_id", "external_ids"], w2)
    rep["assertions"] = upsert(cur, "assertions",
                               ["id", "subject_id", "predicate_uri", "object_id", "literal",
                                "epistemic_mode", "evidence_use_ids", "asserted_by", "actor_ref",
                                "asserted_at", "recorded_at", "lifecycle", "created_from_event",
                                "supersedes"], as2, raw={10: "NOW()"})
    rep["external_identifiers"] = upsert(cur, "external_identifiers",
                                         ["id", "entity_id", "scheme", "value",
                                          "source_observation_id", "relation_confidence",
                                          "created_at"], [r + (None,) for r in ei2],
                                         raw={6: "NOW()"})
    con.commit()
    for k, v in rep.items():
        print(f"{k}: {v}")
    totals = {}
    for t in ("works", "assertions", "external_identifiers", "events",
              "editions", "witnesses", "etexts", "passages"):
        cur.execute(f"SELECT count(*) FROM {t}")
        totals[t] = cur.fetchone()[0]
    print("totals:", totals)
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
