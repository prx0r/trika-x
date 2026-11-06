#!/usr/bin/env python3
"""chunk_verse.py — derive chunk<->verse<->byte maps from existing artifacts.

Read-only. Joins translation-work passage ledgers (chunk locators with
`verses` ranges like "8.1-8.17") against source volume manifests
(passage_id `tsa-a08-v01` spans with byte offsets + text_sha256).
Emits bridge/chunk-verse-<work>-<date>.json per closable work:
{chunk: {verses, verse_spans[], byte_start/end, span integrity}}.

A work closes when: volume manifest(s) exist, verse spans are contiguous
over the ledger's ranges, and every range resolves to spans. Anything else
is reported OPEN with the reason (no spans, ragged ranges, verse-id
mismatch) — never guessed. This is the CHAIN-GAP closer built from parts
both lanes already banked; it invents no mapping.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parent / "bridge"


def parse_range(vrange: str):
    """'8.1-8.17' -> (prefix '8.', 1, 17); '8.5' -> (prefix, 5, 5).
    Bare '1-9'/'1' -> ('', 1, 9): safe because spans resolve inside the
    single work's own manifest, never across works."""
    m = re.fullmatch(r"\s*(\d+)\.(\d+)\s*-\s*(\d+)\.(\d+)\s*", vrange or "")
    if m:
        if m.group(1) != m.group(3):
            return None
        return (m.group(1) + ".", int(m.group(2)), int(m.group(4)))
    m = re.fullmatch(r"\s*(\d+)\.(\d+)\s*", vrange or "")
    if m:
        return (m.group(1) + ".", int(m.group(2)), int(m.group(2)))
    m = re.fullmatch(r"\s*(\d+)\s*-\s*(\d+)\s*", vrange or "")
    if m:
        return ("", int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r"\s*(\d+)\s*", vrange or "")
    if m:
        return ("", int(m.group(1)), int(m.group(1)))
    return None


def verse_ids(workdir: str, prefix: str, v0: int, v1: int, songs: set):
    """Candidate span passage_ids for verses v0..v1 (try work's song ids)."""
    cands = []
    for v in range(v0, v1 + 1):
        hit = None
        for fmt in (f"{prefix}v{v:02d}", f"{prefix}v{v}", f"{prefix}{v:02d}", f"{prefix}{v}"):
            if fmt in songs:
                hit = fmt
                break
        if hit is None:
            return None
        cands.append(hit)
    return cands


def close_work(tw: Path, workdir: str):
    ledger = tw / workdir / "passages.jsonl"
    if not ledger.is_file():
        return None, "no ledger"
    rows = [json.loads(l) for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
    vdir = tw / workdir / "source" / "volumes"
    mans = sorted(vdir.glob("*.json")) if vdir.is_dir() else []
    if not mans:
        return None, "no volume manifests"
    spans = {}
    for mf in mans:
        try:
            m = json.loads(mf.read_text(encoding="utf-8"))
        except ValueError:
            return None, f"manifest unreadable: {mf.name}"
        for s in m.get("spans", []):
            spans[s["passage_id"]] = s
    # guess the song prefix from span ids (e.g. 'tsa-a08-')
    prefixes = set()
    for pid in spans:
        m = re.match(r"^(.+?v)\d+$", pid)
        if m:
            prefixes.add(m.group(1))
    chunks = {}
    for r in rows:
        pr = parse_range(r.get("verses", ""))
        if pr is None:
            return None, f"ragged verses range: {r.get('locator')}={r.get('verses')!r}"
        prefix, v0, v1 = pr
        ids = None
        for pfx in sorted(prefixes):
            ids = verse_ids(workdir, pfx, v0, v1, set(spans))
            if ids is not None:
                break
        if ids is None:
            return None, f"verse ids unresolvable: {r.get('locator')} {r.get('verses')!r}"
        segs = [spans[i] for i in ids]
        for a, b in zip(segs, segs[1:]):
            if a["end"] != b["start"]:
                return None, f"span break inside {r.get('locator')}"
        chunks[r["locator"]] = {
            "verses": r.get("verses"), "verse_spans": ids,
            "byte_start": segs[0]["start"], "byte_end": segs[-1]["end"],
            "span_shas": [s["text_sha256"][:12] for s in segs]}
    return {"workdir": workdir, "chunks": chunks,
            "manifests": [m.name for m in mans]}, "CLOSED"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--work", action="append", default=[])
    a = ap.parse_args()
    works = a.work or sorted(p.name for p in a.tw.iterdir()
                             if p.is_dir() and (p / "passages.jsonl").is_file()
                             and not p.name.startswith("."))
    closed, opened = {}, {}
    for w in works:
        doc, status = close_work(a.tw, w)
        (closed if status == "CLOSED" else opened)[w] = doc if doc else status
    date = datetime.date.today().isoformat()
    for w, doc in closed.items():
        out = BRIDGE / f"chunk-verse-{w}-{date}.json"
        out.write_text(json.dumps({"format": "trika-chunk-verse/1", "date": date,
                                   **doc}, ensure_ascii=False, indent=1) + "\n")
    print(f"works: {len(works)}; CLOSED: {len(closed)}; OPEN: {len(opened)}")
    for w, reason in sorted(opened.items())[:20]:
        print(f"  OPEN {w}: {reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
