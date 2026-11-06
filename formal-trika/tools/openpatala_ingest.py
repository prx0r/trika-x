#!/usr/bin/env python3
"""openpatala_ingest.py — O2/O3/O4/O7: works+editions+etexts+passages from repos.

Reads (never writes) translation-work standard layout + openpatala-map;
writes ONLY the local box DB (DSN default patala@localhost/openpatala).
Idempotent everywhere (ON CONFLICT DO NOTHING on stable IDs).

Per workdir with passages.jsonl:
  works:    id = openpatala_work_id (dossier-mapped) else workdir;
            availability/dossier rows already seeded (skip if present).
  editions: id = {workkey}:edition:1; title + external_ids [map edition
            string + dossier ext-id values]; rights_policy NULL (unknown).
  artifacts:id = sha256(source bytes); digests/media/byte_length;
            storage_uri = file:// local path (bytes stay on disk; R2 later).
  etexts:   id = {workkey}:etext:1; provider translation-work (or --provider);
            format text/plain, script Latn (IAST transliteration), lang sa.
  passages: id = immutable_id; work_id = works-row id used above;
            citation_scheme chunk-locator; citation_value locator;
            order_key = ledger order (nulls last).
Source file = first existing of SOURCE.txt/SOURCE.md/source.txt/
source/edition.json/source/record.json (recorded per work).
Mode B (--file/--work/--edition/--title): ingest one new Sanskrit work
from anywhere (O7): same rows under the given work key.

Usage:
  python3 formal-trika/tools/openpatala_ingest.py [--tw PATH] [--limit N]
  python3 formal-trika/tools/openpatala_ingest.py --file X.txt --work foo \\
      --edition "GRETIL ..." --title "Foo" [--provider NAME]
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MAP = json.loads((HERE / "bridge" / "openpatala-map.json").read_text())
SOURCE_CANDIDATES = ["SOURCE.txt", "SOURCE.md", "source.txt",
                     "source/edition.json", "source/record.json"]
BRIDGED = {"tantrasara-a08": "tsa08", "tantrasara-a07": "tsa07",
           "paramarthasara": "param", "phrdaya": "phr",
           "vbt": "vbt", "spanda": "spanda"}


def upsert(cur, table, cols, rows, raw=None, arrays=()):
    from psycopg2.extras import Json
    raw = raw or {}
    arrays = set(arrays)
    slots = ["%s" if i not in raw else raw[i] for i in range(len(cols))]
    q = (f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(slots)}) "
         f"ON CONFLICT ({cols[0]}) DO NOTHING RETURNING {cols[0]}")
    ins = 0
    for r in rows:
        vals = [(v if (isinstance(v, list) and cols[i] in arrays)
                 else (Json(v) if isinstance(v, (dict, list)) else v))
                for i, v in enumerate(r) if i not in raw]
        cur.execute(q, vals)
        if cur.fetchone():
            ins += 1
    return ins, len(rows) - ins


def work_key_for(workdir):
    b = BRIDGED.get(workdir)
    if b:
        wid = MAP["works"][b].get("openpatala_work_id", "")
        if wid and wid != "UNPINNED" and not wid.startswith("UNPINNED"):
            return b, wid
    return None, workdir


def ingest_work(cur, workkey, wid, title, edition_note, src_path, provider,
                passages):
    """passages: list of (immutable_id, locator, order). Returns counts."""
    counts = {}
    counts["works"] = upsert(cur, "works",
                             ["id", "preferred_title", "work_type",
                              "current_title_assertion_id", "external_ids"],
                             [(wid, title, "TEXT", None, [])])
    ext_ids = ([{"edition_note": edition_note}] if edition_note else [])
    counts["editions"] = upsert(cur, "editions",
                                ["id", "work_id", "title", "publication_assertions",
                                 "editor_assertions", "publisher_assertions",
                                 "year_assertions", "external_ids"],
                                [(f"{workkey}:edition:1", wid, title or workkey,
                                  [], [], [], [], ext_ids)])
    data = Path(src_path).read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    counts["artifacts"] = upsert(cur, "artifacts",
                                 ["id", "digests", "media_type", "byte_length",
                                  "storage_uri", "compression", "encoding",
                                  "rights_assessment_ids", "availability_state",
                                  "created_at"],                                 [(sha, {"sha256": sha}, "text/plain", len(data),
                                   f"file://{src_path}", None, "utf-8", [],
                                   "local-box")],
                                 raw={9: "NOW()"}, arrays={"rights_assessment_ids"})
    counts["etexts"] = upsert(cur, "etexts",
                              ["id", "work_id", "edition_id", "witness_id",
                               "provider_id", "artifact_id", "text_format",
                               "script", "language"],
                              [(f"{workkey}:etext:1", wid, f"{workkey}:edition:1",
                                None, provider, sha, "text/plain", "Latn", "sa")])
    prows = [(pid, loc, order if isinstance(order, int) else None)
             for pid, loc, order in passages]
    counts["passages"] = upsert(cur, "passages",
                                ["id", "work_id", "citation_scheme",
                                 "citation_value", "parent_passage_id", "order_key"],
                                [(pid, wid, "chunk-locator", loc, None, order)
                                 for pid, loc, order in prows])
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dsn", default="postgresql://patala:patala@localhost:5432/openpatala")
    ap.add_argument("--file", type=Path, default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--edition", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--provider", default="translation-work")
    a = ap.parse_args()
    import psycopg2
    con = psycopg2.connect(a.dsn)
    cur = con.cursor()
    tot = {"works": [0, 0], "editions": [0, 0], "artifacts": [0, 0],
           "etexts": [0, 0], "passages": [0, 0]}
    nworks = 0

    def acc(counts):
        for k, (i, s) in counts.items():
            tot[k][0] += i
            tot[k][1] += s

    if a.file:
        if not a.work:
            raise SystemExit("--work required with --file")
        passages = []
        counts = ingest_work(cur, a.work,
                             a.work, a.title or a.work, a.edition,
                             str(a.file), a.provider, passages)
        acc(counts)
        nworks = 1
    else:
        ledgers = sorted(a.tw.glob("*/passages.jsonl"))
        if a.limit:
            ledgers = ledgers[:a.limit]
        for ledger in ledgers:
            workdir = ledger.parent.name
            src = next((ledger.parent / c for c in SOURCE_CANDIDATES
                        if (ledger.parent / c).is_file()), None)
            if src is None:
                print(f"SKIP {workdir}: no source file")
                continue
            b, wid = work_key_for(workdir)
            edition_note = ""
            if b:
                edition_note = MAP["works"][b].get("edition", "")
            passages = []
            for line in ledger.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                r = json.loads(line)
                if r.get("locator"):
                    passages.append((r.get("immutable_id") or
                                     f"{workdir}:{r['locator']}",
                                     r["locator"], r.get("order")))
            acc(ingest_work(cur, workdir, wid, workdir, edition_note,
                            str(src), "translation-work", passages))
            nworks += 1
    con.commit()
    print(f"works processed: {nworks}")
    for k, (i, s) in tot.items():
        print(f"  {k}: inserted {i}, skipped {s}")
    cur.execute("SELECT (SELECT count(*) FROM works), (SELECT count(*) FROM editions), "
                "(SELECT count(*) FROM etexts), (SELECT count(*) FROM passages), "
                "(SELECT count(*) FROM witnesses)")
    print("db totals (works, editions, etexts, passages, witnesses):", cur.fetchone())
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
