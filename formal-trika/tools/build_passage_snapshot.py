#!/usr/bin/env python3
"""Snapshot passage identifiers and ledger hashes, never passage text.

Run with --tw /path/to/translation-work --output FILE. The input ledgers
must be tracked and unchanged at the recorded commit. This is a locator
inventory, not verification of the edition, interpretation, or witness.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def git(tw, *args):
    r = subprocess.run(['git', '-C', str(tw), *args], capture_output=True, text=True)
    if r.returncode:
        raise ValueError('translation-work must be an accessible Git checkout: ' + r.stderr.strip())
    return r.stdout.strip()


def build(tw):
    specs = json.loads((ROOT / 'EVIDENCE.json').read_text(encoding='utf-8'))['works']
    revision = git(tw, 'rev-parse', '--verify', 'HEAD^{commit}')
    manifest_rev, manifest_at = None, None
    try:
        man = json.loads((tw / 'MANIFEST.json').read_bytes().decode('utf-8'))
        manifest_rev, manifest_at = man.get('rev'), man.get('at')
    except (OSError, ValueError, AttributeError):
        pass
    works = {}
    seen_locators, seen_ids = set(), set()
    for work, spec in sorted(specs.items()):
        ledger = spec['ledger']
        prefix = 'translation-work/'
        if not ledger.startswith(prefix):
            raise ValueError(f'invalid ledger path: {ledger}')
        relative = ledger[len(prefix):]
        if Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise ValueError(f'unsafe ledger path: {relative}')
        git(tw, 'ls-files', '--error-unmatch', '--', relative)
        if git(tw, 'status', '--porcelain', '--', relative):
            raise ValueError(f'ledger differs from commit: {relative}')
        data = (tw / relative).read_bytes()
        rows = []
        for line_no, line in enumerate(data.decode('utf-8').splitlines(), 1):
            if not line.strip():
                continue
            item = json.loads(line)
            loc, pid = item.get('locator'), item.get('immutable_id')
            if not isinstance(loc, str) or not isinstance(pid, str) or not loc or not pid:
                raise ValueError(f'{relative}:{line_no}: missing passage locator or id')
            if loc in seen_locators or pid in seen_ids:
                raise ValueError(f'{relative}:{line_no}: duplicate locator or id')
            seen_locators.add(loc)
            seen_ids.add(pid)
            rows.append({'locator': loc, 'immutable_id': pid, 'verses': item.get('verses')})
        if not rows:
            raise ValueError(f'empty passage ledger: {relative}')
        works[work] = {'ledger': relative, 'sha256': hashlib.sha256(data).hexdigest(),
                       'passages': rows}
    return {'format': 'trika-passage-snapshot/1',
            'repository': 'https://github.com/prx0r/translation-work',
            'revision': revision,
            'manifest_rev': manifest_rev, 'manifest_at': manifest_at,
            'works': works}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tw', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        doc = build(args.tw)
        args.output.write_text(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f'ERROR: {e}', file=sys.stderr)
        return 1
    print(f"Recorded {sum(len(w['passages']) for w in doc['works'].values())} passage IDs at {doc['revision']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
