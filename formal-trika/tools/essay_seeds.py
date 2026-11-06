#!/usr/bin/env python3
"""essay_seeds.py — one index over every essay seed on the box.

Kinds: owner-original (tantraessays E-series + final12), expansion-draft
(trika-x swarm, machine-compiled), research-essay/commentary/topic
(research-library assignments), pushing-session (ipvv pushing), density
(density-subtlebody shelf), research-object (ro-* dirs), subtle-body packs
(tantraloka goldrender/moderngl + frontier historical), platinum
(hxrmxs queue4 binds — included by name, scope unclear), scholar-essay
(svread Scholar projections).

Writes data/essay-seeds.json {seeds[], counts}. Statuses are kind-defaults
documented below — per-item review states live in each lane, not here.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
RLIB = Path("/root/projects/research-library")
TANTRA = Path("/root/tantraessays/essays")
IPVV = Path("/root/ipvv/site/data/pushing")


def title_of(md: Path) -> str:
    try:
        for line in md.read_text(encoding="utf-8").splitlines()[:6]:
            m = re.match(r"#+\s+(.*)", line.strip())
            if m:
                return m.group(1)[:100]
    except (OSError, ValueError):
        pass
    return md.stem


def main() -> int:
    seeds = []

    def add(sid, kind, title, path, status, extra=None):
        d = {"id": sid, "kind": kind, "title": title, "path": str(path), "status": status}
        if extra:
            d.update(extra)
        seeds.append(d)

    for f in sorted((TANTRA / "essays20").glob("E*.md")):
        add(f"owner:{f.stem}", "owner-original", title_of(f), f, "clips+framing (voice source)")
    for d in sorted((TANTRA / "final12").iterdir()):
        add(f"owner:{d.name}", "owner-original",
            title_of(d / "README.md") if (d / "README.md").is_file() else d.name,
            d, "rendered" if d.is_dir() else "file")
    for f in sorted((HERE / "swarm").glob("expansion-*.md")):
        add(f"expansion:{f.stem}", "expansion-draft", title_of(f), f, "MACHINE-COMPILED")
    for f in sorted(RLIB.glob("ESSAY-*.md")) + sorted(RLIB.glob("THREE-ESSAYS*.md")):
        add(f"research:{f.stem}", "research-essay", title_of(f), f, "assigned (collection framing)")
    for f in sorted(RLIB.glob("COMMENTARY-*.md")):
        add(f"research:{f.stem}", "commentary", title_of(f), f, "analysis (graded in-file)")
    for f in sorted((RLIB / "concept-deepdives").glob("*.md")):
        add(f"topic:{f.stem}", "topic", title_of(f), f, "topic node")
    for f in sorted((RLIB / "research-objects").iterdir()):
        add(f"ro:{f.name}", "research-object", f.name, f, "object dir")
    for f in sorted((RLIB / "density-subtlebody").glob("*.md")):
        add(f"density:{f.stem}", "density", title_of(f), f, "shelf (provenance varies)")
    for sub in ("tantraloka", "ipvv", "research"):
        base = IPVV / sub
        if not base.is_dir():
            continue
        for f in sorted(base.glob("*.md")):
            add(f"pushing:{sub}/{f.stem}", "pushing-session", title_of(f), f, "session (verdicts in-file)")
    for f in sorted(Path("/root/projects/tantraloka/goldrender").glob("subtle_body*.py")) + \
            sorted(Path("/root/projects/tantraloka/moderngl").glob("subtle_body*.py")):
        add(f"subtle:{f.stem}", "subtle-body-pack", f.stem, f, "render pack (code)")
    for f in sorted(Path("/root/hxrmxs-truth-engine/queue4").glob("*platinum*.py")):
        add(f"platinum:{f.stem}", "platinum", f.stem, f, "unexamined (scope unclear)")
    for f in sorted(Path("/root/projects/source-library/frontier").glob("subtle_body*")):
        add(f"subtle:{f.name}", "subtle-body-historical", f.name, f, "frontier shelf")
    add("corpus:essay-corpus", "idea-units", "essay-corpus (242 units, TEXT×TOPIC×GRADE×QUESTION)",
        "github:prx0r/essay-corpus", "external live repo (query via build_corpus.py)")
    from collections import Counter
    counts = dict(Counter(s["kind"] for s in seeds))
    doc = {"format": "trika-essay-seeds/1", "seeds": seeds, "counts": counts,
           "note": "statuses are kind-defaults; per-item review lives in owning lanes"}
    (HERE / "data" / "essay-seeds.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"essay seeds: {len(seeds)}")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
