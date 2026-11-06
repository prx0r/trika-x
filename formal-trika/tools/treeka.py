#!/usr/bin/env python3
"""treeka.py — B5: read-only assembler (works → passages → nodes → cruxes → essays).

Joins, never invents. Entries keyed work:locator (bare locators COLLIDE
across works: anu-* shared by anubhavanivedana/anuttarastika, par-*
shared by parapravesika/paramarthacarca — recorded in ambiguous).
  works:    svread/source-map.json (87 ledgers + bridge status)
  passages: translation-work/*/passages.jsonl (locator + verses)
  nodes:    formal-trika/data/argmap-nodes.jsonl (argued? = has premises)
  cruxes:   formal-trika/data/crux-queue.jsonl (cruxless? = no candidate)
  formal:   exact passage references in formal-trika/EVIDENCE.json
  essays:   translation-work/*/scholar/essays/*.json (essayless? per locator)
Output: formal-trika/data/treeka.json {works, gaps, ambiguous, counts}.
Gap report drives the crux queue (Phase 3.1): unargued passages,
cruxless arguments, essayless cruxes, chunks with no registry reference.

A registry reference is an unreviewed association, not a checked proof or
an assessment that the passage entails the model. Outputs cannot certify
that a passage is formalized.
Usage: python3 formal-trika/tools/treeka.py [--tw PATH] [--out PATH]
"""
import argparse
import glob
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def formal_references(evidence):
    """Resolve explicit theorem references to a unique (work, locator).

    `works[*].chunks` is an inventory, not a list of formalized passages.
    A missing or ambiguous inventory reference cannot be assigned to a work.
    """
    by_locator = {}
    for spec in evidence.get("works", {}).values():
        ledger = spec.get("ledger", "")
        prefix = "translation-work/"
        if not ledger.startswith(prefix):
            raise ValueError(f"invalid evidence ledger: {ledger!r}")
        parts = Path(ledger[len(prefix):]).parts
        if len(parts) != 2 or parts[1] != "passages.jsonl" or parts[0] in (".", ".."):
            raise ValueError(f"invalid evidence ledger: {ledger!r}")
        for loc in spec.get("chunks", []):
            by_locator.setdefault(loc, set()).add(parts[0])
    refs = {}
    for theorem, entry in evidence.get("entries", {}).items():
        for chunk in entry.get("chunks", []):
            loc = chunk.get("locator")
            if loc == "vbt":  # historical work-level reference
                continue
            owners = by_locator.get(loc, set())
            if len(owners) != 1:
                raise ValueError(f"unresolved or ambiguous evidence locator: {loc!r}")
            key = (next(iter(owners)), loc)
            refs.setdefault(key, set()).add(theorem)
    return {key: sorted(values) for key, values in refs.items()}


def verify_inputs(tw, smap, nodes):
    """Check the bytes behind every locator join, without claiming meaning."""
    ledger_hashes = {}
    for work, meta in smap.items():
        if Path(work).name != work or work in ('.', '..'):
            raise ValueError(f'invalid work directory: {work!r}')
        data = (tw / work / 'passages.jsonl').read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != meta.get('ledger_sha256'):
            raise ValueError(f'source-map ledger hash mismatch for {work}')
        ledger_hashes[work] = digest
    source_hashes = {}
    for node in nodes:
        work = node.get('work')
        if node.get('locator') == 'UNKNOWN' or work not in smap:
            continue
        path = Path(node.get('source_file') or '')
        if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != work:
            raise ValueError(f'invalid argmap source path for {work}')
        if path not in source_hashes:
            source_hashes[path] = hashlib.sha256((tw / path).read_bytes()).hexdigest()
        if (node.get('source_file_sha256') != source_hashes[path] or
                node.get('ledger_sha256') != ledger_hashes[work]):
            raise ValueError(f'stale argmap or ledger for {work}: {path}')


def verify_queue(nodes, queue, smap):
    def identity(item, text):
        return (item.get('work'), item.get('locator'), item.get('verse_id'),
                item.get('source_file'), item.get('source_file_sha256'),
                item.get('ledger_sha256'), text)
    expected = {identity(n, u.strip()) for n in nodes for u in n.get('uncertainties', []) or []
                if isinstance(u, str) and u.strip()}
    for item in queue:
        if (item.get('kind') != 'argmap-uncertainty' or item.get('locator') == 'UNKNOWN'
                or item.get('work') not in smap):
            continue
        if identity(item, item.get('text')) not in expected:
            raise ValueError('stale crux queue: no matching source node')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tw", type=Path, default=Path("/root/translation-work"))
    ap.add_argument("--sourcemap", type=Path, default=Path("/root/svread/source-map.json"))
    ap.add_argument("--nodes", type=Path, default=HERE / "data" / "argmap-nodes.jsonl")
    ap.add_argument("--queue", type=Path, default=HERE / "data" / "crux-queue.jsonl")
    ap.add_argument("--out", type=Path, default=HERE / "data" / "treeka.json")
    a = ap.parse_args()
    smap = json.loads(a.sourcemap.read_text(encoding="utf-8"))["works"]
    if not isinstance(smap, dict) or not smap:
        raise ValueError('source map has no works')
    nodes = load_jsonl(a.nodes)
    queue = load_jsonl(a.queue)
    ev = json.loads((HERE / "EVIDENCE.json").read_text(encoding="utf-8"))
    verify_inputs(a.tw, smap, nodes)
    verify_queue(nodes, queue, smap)
    formal_refs = formal_references(ev)
    nodes_by_key, crux_by_key = {}, {}
    for n in nodes:
        nodes_by_key.setdefault((n.get("work"), n.get("locator")), []).append(n)
    for q in queue:
        if q.get("kind") == "argmap-uncertainty" and q.get("locator"):
            crux_by_key.setdefault((q.get("work"), q.get("locator")), []).append(q)
    seen_work, ambiguous = {}, set()
    essays_by_loc = {}
    for f in glob.glob(str(a.tw / "*" / "scholar" / "essays" / "*.json")):
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        t = d.get("target") or d.get("entry", {}).get("target")
        if t:
            workdir = Path(f).relative_to(a.tw).parts[0]
            essays_by_loc.setdefault((workdir, t), []).append(Path(f).name)
    works, gaps = {}, {"unargued": [], "cruxless": [], "essayless": [], "no_formal_reference": []}
    for workdir, meta in sorted(smap.items()):
        for line in (a.tw / workdir / "passages.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            p = json.loads(line)
            loc = p.get("locator")
            if not loc:
                raise ValueError(f"missing locator in {workdir}/passages.jsonl")
            key = f"{workdir}:{loc}"
            if key in works:
                raise ValueError(f"duplicate passage {key}")
            if loc in seen_work and seen_work[loc] != workdir:
                ambiguous.add(loc)
            seen_work.setdefault(loc, workdir)
            ns = nodes_by_key.get((workdir, loc), [])
            argued = any(n.get("premises") for n in ns)
            refs = formal_refs.get((workdir, loc), [])
            source_keys = sorted({(n['source_file'], n['source_file_sha256'],
                                   n.get('translation_work_revision') or '',
                                   n.get('source_checkout_state') or 'UNVERIFIED')
                                  for n in ns})
            entry = {"work": workdir, "verses": p.get("verses"),
                     "argued": argued, "nodes": len(ns),
                     "ledger_sha256": meta['ledger_sha256'],
                     "argument_sources": [
                         {'path': path, 'sha256': sha, 'translation_work_revision': rev or None,
                          'checkout_state': state}
                         for path, sha, rev, state in source_keys],
                     "cruxes": len(crux_by_key.get((workdir, loc), [])),
                     "formalized": None,
                     "formal_reference": bool(refs), "formal_refs": refs,
                     "formal_status": "REGISTRY_REFERENCE_ONLY" if refs else "NO_REGISTRY_REFERENCE",
                     "essays": essays_by_loc.get((workdir, loc), []),
                     "bridge": meta.get("status", "?")}
            works[key] = entry
            if not argued:
                gaps["unargued"].append(key)
            elif not entry["cruxes"]:
                gaps["cruxless"].append(key)
            if not entry["essays"] and (argued or entry["cruxes"]):
                gaps["essayless"].append(key)
            if not refs:
                gaps["no_formal_reference"].append(key)
    doc = {"format": "treeka-research-index/2",
           "limitations": ["Registry references are unreviewed associations, not proof of a source-to-model interpretation.",
                           "Matched node and ledger bytes and queue membership are checked; semantic interpretation is not verified."],
           "works": works, "gaps": gaps, "ambiguous_locators": sorted(ambiguous),
           "counts": {"passages": len(works), **{k: len(v) for k, v in gaps.items()}}}
    a.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"passages: {len(works)}; gaps: " +
          ", ".join(f"{k}={len(v)}" for k, v in gaps.items()) +
          f"; ambiguous: {len(ambiguous)} -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
