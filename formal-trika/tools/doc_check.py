#!/usr/bin/env python3
"""doc_check.py — the documentation gate: every registered doc exists, is
honestly labelled, keeps its verified numbers, links resolve, and the
geometry holds.

  python3 formal-trika/tools/doc_check.py [--root REPO]

Reads formal-trika/data/docs.json (the registry). For each entry:
 1. file exists; first-15-lines `*Status: TIER*` matches registry;
 2. CANONICAL / HISTORICAL / SUPERSEDED carry a YYYY-MM-DD date (header or filename);
 3. each claim: extract the doc number with its pattern, compute the live
    number with its source, compare. requires:["db"] skips without a box DB.
    Skips are listed, never silent.
 4. every relative markdown link resolves to a file in the repo.
Then: geometry nodes resolve; geometry edges resolve both ends.

WARN (never fail, listed): prose that looks like an unregistered live number
(`N tools|theorems|works|passages|chunks|tests|gates|bundles|families|entries|witnesses`,
`N/M`) in a CANONICAL doc, minus allow_stale patterns.

Exit 0 + "docs: SHARP" iff zero FAIL. Exit 1 + "docs: DRIFT" otherwise.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DEFAULT_ROOT = HERE.parent.parent


def run(argv, cwd, timeout, env=None):
    try:
        e = dict(os.environ)
        if env:
            e.update(env)
        p = subprocess.run([str(a) for a in argv], cwd=str(cwd),
                           capture_output=True, text=True, timeout=timeout,
                           env=e)
        return p, None
    except (OSError, subprocess.TimeoutError) as e:
        return None, str(e)


DB_ENV = {"PGHOST": "127.0.0.1", "PGUSER": "patala",
          "PGCONNECT_TIMEOUT": "5"}


def have_db():
    try:
        p = subprocess.run(["psql", "-h", "127.0.0.1", "-U", "patala",
                            "-d", "openpatala", "-tA", "-c", "SELECT 1"],
                           capture_output=True, text=True, timeout=8,
                           env={**os.environ, "PGCONNECT_TIMEOUT": "3",
                                "PGPASSWORD": os.environ.get("PGPASSWORD", "patala")})
        return p.returncode == 0
    except (OSError, subprocess.TimeoutError):
        return False


PATH_DEFAULTS = {"TRANSLATION_WORK": "/root/translation-work"}


def expand_argv(argv):
    """Expand $VARS (env, then built-in defaults). Returns (list, missing)."""
    out = []
    for a in argv:
        if isinstance(a, str) and "$" in a:
            import re as _re

            def sub(m):
                v = m.group(1)
                return os.environ.get(v, PATH_DEFAULTS.get(v, m.group(0)))
            b = _re.sub(r"\$([A-Za-z_][A-Za-z0-9_]*)", sub, a)
            if b != a and not os.path.exists(b):
                return None, b
            out.append(b)
        else:
            out.append(a)
    return out, None


def check_claim(doc, claim, text, root, box_db, fails, warns, skips):
    cid, pat = claim["id"], claim["pattern"]
    src = claim.get("source", {})
    m = re.search(pat, text)
    if not m:
        if claim.get("optional"):
            skips.append(f"{doc}:{cid} pattern absent (optional)")
            return
        fails.append(f"{doc}:{cid} pattern not found: {pat[:80]}")
        return
    doc_num = m.group(1) if m.lastindex else m.group(0)
    req = claim.get("requires", [])
    if "db" in req and not box_db:
        skips.append(f"{doc}:{cid} skipped: no box DB")
        return
    live = None
    if "argv" in src:
        argv, missing = expand_argv(src["argv"])
        if argv is None:
            skips.append(f"{doc}:{cid} skipped: missing path {missing}")
            return
        call_env = None
        if "db" in (claim.get("requires") or []):
            call_env = dict(DB_ENV)
            call_env["PGPASSWORD"] = os.environ.get("PGPASSWORD", "patala")
            p, err = run(argv, REPO, src.get("timeout", 300), call_env)
        else:
            p, err = run(argv, REPO, src.get("timeout", 300))
        if p is None:
            fails.append(f"{doc}:{cid} command failed to run: {err}")
            return
        if p.returncode != 0:
            fails.append(f"{doc}:{cid} command exited {p.returncode}: {(p.stderr or p.stdout or '')[:200]}")
            return
        sm = re.search(src["pattern"], p.stdout + "\n" + p.stderr, re.MULTILINE)
        if not sm:
            fails.append(f"{doc}:{cid} live pattern not found in command output")
            return
        live = sm.group(1) if sm.lastindex else sm.group(0)
    elif "ledger" in src:
        try:
            from functools import reduce
            import operator
            data = json.loads((root / "formal-trika" / "data" / "freshness.json").read_text(encoding="utf-8"))
            live = reduce(operator.getitem, src["ledger"].split("."), data)
        except (OSError, ValueError, KeyError, TypeError) as e:
            fails.append(f"{doc}:{cid} ledger read failed: {e}")
            return
    elif "jsonfile" in src:
        try:
            data = json.loads((root / src["jsonfile"]).read_text(encoding="utf-8"))
            for k in src.get("key", "").split("."):
                data = data[k]
            live = data
        except (OSError, ValueError, KeyError, TypeError) as e:
            fails.append(f"{doc}:{cid} json read failed: {e}")
            return
    elif "ci" in src:
        try:
            wf = (REPO / ".github" / "workflows" / "formal-checks.yml").read_text(encoding="utf-8")
        except OSError as e:
            fails.append(f"{doc}:{cid} cannot read CI workflow: {e}")
            return
        if src["ci"] not in wf:
            fails.append(f"{doc}:{cid} CI does not run {src['ci']}")
            return
        return
    else:
        fails.append(f"{doc}:{cid} unknown source kind")
        return
    if str(doc_num).strip() != str(live).strip():
        fails.append(f"{doc}:{cid} DRIFT doc={doc_num!r} live={live!r}")


WARN_PATS = [re.compile(r"\b\d{2,4}\s+(?:tools|theorems|works|passages|chunks|tests?|gates|bundles|families|entries|witnesses)\b"),
             re.compile(r"(?<!\d)\d{1,4}/\d{1,4}(?!\d)")]


def main() -> int:
    root = Path(sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else REPO)
    reg = json.loads((root / "formal-trika" / "data" / "docs.json").read_text(encoding="utf-8"))
    docs = reg["docs"]
    fails, warns, skips = [], [], []
    checked = 0
    box_db = have_db()
    on_disk = {p.name for p in root.glob("*.md")}
    for f in sorted(on_disk):
        if f not in docs:
            fails.append(f"unregistered doc: {f} (register it, move it, or delete it)")
    for name, spec in docs.items():
        p = root / name
        if not p.is_file():
            fails.append(f"registered but missing: {name}")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        head = "\n".join(text.split("\n")[:15])
        m = re.search(r"\*Status:\s*([A-Z_]+)", head)
        if not m or m.group(1) != spec["status"]:
            fails.append(f"{name}: header status {m.group(1) if m else None!r} != registry {spec['status']!r}")
            continue
        if spec["status"] in ("CANONICAL", "HISTORICAL", "SUPERSEDED"):
            if not (re.search(r"\d{4}-\d{2}-\d{2}", head) or re.search(r"\d{4}-\d{2}-\d{2}", name)):
                fails.append(f"{name}: {spec['status']} requires a date (header or filename)")
        for claim in spec.get("claims", []):
            check_claim(name, claim, text, root, box_db, fails, warns, skips)
            checked += 1
        if spec["status"] == "CANONICAL":
            allows = [re.compile(a) for a in spec.get("allow_stale", [])]
            for wp in WARN_PATS:
                for wm in wp.finditer(text):
                    line_start = text.rfind("\n", 0, wm.start()) + 1
                    line_end = text.find("\n", wm.end())
                    line = text[line_start:line_end if line_end != -1 else len(text)]
                    # A number on, or within one line of, an explicit
                    # YYYY-MM-DD is a dated claim (spec: dated scopes are valid
                    # history), not live-number drift.
                    ls = text.rfind("\n", 0, wm.start()) + 1
                    le = text.find("\n", wm.end())
                    le = len(text) if le == -1 else le
                    prev_nl = text.rfind("\n", 0, max(0, ls - 1))
                    next_nl = text.find("\n", le + 1)
                    window = text[prev_nl + 1:(len(text) if next_nl == -1 else text.find("\n", next_nl + 1) if text.find("\n", next_nl + 1) != -1 else len(text))]
                    if re.search(r"\d{4}-\d{2}-\d{2}", window):
                        continue
                    ctx = text[max(0, wm.start() - 60):wm.end() + 30].replace("\n", " ")
                    if not any(a.search(ctx) for a in allows):
                        warns.append(f"{name}: unregistered live-looking number {wm.group(0)!r} (…{ctx.strip()[:90]}…)")
        for lm in re.finditer(r"\[[^\]]*\]\(([^)#\s][^)\s]*)\)", text):
            tgt = lm.group(1).split("#", 1)[0]
            if not tgt or tgt.startswith(("http://", "https://", "mailto:")) or "@" in tgt:
                continue
            if not ((root / tgt).exists() or (p.parent / tgt).exists()):
                fails.append(f"{name}: dead link → {tgt}")
    # geometry
    try:
        geo = json.loads((root / "formal-trika" / "data" / "docs-geometry.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        fails.append(f"geometry file unreadable: {e}")
        geo = {"nodes": [], "edges": []}
    node_ids = set()
    for n in geo.get("nodes", []):
        nid, kind = n.get("id", ""), n.get("kind", "")
        node_ids.add(nid)
        if kind == "doc":
            if not (root / nid).is_file():
                fails.append(f"geometry: doc node missing: {nid}")
        elif kind == "code" or kind == "data":
            if not (root / nid).is_file():
                fails.append(f"geometry: {kind} node missing: {nid}")
        elif kind == "repo":
            if not os.path.isdir(f"/root/{nid}"):
                skips.append(f"geometry: repo node absent on this box (skipped): {nid}")
        else:
            fails.append(f"geometry: unknown node kind {kind!r} for {nid}")
    for e in geo.get("edges", []):
        for end in (e.get("from"), e.get("to")):
            if end not in node_ids and end not in docs:
                fails.append(f"geometry: edge endpoint unknown: {end}")
    print(f"checked {len(docs)} docs, {checked} claims: "
          f"{len(fails)} FAIL, {len(warns)} warn, {len(skips)} skip")
    for s in skips:
        print("  SKIP:", s)
    show_all = "--all-warns" in sys.argv
    for w in (warns if show_all else warns[:10]):
        print("  WARN:", w)
    if not show_all and len(warns) > 10:
        print(f"  … {len(warns) - 10} more warnings (review queue; --all-warns to list)")
    for f in fails:
        print("  FAIL:", f)
    if fails:
        print("docs: DRIFT")
        return 1
    print("docs: SHARP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
