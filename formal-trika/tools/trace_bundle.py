#!/usr/bin/env python3
"""trace_bundle.py — compile (and verify) a trika-trace/1 bundle for one chunk.

Reads ONLY (never writes outside trika-x/formal-trika/data/traces/):
  translation-work ledgers/layers/proofs/STATUS · openpatala box DB ·
  trika-x EVIDENCE.json + runs ledger · svread scholar projections.

Usage:
  python3 formal-trika/tools/trace_bundle.py --work tantrasara-a08 --target tsa08-p03 [--tw PATH] [--out traces/]
  python3 formal-trika/tools/trace_bundle.py --verify traces/<work>-<target>.json [--tw PATH]

Exit 0 + bundle on stdout/file when compiled; --verify exits 0 only if every
hash re-checks and every recorded status still holds. Missing links are
UNKNOWN (exit 0, stated), mismatches are FAIL (exit 1, named).

Trust semantics (PR #7): `verdict` (COMPLETE/PARTIAL) means trace links are
present — nothing more. The `assurance` block measures each dimension
separately (links, span, gate, witness, formal run, review, publication) and
no dimension is inferred from another. Formal theorems are REGISTERED
associations (run_bound: false), never checked proofs. --verify compares
every canonical field including gaps, caveats, open_problems and the format
version.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
EVIDENCE = HERE / "EVIDENCE.json"
RUNS = HERE / "runs" / "runs.jsonl"
OUTDIR = HERE / "data" / "traces"
TW_DEFAULT = Path(os.environ.get("TRANSLATION_WORK", "/root/translation-work"))
SV_DEFAULT = Path(os.environ.get("SVREAD_CHECKOUT", "/root/svread"))
DSN_DEFAULT = "postgresql://patala:patala@localhost:5432/openpatala"

LAYERS = ("t1", "l0", "argmap", "l2", "c1", "l3", "l4", "c2")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(o) -> bytes:
    return json.dumps(o, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode()


def fail(msg: str) -> int:
    print(f"trace_bundle FAIL: {msg}", file=sys.stderr)
    return 1


def song_guess(target: str) -> str | None:
    """Chunk locator -> song file stem (tsa08-p03 -> tsa-a08). Heuristic for
    works whose layers are per-song files; exact chunk files always win.
    Returns None when no song shape is detectable."""
    import re
    m = re.fullmatch(r"([a-z]+?)(\d+)-p\d+", target)
    if m:
        return f"{m.group(1)}-a{int(m.group(2)):02d}"
    return None


def load_ledger(tw: Path, work: str) -> list:
    p = tw / work / "passages.jsonl"
    if not p.exists():
        raise FileNotFoundError(f"no ledger: {p}")
    rows = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def layer_candidates(tw: Path, work: str, target: str, layer: str):
    """Yield (path, status): exact chunk files first, else song-guess files
    (BOUND-WHOLE-SONG), else work-level markdown (BOUND-WORK-MD — the TAL
    layout ships L1/L2/L200/T1 as work files, not per-song JSON; recorded
    as bound-to-work, never as chunk-level proof)."""
    exact = tw / work / "data" / f"{target}.{layer}.json"
    if exact.exists():
        yield exact, "BOUND"
        return
    sg = song_guess(target)
    if sg:
        p = tw / work / "data" / f"{sg}.{layer}.json"
        if p.exists():
            yield p, "BOUND-WHOLE-SONG"
            return
    wl = (tw / work / "data" / f"{work}.{layer}.json")
    if wl.exists():
        yield wl, "BOUND-WORK-MD"
        return
    md_names = {"t1": "T1.md", "l2": "L2.md", "argmap": "ARGMAP.md",
                "c1": "C1.md", "l1": "L1.md", "l200": "L200.md"}
    md = md_names.get(layer)
    if md and (tw / work / md).exists():
        yield (tw / work / md), "BOUND-WORK-MD"


def resolve_formal(evidence: dict, work: str, target: str):
    """Join EVIDENCE theorems to a (work, locator) pair through the works
    inventory — never on a bare locator (duplicate locators exist across
    works). Returns (theorems, problems). Ambiguous or foreign locators
    yield no theorems plus a named problem, never a cross-work attribution.
    """
    problems = []
    by_loc: dict[str, set] = {}
    for spec in (evidence.get("works") or {}).values():
        ledger = spec.get("ledger", "")
        parts = Path(ledger.replace("translation-work/", "")).parts
        if len(parts) != 2 or parts[1] != "passages.jsonl":
            continue
        for loc in spec.get("chunks", []) or []:
            by_loc.setdefault(loc, set()).add(parts[0])
    owners = by_loc.get(target, set())
    if len(owners) != 1 or next(iter(owners)) != work:
        if owners:
            problems.append(
                "EVIDENCE locator ambiguous or foreign: "
                f"{target} owned by {sorted(owners)}")
        return [], problems
    theorems = []
    for thm, ent in (evidence.get("entries") or {}).items():
        for c in (ent.get("chunks") or []):
            if c.get("locator") == target:
                theorems.append({"theorem": thm,
                                 "kind": ent.get("kind"),
                                 "via": c.get("via"),
                                 "tier": c.get("tier"),
                                 "status": c.get("status"),
                                 "run_bound": False,
                                 "run_note": ("registry reference only; "
                                              "no per-declaration run "
                                              "digest bound")})
    return theorems, problems


def compile_bundle(work: str, target: str, tw: Path, sv: Path,
                   dsn: str, use_db: bool = True) -> tuple[dict, int]:
    problems = []
    caveats_later = []
    rows = load_ledger(tw, work)
    hits = [r for r in rows if r.get("locator") == target]
    if len(hits) != 1:
        return {}, fail(f"locator {target!r}: {len(hits)} exact matches "
                        f"(need exactly 1; no prefix guessing)")
    row = hits[0]
    immutable = row.get("immutable_id", "")
    sanskrit = row.get("sanskrit", "")
    src_bytes = sanskrit.encode() if isinstance(sanskrit, str) else b""
    source = {"bytes_sha256": sha(src_bytes) if src_bytes else None,
              "bytes_present": bool(src_bytes),
              "ledger": f"{work}/passages.jsonl",
              "immutable_id": immutable,
              "verses": row.get("verses", "")}
    # SOURCE.sha cross-check where present
    sha_files = list((tw / work).glob("SOURCE.sha")) + \
        list((tw / work / "source").glob("*.sha")) if (tw / work).exists() else []
    if sha_files:
        recorded = sha_files[0].read_text().strip().split()[0]
        source["source_sha_file"] = str(sha_files[0].relative_to(tw))
        source["source_sha_recorded"] = recorded
        # ledger sanskrit is an excerpt, not the whole volume: record, don't equate
        source["source_sha_note"] = ("ledger span vs volume file differ by "
                                     "design; no equality claimed")
    else:
        source["source_sha_file"] = None
    # edition label from bridge map if present (candidate, never proof)
    edition = {"label": None, "status": "UNKNOWN"}
    try:
        mmap = json.loads((HERE / "bridge" / "openpatala-map.json").read_text())
        for _k, v in (mmap.get("works", {}) or {}).items():
            if isinstance(v, dict) and v.get("ours", "").endswith("/" + work):
                edition = {"label": v.get("edition"),
                           "status": v.get("status", "UNKNOWN")}
                break
    except (OSError, ValueError):
        problems.append("bridge map unreadable")
    source["edition"] = edition
    source["witness"] = {"id": None, "status": "UNPINNED"}

    # 2. openpatala identity
    identity = {"db": None, "rows": {}, "status": "UNKNOWN"}
    if use_db:
        try:
            import psycopg2
            cx = psycopg2.connect(dsn)
            cur = cx.cursor()
            cur.execute("SELECT work_id, citation_value FROM passages "
                        "WHERE id = %s", (immutable,))
            r = cur.fetchone()
            if r:
                identity["rows"]["passage"] = {"work_id": r[0],
                                               "citation_value": r[1]}
            cur.execute("SELECT id, title FROM editions WHERE work_id = %s",
                        (work,))
            identity["rows"]["editions"] = [{"id": x[0], "title": x[1]}
                                            for x in cur.fetchall()]
            cur.execute("SELECT id, provider_id, artifact_id FROM etexts "
                        "WHERE work_id = %s", (work,))
            identity["rows"]["etexts"] = [{"id": x[0], "provider": x[1],
                                           "artifact": x[2]}
                                          for x in cur.fetchall()]
            cur.execute("SELECT count(*) FROM witnesses")
            identity["rows"]["witnesses_total"] = cur.fetchone()[0]
            cx.close()
            identity["db"] = re.sub(r":[^@/]*@", ":***@", dsn)
            identity["status"] = ("BOUND" if identity["rows"].get("passage")
                                  else "UNRESOLVED")
            if identity["status"] == "UNRESOLVED":
                problems.append("passage id absent from box DB")
        except Exception as e:
            identity["status"] = "UNKNOWN"
            problems.append(f"DB unreadable: {type(e).__name__}")
    else:
        problems.append("DB skipped (--no-db)")

    # 3+4. layers + proofs
    layers = {}
    for layer in LAYERS:
        got = list(layer_candidates(tw, work, target, layer))
        if not got:
            if layer == "c2":
                layers[layer] = {"present": False, "status": "NOT-APPLICABLE",
                                 "note": "C2 renders are optional (owner: "
                                         "existing C2 stays; waived)"}
            else:
                layers[layer] = {"present": False, "status": "UNKNOWN"}
            continue
        p, status = got[0]
        raw = p.read_bytes()
        try:
            rel = p.relative_to(tw).as_posix()
        except ValueError:
            rel = f"{work}/{p.name}"
        entry = {"present": True, "sha256": sha(raw),
                 "path": rel, "status": status}
        if status == "BOUND-WHOLE-SONG":
            entry["note"] = ("chunk is a span of this song file; "
                             "span-level binding needs a verse-range join")
        elif status == "BOUND-WORK-MD":
            entry["note"] = ("work-level markdown layer, not per-chunk JSON; "
                             "bound to the work, not the chunk span")
        layers[layer] = entry
    proofs = {}
    song = re.sub(r"-v\d+$", "", target)
    pf = tw / work / "proof" / f"proof-{song}.json"
    if not pf.exists():
        sg = song_guess(target)
        if sg:
            pf = tw / work / "proof" / f"proof-{sg}.json"
    # PR #7: a proof file is evidence only through EXPLICIT fields. An
    # absent `blocking` list is UNKNOWN, never an empty list; PASS requires
    # deterministic_gate == PASS with empty blocking AND recorded warnings.
    REQUIRED_PROOF_KEYS = ("deterministic_gate", "blocking", "warnings",
                           "tool")
    if pf.exists():
        try:
            pj = json.loads(pf.read_text(encoding="utf-8"))
            raw = pf.read_bytes()
            missing = [k for k in REQUIRED_PROOF_KEYS if k not in pj]
            entry = {"file": f"{work}/proof/{pf.name}",
                     "sha256": sha(raw),
                     "blocking": list(pj.get("blocking", [])),
                     "warnings": int(len(pj.get("warnings", []))),
                     "tool": pj.get("tool"),
                     "deterministic_gate": pj.get("deterministic_gate")}
            if missing:
                entry["status"] = "UNKNOWN"
                entry["note"] = ("proof fields incomplete, missing: "
                                 + ",".join(missing))
                problems.append("proof fields incomplete: "
                                + ",".join(missing))
            elif (pj.get("deterministic_gate") == "PASS"
                  and not pj.get("blocking")):
                entry["status"] = "PASS"
            elif (pj.get("deterministic_gate") == "BLOCKED"
                  or pj.get("blocking")):
                entry["status"] = "BLOCKED"
            else:
                entry["status"] = "UNKNOWN"
                entry["note"] = "gate inconclusive"
                problems.append("proof gate inconclusive")
            if isinstance(pj.get("warnings"), list) and pj["warnings"]:
                caveats_later.append(
                    f"song_proof warnings: {len(pj['warnings'])}")
            proofs["song_proof"] = entry
        except (OSError, ValueError) as e:
            proofs["song_proof"] = {"status": "UNREADABLE", "error": str(e)[:120]}
    else:
        proofs["song_proof"] = {"status": "UNKNOWN", "note": "no proof file"}
    gf = tw / work / "GATE.json"
    if gf.exists():
        try:
            gj = json.loads(gf.read_text(encoding="utf-8"))
            ge = gj.get(target)
            if isinstance(ge, dict):
                missing = [k for k in ("deterministic_gate", "blocking")
                           if k not in ge]
                checks = ge.get("checks", {})
                entry = {
                    "deterministic_gate": ge.get("deterministic_gate"),
                    "blocking": list(ge.get("blocking", [])),
                    "checks_pass": {k: bool(v[0]) for k, v in checks.items()
                                    if isinstance(v, (list, tuple)) and v},
                    "entry_sha256": sha(json.dumps(
                        ge, sort_keys=True).encode())}
                if missing:
                    entry["status"] = "UNKNOWN"
                    entry["note"] = ("gate fields incomplete, missing: "
                                     + ",".join(missing))
                    problems.append("chunk gate fields incomplete")
                elif (ge.get("deterministic_gate") == "PASS"
                      and not ge.get("blocking")):
                    entry["status"] = "PASS"
                elif (ge.get("deterministic_gate") == "BLOCKED"
                      or ge.get("blocking")):
                    entry["status"] = "BLOCKED"
                else:
                    entry["status"] = "UNKNOWN"
                    entry["note"] = "gate inconclusive"
                    problems.append("chunk gate inconclusive")
                proofs["chunk_gate"] = entry
            else:
                proofs["chunk_gate"] = {"status": "UNKNOWN",
                                        "note": "chunk not in GATE.json"}
        except (OSError, ValueError) as e:
            proofs["chunk_gate"] = {"status": "UNREADABLE", "error": str(e)[:120]}
    else:
        proofs["chunk_gate"] = {"status": "UNKNOWN", "note": "no GATE.json"}

    # 5. formal — joined on (work, locator) through the works inventory,
    # never on a bare locator (duplicate locators exist across works).
    # Status is REGISTERED: a registry reference is not a checked proof
    # and no per-declaration run digest is bound (PR #7). MODEL_CHECKED
    # may only be emitted with a verifiable declaration-specific
    # successful run bound to statement + toolchain + artifact digest.
    formal = []
    try:
        ev = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        formal, fprobs = resolve_formal(ev, work, target)
        problems.extend(fprobs)
    except (OSError, ValueError) as e:
        problems.append(f"EVIDENCE unreadable: {type(e).__name__}")
    formal_status = ("REGISTERED" if formal else "none")

    # 6. essays (verbatim mention only — never claim support)
    essays = []
    proj = sv / "data" / "scholar" / f"{work}.json"
    if proj.exists():
        try:
            pj = json.loads(proj.read_text(encoding="utf-8"))
            for e in pj.get("essays", []) or []:
                text = json.dumps(e.get("text", e)) if isinstance(e, dict) else ""
                if not text:
                    try:
                        text = json.dumps(e)
                    except (TypeError, ValueError):
                        text = ""
                if target in text or song in text:
                    essays.append({"essay_id": e.get("essay_id") if isinstance(e, dict) else None,
                                   "author": e.get("author") if isinstance(e, dict) else None,
                                   "identity_state": e.get("identity_state") if isinstance(e, dict) else None,
                                   "rights": e.get("rights") if isinstance(e, dict) else None,
                                   "cites_text": True,
                                   "claim_support": "UNASSESSED (needs essay-claim/1 + audit)"})
            proj_sha = pj.get("projection_sha256")
        except (OSError, ValueError):
            proj_sha = None
            problems.append("scholar projection unreadable")
    else:
        proj_sha = None
        problems.append("no scholar projection for work")

    gaps = [f"layer:{k}" for k, v in layers.items()
            if isinstance(v, dict) and v.get("status") == "UNKNOWN"]
    if not source.get("bytes_present"):
        gaps.append("source:bytes")
    if identity.get("status") in ("UNKNOWN", "UNRESOLVED"):
        gaps.append("identity:db")
    if proofs.get("song_proof", {}).get("status") in ("UNKNOWN", "UNREADABLE"):
        gaps.append("proofs:song")
    caveats = [f"layer:{k}=whole-song-span" for k, v in layers.items()
               if isinstance(v, dict)
               and v.get("status") == "BOUND-WHOLE-SONG"]
    caveats.extend(caveats_later)
    cg = proofs.get("chunk_gate", {})
    if cg.get("status") == "BLOCKED":
        caveats.append("chunk_gate BLOCKED: "
                       + ",".join(cg.get("blocking", [])))
    verdict = "COMPLETE" if not gaps else "PARTIAL"
    # PR #7: separated assurance dimensions. COMPLETE means trace links are
    # present — nothing more. Each dimension below is independently measured;
    # no dimension is inferred from another.
    gate_status = proofs.get("chunk_gate", {}).get("status", "UNKNOWN")
    assurance = {
        "trace_links_present":
            "PASS" if (source.get("bytes_present")
                       and all(isinstance(v, dict)
                               and (v.get("present") or v.get("status")
                                    == "NOT-APPLICABLE")
                               for v in layers.values())
                       and proofs.get("song_proof", {}).get("status")
                       in ("PASS", "BLOCKED")) else "FAIL",
        "source_span_verified": "UNKNOWN",
        "source_span_note": ("ledger span is an excerpt; the edition volume "
                             "is not hashed — span completeness unverified"),
        "chunk_gate": (gate_status if gate_status in ("PASS", "BLOCKED")
                       else "UNKNOWN"),
        "witness": (source.get("witness", {}) or {}).get("status",
                                                         "UNPINNED"),
        "formal_run": "UNBOUND",
        "formal_run_note": ("registry references only; no per-declaration "
                            "run digest bound"),
        "review": "UNREVIEWED",
        "review_note": "no review decision bound to this trace",
        "publication": "NOT_AUTHORIZED",
        "publication_note": "human sign-off required; never automatic",
    }
    bundle = {
        "format": "trika-trace/1",
        "chunk": {"work": work, "target": target,
                  "immutable_id": immutable},
        "source": source,
        "identity": identity,
        "layers": layers,
        "proofs": proofs,
        "formal": {"theorems": formal, "status": formal_status},
        "assurance": assurance,
        "verdict_scope": ("links present only — see assurance, gaps, "
                          "caveats. COMPLETE is not approval, proof, or "
                          "witness verification."),
        "essays": {"citing": essays,
                   "projection_sha256": proj_sha},
        "verdict": verdict,
        "gaps": gaps,
        "caveats": caveats,
        "open_problems": problems,
    }
    return bundle, 0


def verify_bundle(bundle: dict, tw: Path, sv: Path, dsn: str) -> int:
    work = bundle["chunk"]["work"]
    target = bundle["chunk"]["target"]
    fresh, rc = compile_bundle(work, target, tw, sv, dsn,
                               use_db=bundle.get("identity", {}).get("db") is not None)
    if rc != 0:
        return fail("recompilation failed")
    # PR #7: verify compares EVERY canonical field — including gaps,
    # caveats, open_problems, assurance and the format version. A bundle
    # with removed warnings verifies as changed, never as clean.
    def norm(o):
        o = json.loads(json.dumps(o, sort_keys=True))
        o.pop("produced_at", None)
        o.pop("produced_by", None)
        return o
    a, b = norm(bundle), norm(fresh)
    if a.get("format") != b.get("format"):
        return fail(f"format changed {a.get('format')} -> {b.get('format')}")
    if a == b:
        print(f"trace_bundle VERIFIED: {work}:{target} "
              f"(verdict {b.get('verdict')}; "
              f"{len(b.get('gaps', []))} gaps, "
              f"{len(b.get('caveats', []))} caveats re-checked)")
        return 0
    # name the first divergence for a readable failure
    for key in sorted(set(a) | set(b)):
        if a.get(key) != b.get(key):
            va, vb = a.get(key), b.get(key)
            if isinstance(va, dict) and isinstance(vb, dict):
                ka, kb = set(va), set(vb)
                return fail(f"divergence in {key!r} "
                            f"(removed={sorted(ka - kb)[:5]} "
                            f"added={sorted(kb - ka)[:5]})")
            if isinstance(va, list) and isinstance(vb, list):
                return fail(f"divergence in {key!r}: "
                            f"recorded {va} vs fresh {vb}")
            return fail(f"divergence in {key!r}: "
                        f"recorded {va!r} vs fresh {vb!r}")
    return fail("bundles differ in no enumerable key (non-canonical JSON?)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--work", help="translation-work dir")
    ap.add_argument("--target", help="chunk locator, e.g. tsa08-p03")
    ap.add_argument("--tw", default=str(TW_DEFAULT))
    ap.add_argument("--sv", default=str(SV_DEFAULT))
    ap.add_argument("--dsn", default=DSN_DEFAULT)
    ap.add_argument("--no-db", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--verify", default=None)
    a = ap.parse_args()
    tw, sv = Path(a.tw), Path(a.sv)
    if a.verify:
        try:
            bundle = json.loads(Path(a.verify).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            return fail(f"cannot read bundle: {e}")
        if bundle.get("format") != "trika-trace/1":
            return fail("not a trika-trace/1 bundle")
        return verify_bundle(bundle, tw, sv, a.dsn)
    if not a.work or not a.target:
        print("need --work and --target (or --verify FILE)", file=sys.stderr)
        return 2
    bundle, rc = compile_bundle(a.work, a.target, tw, sv, a.dsn,
                                use_db=not a.no_db)
    if rc != 0:
        return rc
    import subprocess
    try:
        rev = subprocess.run(["git", "-C", str(HERE.parent.parent),
                              "rev-parse", "--short", "HEAD"],
                             capture_output=True, check=True,
                             text=True).stdout.strip()
    except Exception:
        rev = "UNKNOWN"
    bundle["produced_by"] = {"tool": "trace_bundle/1", "trika_rev": rev}
    import datetime
    bundle["produced_at"] = datetime.datetime.now(
        datetime.timezone.utc).isoformat(timespec="seconds")
    text = json.dumps(bundle, ensure_ascii=False, sort_keys=True, indent=1)
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out} (verdict {bundle['verdict']})")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
