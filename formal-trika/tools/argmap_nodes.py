#!/usr/bin/env python3
"""Index argmap units with conservative, work-scoped passage locators.

Explicit chunk IDs must belong to the unit's own work. Chapter-qualified
ranges retain their chapter; ambiguous, reversed, foreign or conflicting
references stay UNKNOWN. Locator matching is a candidate join, not a check
that the Sanskrit or interpretation is correct.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def parse_span(value):
    """Return (kind, chapter_start, verse_start, chapter_end, verse_end)."""
    s = str(value or '').strip()
    m = re.fullmatch(r'stotra\s+(\d+)\s*-\s*(\d+)', s, re.IGNORECASE)
    if m:
        a, b = map(int, m.groups())
        return ('stotra', None, a, None, b) if a <= b else None
    m = re.fullmatch(r'(?:(\d+)\.)?(\d+)(?:\s*-\s*(?:(\d+)\.)?(\d+))?', s)
    if not m:
        return None
    c1, v1, c2, v2 = m.groups()
    c1, v1 = (int(c1) if c1 else None), int(v1)
    if v2 is None:
        return ('verse', c1, v1, c1, v1)
    c2, v2 = (int(c2) if c2 else c1), int(v2)
    if c1 is None and c2 is not None:
        return None
    if (c1 is None and v1 > v2) or (c1 is not None and (c1, v1) > (c2, v2)):
        return None
    return ('verse', c1, v1, c2, v2)


def parse_range(value):
    """Compatibility view for simple same-chapter ranges."""
    span = parse_span(value)
    if span is None or span[1] != span[3]:
        return None
    return (span[0], (span[2], span[4]))


def parse_stotra_song(song):
    m = re.fullmatch(r'[sS](\d+)', str(song or ''))
    return int(m.group(1)) if m else None


def verse_coordinate(unit):
    value = unit.get('verse', unit.get('verse_num'))
    # Decimal coordinates stored as floats lose trailing digits (1.10 -> 1.1).
    if isinstance(value, (bool, float)) or value is None:
        return None
    m = re.fullmatch(r'(?:(\d+)\.)?(\d+)', str(value).strip())
    if not m:
        return None
    chapter, verse = m.groups()
    if chapter is None:
        hint = unit.get('chapter', unit.get('ahnika'))
        if not isinstance(hint, bool) and str(hint or '').isdigit():
            chapter = hint
    return (int(chapter) if chapter else None, int(verse))


def contains(span, coord):
    """Return True/False when decidable, otherwise None."""
    kind, c1, v1, c2, v2 = span
    chapter, verse = coord
    if kind != 'verse':
        return None
    if c1 is None:
        return v1 <= verse <= v2
    if chapter is not None:
        return (c1, v1) <= (chapter, verse) <= (c2, v2)
    if c1 == c2:
        return v1 <= verse <= v2
    return None


def resolve_unit(work, unit, spans, locsets, owners):
    local = locsets.get(work, set())
    song, vid = str(unit.get('song') or ''), str(unit.get('verse_id') or '')
    explicit = {loc for loc in local if song == loc or vid == loc or
                vid.startswith(loc + '-') or vid.startswith(loc + '_')}
    if len(explicit) > 1:
        return 'UNKNOWN', 'AMBIGUOUS_LOCATOR', sorted(explicit), []
    coord = verse_coordinate(unit)
    if explicit:
        loc = next(iter(explicit))
        span = spans[work].get(loc)
        matches = contains(span, coord) if span and coord else None
        if matches is False:
            return 'UNKNOWN', 'LOCATOR_RANGE_CONFLICT', [loc], []
        return loc, 'EXACT_LOCATOR' if matches is True else 'LOCATOR_ONLY', [loc], []

    # A chunk-like ID from another work cannot be rescued by a matching number.
    hints = [song]
    m = re.match(r'^([A-Za-z0-9_]+-p\d+)(?:[-_].*)?$', vid)
    if m:
        hints.append(m.group(1))
    for hint in hints:
        if not re.fullmatch(r'[A-Za-z0-9_]+-p\d+', hint):
            continue
        other = sorted(owners.get(hint, set()) - {work})
        if other:
            return 'UNKNOWN', 'FOREIGN_LOCATOR', [hint], other
        if hint not in local:
            return 'UNKNOWN', 'UNKNOWN_LOCATOR', [hint], []

    stotra = parse_stotra_song(song)
    if stotra is not None:
        matches = [loc for loc, span in spans.get(work, {}).items() if span and
                   span[0] == 'stotra' and span[2] <= stotra <= span[4]]
        if len(matches) == 1:
            return matches[0], 'STOTRA_RANGE', matches, []
        if len(matches) > 1:
            return 'UNKNOWN', 'AMBIGUOUS_RANGE', sorted(matches), []

    if coord is None:
        return 'UNKNOWN', 'NO_COORDINATE', [], []
    chapters = {c for span in spans.get(work, {}).values() if span and span[0] == 'verse'
                for c in (span[1], span[3]) if c is not None}
    matches = []
    for loc, span in spans.get(work, {}).items():
        if not span or span[0] != 'verse':
            continue
        # An unqualified number cannot choose among multiple chapters.
        if coord[0] is None and span[1] is not None and len(chapters) > 1:
            continue
        if contains(span, coord) is True:
            matches.append(loc)
    if len(matches) == 1:
        return matches[0], 'NUMBER_RANGE', matches, []
    if len(matches) > 1:
        return 'UNKNOWN', 'AMBIGUOUS_RANGE', sorted(matches), []
    return 'UNKNOWN', 'NO_UNAMBIGUOUS_RANGE', [], []


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tw', type=Path, default=Path('/root/translation-work'))
    ap.add_argument('--out', type=Path, default=HERE / 'data' / 'argmap-nodes.jsonl')
    a = ap.parse_args()
    ledgers = sorted(a.tw.glob('*/passages.jsonl'))
    if not ledgers:
        raise ValueError(f'no passage ledgers under {a.tw}')
    git = subprocess.run(['git', '-C', str(a.tw), 'rev-parse', 'HEAD'],
                         text=True, capture_output=True)
    revision = git.stdout.strip() if git.returncode == 0 else None
    status = subprocess.run(['git', '-C', str(a.tw), 'status', '--porcelain', '--untracked-files=all'],
                            text=True, capture_output=True) if revision else None
    checkout = ('CLEAN' if status and status.returncode == 0 and not status.stdout else
                'DIRTY' if status and status.returncode == 0 else 'UNVERIFIED')
    spans, locsets, owners, ledger_hashes = {}, {}, {}, {}
    for ledger in ledgers:
        wd = ledger.parent.name
        spans[wd], locsets[wd] = {}, set()
        data = ledger.read_bytes()
        ledger_hashes[wd] = hashlib.sha256(data).hexdigest()
        for line in data.decode('utf-8').splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            loc = row.get('locator')
            if not isinstance(loc, str) or not loc or loc in locsets[wd]:
                raise ValueError(f'missing or duplicate locator in {ledger}')
            locsets[wd].add(loc)
            spans[wd][loc] = parse_span(row.get('verses'))
            owners.setdefault(loc, set()).add(wd)
    nodes, files = [], 0
    for fp in sorted(a.tw.glob('*/data/*.argmap.json')):
        workdir = fp.parts[-3]
        data = fp.read_bytes()
        source_hash = hashlib.sha256(data).hexdigest()
        d = json.loads(data.decode('utf-8'))
        if isinstance(d, list):
            units = d
        elif isinstance(d, dict) and ('units' in d or 'argmaps' in d):
            units = d.get('units', d.get('argmaps'))
        else:
            raise ValueError(f'unrecognized argmap layout in {fp}')
        if not isinstance(units, list):
            raise ValueError(f'argmap units must be a list in {fp}')
        if not units:
            continue
        files += 1
        for u in units:
            if not isinstance(u, dict):
                raise ValueError(f'non-object argmap unit in {fp}')
            loc, status, candidates, foreign = resolve_unit(workdir, u, spans, locsets, owners)
            nodes.append({'work': workdir, 'locator': loc, 'locator_status': status,
                          'locator_candidates': candidates, 'cross_work': None,
                          'foreign_work_candidates': foreign,
                          'source_file': str(fp.relative_to(a.tw)),
                          'source_file_sha256': source_hash,
                          'ledger_sha256': ledger_hashes.get(workdir),
                          'translation_work_revision': revision,
                          'source_checkout_state': checkout,
                          'verse_id': u.get('verse_id'), 'verse': u.get('verse'),
                          'speaker': u.get('speaker'), 'question': u.get('question'),
                          'premises': u.get('premises', []), 'inference': u.get('inference'),
                          'uncertainties': u.get('uncertainties', []),
                          'sanskrit_sha': u.get('sanskrit_sha')})
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open('w', encoding='utf-8') as fh:
        for node in nodes:
            fh.write(json.dumps(node, ensure_ascii=False) + '\n')
    unknown = sum(n['locator'] == 'UNKNOWN' for n in nodes)
    print(f'files: {files}; nodes: {len(nodes)}; unknown-locator: {unknown} -> {a.out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
