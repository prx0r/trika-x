#!/usr/bin/env python3
"""Resolve a real passage ID against the pinned translation-work inventory.

This verifies locator membership, not the edition, witness or interpretation.
Without --tw, input comes from a checked-in metadata snapshot: an inventory,
not an independently verified live source. With --tw, the actual six ledger
files must match the pinned SHA-256 bytes. A witness stays UNPINNED until an
independent witness record is available; edition and witness are distinct.

Examples:
  python3 formal-trika/tools/bridge_resolve.py chunk:tsa08-p03
  python3 formal-trika/tools/bridge_resolve.py --check --tw ../translation-work
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent.parent
MAP_PATH = HERE / 'bridge' / 'openpatala-map.json'
CANDIDATES_PATH = HERE / 'bridge' / 'witness-candidates.json'
SNAPSHOT_PATH = HERE / 'bridge' / 'passages.snapshot.json'
EVIDENCE_PATH = HERE / 'EVIDENCE.json'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def inventory(snapshot, mapping, evidence):
    if snapshot.get('format') != 'trika-passage-snapshot/1':
        raise ValueError('unknown passage snapshot format')
    if not re.fullmatch(r'[0-9a-f]{40}', snapshot.get('revision', '')):
        raise ValueError('snapshot needs an exact 40-character Git revision')
    works = snapshot.get('works')
    if not isinstance(works, dict) or set(works) != set(mapping.get('works', {})) or set(works) != set(evidence.get('works', {})):
        raise ValueError('snapshot, bridge and evidence work sets must match')
    by_locator, ids = {}, set()
    for work, spec in works.items():
        meta = mapping['works'][work]
        if any(not meta.get(key) for key in ('ours', 'openpatala_work_key', 'edition', 'status')):
            raise ValueError(f'{work}: incomplete work-level mapping')
        if meta.get('witness') != 'UNPINNED':
            raise ValueError(f'{work}: witness is not independently verified; keep it UNPINNED')
        expected_ledger = evidence['works'][work].get('ledger', '')
        relative = spec.get('ledger', '')
        if expected_ledger != 'translation-work/' + relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise ValueError(f'{work}: invalid ledger mapping')
        if not re.fullmatch(r'[0-9a-f]{64}', spec.get('sha256', '')):
            raise ValueError(f'{work}: invalid ledger hash')
        passages = spec.get('passages')
        if not isinstance(passages, list) or not passages:
            raise ValueError(f'{work}: passage inventory missing')
        declared = evidence['works'][work].get('chunks', [])
        if [p.get('locator') for p in passages] != declared:
            raise ValueError(f'{work}: evidence chunk list differs from snapshot')
        for p in passages:
            loc, pid = p.get('locator'), p.get('immutable_id')
            if not isinstance(loc, str) or not loc or not isinstance(pid, str) or not pid:
                raise ValueError(f'{work}: missing locator or immutable ID')
            if loc in by_locator or pid in ids:
                raise ValueError(f'{work}: duplicate locator or immutable ID')
            by_locator[loc] = (work, p)
            ids.add(pid)
    for key, entry in evidence.get('entries', {}).items():
        for chunk in entry.get('chunks', []):
            loc = chunk.get('locator')
            if loc == 'vbt':  # historical work-level reference, not a passage
                continue
            if loc not in by_locator:
                raise ValueError(f'{key}: unknown passage {loc!r}')
    return by_locator


def verify_ledgers(tw, snapshot):
    for work, spec in snapshot['works'].items():
        p = tw / spec['ledger']
        if not p.is_file():
            raise ValueError(f'{work}: missing translation-work ledger {p}')
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != spec['sha256']:
            raise ValueError(f'{work}: passage ledger differs from pinned snapshot ({p})')


def resolve(ref, snapshot, mapping, by_locator, live_verified=False,
            candidates=None, db_row=None):
    loc = ref.removeprefix('chunk:')
    if loc == 'vbt' and ref == 'vbt':
        return {'kind': 'work', 'work': 'vbt', 'record': mapping['works']['vbt'],
                'note': 'work-level reference; no passage is identified',
                'witness_status': 'UNPINNED'}
    if ':' in loc or loc not in by_locator:
        raise ValueError(f'unknown passage locator {ref!r}')
    work, passage = by_locator[loc]
    out = {'kind': 'passage', 'locator': loc, 'immutable_id': passage['immutable_id'],
            'verses': passage.get('verses'), 'work': work,
            'record': mapping['works'][work], 'witness_status': 'UNPINNED',
            'ledger': {'path': snapshot['works'][work]['ledger'],
                       'sha256': snapshot['works'][work]['sha256'],
                       'translation_work_revision': snapshot['revision'],
                       'status': 'BYTES_MATCH_SNAPSHOT' if live_verified else 'SNAPSHOT_ONLY'},
            'limitations': ['ledger membership is not a verified witness, edition or reading',
                            'work mappings are candidate links, not authority']}
    # Advisory only: candidate manuscript/edition pointers for this work's
    # key. They NEVER change witness_status (hard-enforced UNPINNED above
    # and in inventory()); promotion needs a verified record, not a pointer.
    ours = mapping['works'][work].get('openpatala_work_key', '')
    hits = [c for c in (candidates or {}).get('candidates', [])
            if c.get('work_key') == ours]
    if hits:
        out['witness_candidates'] = hits
        out['limitations'].append('listed candidates are pointers with provenance, not pins')
    # Backbone row (O5): DB-backed identity when --db supplied. The snapshot
    # ledger check stays authoritative for BYTES; the DB answers IDENTITY
    # (which work/edition/etext holds this chunk). Witnesses stay UNPINNED:
    # the witnesses table is empty box-wide (R2 audit 2026-11-06).
    if db_row is not None:
        out['backbone'] = db_row
        out['limitations'].append('backbone identity: box DB (populated from repos, not a witness)')
    return out


def db_lookup(dsn, locator):
    """Resolve one chunk locator against the box openpatala DB. Returns a
    backbone dict or raises ValueError. Read-only (SELECT only)."""
    import psycopg2
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute("SELECT id, work_id, citation_value FROM passages WHERE citation_value = %s",
                (locator,))
    rows = cur.fetchall()
    if not rows:
        con.close()
        raise ValueError(f'unknown passage locator {locator!r} (not in box DB)')
    pid, wid, _ = rows[0]
    cur.execute("SELECT id, preferred_title FROM works WHERE id = %s", (wid,))
    w = cur.fetchone()
    cur.execute("SELECT id, title, external_ids FROM editions WHERE work_id = %s", (wid,))
    eds = cur.fetchall()
    cur.execute("SELECT id, provider_id, artifact_id, text_format FROM etexts WHERE work_id = %s",
                (wid,))
    ets = cur.fetchall()
    con.close()
    return {"passage_id": pid, "work": {"id": wid, "title": w[1] if w else None},
            "editions": [{"id": e[0], "title": e[1], "external_ids": e[2]} for e in eds],
            "etexts": [{"id": e[0], "provider": e[1], "artifact": e[2], "format": e[3]}
                       for e in ets],
            "witnesses": [],
            "witness_status": "UNPINNED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ref', nargs='?', help='exact chunk locator, e.g. chunk:tsa08-p03')
    parser.add_argument('--tw', type=Path, help='translation-work checkout to hash-check')
    parser.add_argument('--db', nargs='?', const='postgresql://patala:patala@localhost:5432/openpatala',
                        default=None,
                        help='box openpatala DSN for backbone identity '
                             '(bare --db uses the box default)')
    parser.add_argument('--check', action='store_true', help='check snapshot and evidence references')
    args = parser.parse_args()
    try:
        snapshot, mapping, evidence = map(read_json, (SNAPSHOT_PATH, MAP_PATH, EVIDENCE_PATH))
        try:
            candidates = read_json(CANDIDATES_PATH)
        except OSError:
            candidates = {"candidates": []}
        by_locator = inventory(snapshot, mapping, evidence)
        if args.tw is not None:
            verify_ledgers(args.tw, snapshot)
        if args.check:
            source_status = 'ledger bytes match pinned snapshot' if args.tw is not None else 'snapshot only; live ledger bytes not checked'
            print(f"{len(snapshot['works'])} works, {len(by_locator)} passage IDs; {source_status}; witnesses UNPINNED")
        elif args.ref:
            db_row = None
            if args.db is not None:
                loc = args.ref.removeprefix('chunk:')
                try:
                    db_row = db_lookup(args.db, loc)
                except ValueError as exc:
                    print(f'ERROR: {exc}', file=sys.stderr)
                    return 1
                except Exception as exc:  # DB down / driver missing: fail closed
                    print(f'ERROR: backbone unavailable ({type(exc).__name__}: {exc})',
                          file=sys.stderr)
                    return 1
            print(json.dumps(resolve(args.ref, snapshot, mapping, by_locator, args.tw is not None, candidates, db_row), ensure_ascii=False, indent=2))
        else:
            parser.error('give a passage locator or --check')
    except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
