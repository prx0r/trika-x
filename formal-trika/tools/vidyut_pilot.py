#!/usr/bin/env python3
"""vidyut_pilot.py — machine morphology beside L0 (L0-as-terms pilot support).

Runs Vidyut cheda (segmentation + morphological analysis) over a volume
span's bytes and emits a comparison receipt against the gold L0 token rows
for the same verse. The machine proposes analyses; the grammarian (human)
disposes. Never overwrites L0; never promotes AMBIGUOUS; never judges forks.

  VIDYUT_VENV=/root/.venvs/vidyut VIDYUT_DATA=/tmp/vidyut-data \\
    python3 tools/vidyut_pilot.py --work tantrasara-a08 --verse tsa-a08-v71 \\
      --src /root/ipvv/site/data/sanskrit/tantrasara.txt

Receipt: data/vidyut-<verse>.json {tokens, l0_compare, verdict}.
Requires the vidyut venv + data (see EXTERNAL-SURVEY-2026-11-06 §4).
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
VENV = Path(os.environ.get("VIDYUT_VENV", "/root/.venvs/vidyut"))
VDATA = os.environ.get("VIDYUT_DATA", "/tmp/vidyut-data")
PY = VENV / "bin" / "python"


CHE_DA = r"""
import json, re, sys
from vidyut.vidyut import cheda, lipi
man_path, verse, src_path, data_dir, surfaces_json = sys.argv[1:6]
man = json.load(open(man_path, encoding="utf-8"))
spans = {s["passage_id"]: s for s in man["spans"]}
s = spans[verse]
raw = open(src_path, "rb").read()
seg = raw[s["start"]:s["end"]].decode("utf-8")
norm_lines = []
for ln in seg.splitlines():
    ln = re.sub(r"//.*$", " ", ln)          # trailing editorial markers are not text
    ln = re.sub(r"\[[^\]]*\]", " ", ln)     # bracketed markers are not text
    norm_lines.append(ln)
norm = " ".join(norm_lines)
# allow-list IAST letters + space: everything else (digits, _, punctuation,
# avagraha, danda) is editorial/orthographic noise for the analyzer
norm = re.sub(r"[^a-zA-Zāīūṛṝḷḹēōṃḥṅñṭḍṇśṣ ]", " ", norm)
norm = re.sub(r"\s+", " ", norm)
slp = lipi.transliterate(norm, lipi.Scheme.Iast, lipi.Scheme.Slp1)
c = cheda.Chedaka(data_dir)
out = []
for t in c.run(slp):
    blob = t.data if isinstance(t.data, str) else json.dumps(t.data, default=str)
    feats = {"text": t.text, "lemma": t.lemma}
    m = re.search(r"PadaEntry\.(\w+)", blob)
    if m:
        feats["kind"] = m.group(1)
    for attr in ("linga", "vibhakti", "vacana", "lakara", "gana"):
        m = re.search(attr + r"[=:](\w+)", blob.replace(" ", ""))
        if m:
            feats[attr] = m.group(1).split(".")[-1]
    m = re.search(r"aupadeshika='([^']+)'", blob)
    if m:
        feats["dhatu"] = m.group(1)
    out.append(feats)
surfaces = json.loads(surfaces_json)
cmps = []
for surf in surfaces:
    norm = lipi.transliterate(surf.replace("-", "").replace(" ", "").replace("'", ""),
                              lipi.Scheme.Iast, lipi.Scheme.Slp1).lower()
    hit = []
    for t in out:
        for field in (t["text"].lower(), t["lemma"].lower()):
            # boundary-anchored matching only: exact or shared prefix
            # (infix containment matches endings, not words — F-noise)
            if norm and field and (norm == field or (len(norm) >= 3 and len(field) >= 3
                                   and (norm.startswith(field) or field.startswith(norm)))):
                hit.append(t["lemma"])
                break
    cmps.append({"surface": surf, "slp1": norm,
                 "hit": bool(hit),
                 "hit_lemmas": sorted(set(hit))})
print(json.dumps({"span_text": seg, "tokens": out, "surface_match": cmps}, ensure_ascii=False))
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", required=True)
    ap.add_argument("--verse", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--tw", default="/root/translation-work")
    a = ap.parse_args()
    mans = sorted(Path(a.tw, a.work, "source", "volumes").glob("*.json"))
    if not mans:
        print(f"ERROR: no volume manifest for {a.work}")
        return 1
    cands = sorted(Path(a.tw, a.work, "data").glob("*.l0.json"))
    l0 = []
    for cf in cands:
        try:
            rows = json.loads(cf.read_text(encoding="utf-8"))
        except ValueError:
            continue
        l0.extend([x for x in (rows if isinstance(rows, list) else rows.get("units", []))
                   if x.get("verse_id") == a.verse])
    if not l0:
        print(f"ERROR: no L0 rows for verse {a.verse}")
        return 1
    surfaces = json.dumps([r.get("surface") or "" for r in l0], ensure_ascii=False)
    r = subprocess.run([str(PY), "-c", CHE_DA, str(mans[0]), a.verse, a.src, VDATA, surfaces],
                       capture_output=True, text=True, timeout=300)
    if r.returncode:
        print(f"ERROR: cheda failed: {r.stderr.strip()[:300]}")
        return 1
    got = json.loads(r.stdout)
    vtTexts = [t["text"] for t in got["tokens"]]
    compared, matched = [], 0
    for row, cm in zip(l0, got.get("surface_match", [])):
        hit = cm.get("hit", False)
        matched += bool(hit)
        compared.append({"l0_surface": row.get("surface"), "l0_morph": row.get("morph"),
                         "l0_status": row.get("status"), "fork": row.get("fork"),
                         "vidyut_hit": hit, "vidyut_lemmas": cm.get("hit_lemmas", [])})
    verdict = (f"{matched}/{len(compared)} L0 surfaces align with machine tokens; "
               + ("forks present — grammarian review owed" if any(c["fork"] not in (None, "none") for c in compared)
                  else "no live forks in verse"))
    doc = {"format": "trika-vidyut-pilot/1", "work": a.work, "verse": a.verse,
           "span_text": got.get("span_text", ""),
           "analysis_normalization": "editorial markers + verse numbers dropped, avagraha/bar/slash stripped from an analysis COPY; span bytes authoritative",
           "span_sha_note": "span bytes from volume manifest (see bind receipts)",
           "machine_tokens": got["tokens"], "l0_compare": compared, "verdict": verdict,
           "note": "machine proposes, grammarian disposes; never overwrites L0"}
    out = HERE / "data" / f"vidyut-{a.verse}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"{a.verse}: {verdict} -> {out.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
