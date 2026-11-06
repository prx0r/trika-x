#!/usr/bin/env python3
"""argmap_nodes.py — B3: argmap units → machine nodes index.

Consumes translation-work data/*.argmap.json (read-only) + passages.jsonl
verse ranges; emits formal-trika/data/argmap-nodes.jsonl, one node per
unit: work, locator (chunk), verse_id, speaker, question, premises,
inference, uncertainties (crux candidates), sanskrit_sha. Units whose
verse falls in no chunk range are emitted with locator UNKNOWN (never
dropped silently). Deterministic; rerun any time.
Usage: python3 formal-trika/tools/argmap_nodes.py [--tw PATH] [--out PATH]
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def parse_range(s):
    m = re.fullmatch(r"\s*(?:(\d+)\.)?(\d+)\s*-\s*(?:(\d+)\.)?(\d+)\s*", s or "")
    if m:
        a, b = int(m.group(2)), int(m.group(4))
        return ("verse", (a, b) if a <= b else (b, a))
    m = re.fullmatch(r"\s*stotra\s+(\d+)\s*-\s*(\d+)\s*", s or "", re.IGNORECASE)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return ("stotra", (a, b) if a <= b else (b, a))
    m = re.fullmatch(r"\s*(?:(\d+)\.)?(\d+)\s*", s or "")
    if m:
        return ("verse", (int(m.group(2)), int(m.group(2))))
    return None


def parse_stotra_song(song):
    m = re.fullmatch(r"[sS](\d+)", str(song or ""))
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--out", type=Path, default=HERE / "data" / "argmap-nodes.jsonl")
    a = ap.parse_args()
    # chunk ranges per work dir: [(locator, kind, lo, hi)] + locator set
    ranges = {}
    locsets = {}
    song_index = {}  # song string -> (workdir, locator): units often name their chunk
    for ledger in sorted(a.tw.glob("*/passages.jsonl")):
        wd = ledger.parent.name
        rs = []
        for line in ledger.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            pr = parse_range(r.get("verses", ""))
            loc = r.get("locator", "?")
            song_index.setdefault(loc, (wd, loc))
            if pr:
                kind, (lo, hi) = pr
                rs.append((loc, kind, lo, hi))
        ranges[wd] = rs
        locsets[wd] = {loc for loc, _, _, _ in rs} | {l for l in song_index if song_index[l][0] == wd}
    nodes, unknown, files = [], 0, 0
    for fp in sorted(a.tw.glob("*/data/*.argmap.json")):
        workdir = fp.parts[-3]
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        units = d if isinstance(d, list) else d.get("units", d.get("argmaps", []))
        if not units:
            continue
        files += 1
        for u in units:
            if not isinstance(u, dict):
                continue
            loc, v = "UNKNOWN", u.get("verse")
            cross = None
            try:
                v = int(v)
            except (TypeError, ValueError):
                v = None
            if v is not None:
                for l, kind, lo, hi in ranges.get(workdir, []):
                    if kind == "verse" and lo <= v <= hi:
                        loc = l
                        break
            stotra_n = parse_stotra_song(u.get("song"))
            if loc == "UNKNOWN" and stotra_n is not None:
                for l, kind, lo, hi in ranges.get(workdir, []):
                    if kind == "stotra" and lo <= stotra_n <= hi:
                        loc = l
                        break
            if loc == "UNKNOWN":
                # units often name their chunk in song/verse_id
                for key in (u.get("song"), (u.get("verse_id") or "").split("-v")[0]):
                    if key and key in song_index:
                        w2, l2 = song_index[key]
                        loc = l2
                        cross = w2 if w2 != workdir else None
                        break
            if loc == "UNKNOWN":
                # passage-level units: verse_id itself names the chunk
                vid = str(u.get("verse_id", ""))
                for l in locsets.get(workdir, ()):
                    if vid == l or vid.startswith(l + "-") or vid.startswith(l + "_"):
                        loc = l
                        break
            if loc == "UNKNOWN":
                unknown += 1
            nodes.append({"work": workdir, "locator": loc,
                          "cross_work": cross,
                          "verse_id": u.get("verse_id"), "verse": u.get("verse"),
                          "speaker": u.get("speaker"), "question": u.get("question"),
                          "premises": u.get("premises", []),
                          "inference": u.get("inference"),
                          "uncertainties": u.get("uncertainties", []),
                          "sanskrit_sha": u.get("sanskrit_sha")})
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        for n in nodes:
            fh.write(json.dumps(n, ensure_ascii=False) + "\n")
    nun = sum(1 for n in nodes if n["uncertainties"])
    print(f"files: {files}; nodes: {len(nodes)}; unknown-locator: {unknown}; "
          f"units-with-uncertainties: {nun} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
