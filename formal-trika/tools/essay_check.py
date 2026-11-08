#!/usr/bin/env python3
"""essay_check.py — the essay gate (translation-work check.py discipline).

Validates a compiled essay triple (.md + .essay.json + .receipt.json):
schema keys, frozen-claim coverage (every tiered bullet links a claim AND
every claim is cited by a bullet), exact marker binding ([CLM-id] must name
a real claim), tier law (T claims bind an exact span to the current ledger
passage, its digest and edition label), chunk existence in the ledger,
receipt-vs-claim agreement,
no pre-review review claims. Exit 0 = READY_FOR_HUMAN_REVIEW — a human
gate, not approval and not publication; else named failures.

  python3 tools/essay_check.py --slug expansion-mala-full-2026-11-06-145904319815
  python3 tools/essay_check.py --all
"""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
TW = Path(os.environ.get("TRANSLATION_WORK", "/root/translation-work"))
TIERS = {"T", "R", "E", "C", "H", "X"}


def check_slug(swarm: Path, slug: str) -> list:
    fails = []
    md = swarm / f"{slug}.md"
    ejp = swarm / f"{slug}.essay.json"
    rcp = swarm / f"{slug}.receipt.json"
    for p, what in ((md, "draft"), (ejp, "essay.json"), (rcp, "receipt")):
        if not p.is_file():
            fails.append(f"missing {what}: {p.name}")
    if fails:
        return fails
    try:
        ej = json.loads(ejp.read_text(encoding="utf-8"))
        rc = json.loads(rcp.read_text(encoding="utf-8"))
        text = md.read_text(encoding="utf-8")
    except ValueError as e:
        return [f"invalid JSON: {e}"]
    for k in ("id", "title", "date", "chunk", "verses", "voice", "claims",
              "theorems", "tracks", "openpatala", "status"):
        if k not in ej:
            fails.append(f"essay.json missing key: {k}")
    fids = {c.get("id") for c in ej.get("claims", [])}
    by_id = {c.get("id"): c for c in ej.get("claims", [])}
    if len(fids) != len(ej.get("claims", [])):
        fails.append("duplicate essay claim ids")
    for c in ej.get("claims", []):
        if c.get("tier") not in TIERS:
            fails.append(f"claim {c.get('id')} bad tier: {c.get('tier')}")
        if not c.get("text", "").strip():
            fails.append(f"claim {c.get('id')} empty text")
        if c.get("tier") == "T":
            # A self-hash alone does not establish that this text is a source.
            span = c.get("span", "")
            digest = c.get("span_sha256", "")
            if not isinstance(span, str) or not span or not isinstance(digest, str) or not digest:
                fails.append(f"claim {c.get('id')} T-tier without "
                             "span+span_sha256")
            elif hashlib.sha256(span.encode()).hexdigest() != digest:
                fails.append(f"claim {c.get('id')} span digest mismatch")
            if not (ej.get("openpatala", {}) or {}).get("edition_label"):
                fails.append(f"claim {c.get('id')} T-tier without "
                             "edition label")
            if not c.get("source_sha256") or not c.get("source_edition"):
                fails.append(f"claim {c.get('id')} T-tier without "
                             "source_sha256+source_edition")
            if c.get("source_binding_version") != 2:
                fails.append(f"claim {c.get('id')} T-tier requires source_binding_version 2")
    markers = set(re.findall(r"\[CLM-[A-Za-z0-9_-]+\]", text))
    for m in sorted(markers):
        mid = m.strip("[]")
        if mid not in fids:
            fails.append(f"marker names no claim: {m}")
    for cid in sorted(fids):
        if f"[{cid}]" not in text:
            fails.append(f"claim {cid} never cited in draft")
    for line in text.splitlines():
        if line.startswith("- ") and ("(R)" in line or "(T)" in line):
            if "[CLM-" not in line and "::" not in line:
                fails.append(f"untraced bullet: {line[:80]}")
                break
    if "[CLM-" not in text and fids:
        fails.append("draft carries no frozen-claim markers")
    for t in ej.get("theorems", []):
        if t.get("tier") != "UNVERIFIED":
            fails.append(f"theorem {t.get('name')} tier must be UNVERIFIED, got {t.get('tier')}")
    if not ej.get("tracks"):
        fails.append("no research tracks assigned")
    op = ej.get("openpatala", {})
    if "openpatala_work_id" not in op or "mapping_status" not in op:
        fails.append("openpatala block incomplete")
    tn = ej.get("tension")
    if tn is not None:
        if not isinstance(tn, dict) or not tn.get("id", "").startswith("tension:"):
            fails.append(f"bad tension block: {tn}")
        elif tn.get("relation") not in ("resolves", "loosens"):
            fails.append(f"bad tension relation: {tn.get('relation')}")
        else:
            try:
                import sys as _sys
                _sys.path.insert(0, os.environ.get("SVREAD_TOOLS",
                                                   "/root/svread/tools"))
                import lingua as _lingua
                row = _lingua.resolve(tn["id"])
                if row.get("visibility", "private") == "private":
                    fails.append(f"tension-private: {tn['id']}")
            except Exception as e:
                fails.append(f"tension unresolvable: {tn['id']} ({str(e)[:80]})")
    if rc.get("essay") != slug:
        fails.append("receipt essay mismatch")
    # PR #7: receipt must agree with the essay on claims AND theorems —
    # a matching slug alone proves nothing.
    rclaims = {c.get("id"): c.get("text") for c in rc.get("frozen_claims", [])}
    eclaims = {c.get("id"): c.get("text") for c in ej.get("claims", [])}
    if len(rclaims) != len(rc.get("frozen_claims", [])):
        fails.append("duplicate receipt claim ids")
    if set(rclaims) != set(eclaims):
        fails.append("receipt frozen-claim ids differ from essay claims: "
                     f"only-receipt={sorted(set(rclaims) - set(eclaims))[:3]} "
                     f"only-essay={sorted(set(eclaims) - set(rclaims))[:3]}")
    else:
        for cid, rtext in rclaims.items():
            if rtext != eclaims[cid]:
                fails.append(f"receipt claim text changed: {cid}")
                break
    # T-tier evidence is part of the frozen claim, not mutable metadata.
    receipt_by_id = {c.get("id"): c for c in rc.get("frozen_claims", [])}
    for c in ej.get("claims", []):
        if c.get("tier") == "T" or receipt_by_id.get(c.get("id"), {}).get("tier") == "T":
            receipt = receipt_by_id.get(c.get("id"), {})
            for field in ("tier", "span", "span_sha256", "source_sha256", "source_edition", "source_binding_version"):
                if field not in c or c.get(field) != receipt.get(field):
                    fails.append(f"receipt claim {c.get('id')} {field} differs")
    def _tname(t):
        return t.get("name") if isinstance(t, dict) else t
    rthms = sorted(_tname(t) for t in rc.get("theorems", []))
    ethms = sorted(_tname(t) for t in ej.get("theorems", []))
    if rthms != ethms:
        fails.append("receipt theorems differ from essay theorems")
    # Chunk must exist in the ledger (read-only; kills nonexistent chunks).
    work, _, target = (ej.get("chunk", "") or "").partition(":")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", work) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", target):
        fails.append("essay chunk unparsable")
    else:
        led = TW / work / "passages.jsonl"
        try:
            rows = [json.loads(l) for l in led.read_text(encoding="utf-8").splitlines() if l.strip()]
            matches = [row for row in rows if isinstance(row, dict) and row.get("locator") == target]
            if not matches:
                fails.append(f"chunk {target} absent from {work} ledger")
            elif len(matches) != 1:
                fails.append(f"chunk {target} duplicated in {work} ledger")
            else:
                row = matches[0]
                source = row.get("sanskrit")
                edition = row.get("source_edition")
                for c in ej.get("claims", []):
                    if c.get("tier") != "T":
                        continue
                    cid = c.get("id")
                    if not isinstance(source, str) or not source:
                        fails.append(f"claim {cid} source passage unavailable")
                        continue
                    if not isinstance(c.get("span"), str) or not c.get("span") or c["span"] not in source:
                        fails.append(f"claim {cid} span absent from source passage")
                    if c.get("source_sha256") != hashlib.sha256(source.encode("utf-8")).hexdigest():
                        fails.append(f"claim {cid} source passage digest mismatch")
                    if not isinstance(edition, str) or not edition or c.get("source_edition") != edition:
                        fails.append(f"claim {cid} source edition mismatch")
        except (OSError, UnicodeError, ValueError, TypeError):
            fails.append(f"ledger unreadable for work {work}")
    if ej.get("status") != "MACHINE-COMPILED":
        fails.append(f"bad status: {ej.get('status')}")
    # Pre-review drafts must not carry review claims; anything else needs
    # an explicit reviewer decision bound to this revision.
    if ej.get("status") == "MACHINE-COMPILED":
        for k in ("review", "signoff", "approved", "published"):
            if ej.get(k):
                fails.append(f"pre-review draft carries {k}")
    else:
        rev = ej.get("review")
        if not isinstance(rev, dict) or not rev.get("reviewer") \
                or not rev.get("decision") or not rev.get("revision"):
            fails.append("non-draft status without reviewer+decision+revision")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--swarm", type=Path, default=HERE / "swarm")
    a = ap.parse_args()
    slugs = ([a.slug] if a.slug else
             sorted({p.name[:-len(".receipt.json")] for p in a.swarm.glob("expansion-*.receipt.json")}))
    bad = 0
    for slug in slugs:
        fails = check_slug(a.swarm, slug)
        if fails:
            bad += 1
            print(f"FAIL {slug}:")
            for f in fails[:8]:
                print(f"  - {f}")
        else:
            print(f"PASS {slug}")
    print(f"{len(slugs) - bad}/{len(slugs)} essays READY_FOR_HUMAN_REVIEW "
          "(human gate — not approval, not publication)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
