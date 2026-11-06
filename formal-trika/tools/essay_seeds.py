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
import os
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
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--r2", action="store_true",
                    help="include R2 corpora (needs R2 creds in env; slower)")
    opts = ap.parse_args()
    seeds = []

    # Category = pipeline stage (USE), kind = source flavor (ORIGIN).
    # SOURCE: raw voice/material to compile from. COMPILED: machine outputs.
    # REVIEWED: human-verdict material. PUBLISHED: released outputs.
    # BRIEF: planning inputs (topics, claims, questions). RENDER: media.
    # CORPUS: bulk aggregates (counted, not listed).
    CATEGORY = {
        "owner-original": "SOURCE", "research-essay": "SOURCE",
        "commentary": "SOURCE", "topic": "BRIEF", "research-object": "SOURCE",
        "density": "SOURCE", "subtle-body-pack": "SOURCE",
        "subtle-body-historical": "SOURCE", "platinum": "SOURCE",
        "platinum-essay": "SOURCE", "video-essay": "SOURCE",
        "idea-units": "SOURCE", "imported-doc": "SOURCE",
        "essay-object": "BRIEF", "essay-seed": "BRIEF", "contention": "BRIEF",
        "info-packet": "BRIEF", "pushing-session": "REVIEWED",
        "expansion-draft": "COMPILED", "video-build": "RENDER",
        "essay-render": "RENDER", "research-corpus": "CORPUS",
        "bridge-corpus": "CORPUS",
    }
    def add(sid, kind, title, path, status, extra=None, category=None):
        d = {"id": sid, "kind": kind,
             "category": category or CATEGORY.get(kind, "SOURCE"),
             "title": title, "path": str(path), "status": status}
        if extra:
            d.update(extra)
        seeds.append(d)

    for f in sorted((TANTRA / "essays20").glob("E*.md")):
        add(f"owner:{f.stem}", "owner-original", title_of(f), f, "clips+framing (voice source)")
    for d in sorted((TANTRA / "final12").iterdir()):
        add(f"owner:{d.name}", "owner-original",
            title_of(d / "README.md") if (d / "README.md").is_file() else d.name,
            d, "released render", category="PUBLISHED")
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
    # gochema video-essays (per-dir seeds; storyboard/narration where present)
    goch = Path("/root/gochema/essays")
    if goch.is_dir():
        for d in sorted(p for p in goch.iterdir() if p.is_dir()):
            n_md = sum(1 for _ in d.rglob("*.md"))
            add(f"gochema:{d.name}", "video-essay", d.name, d,
                f"essay dir ({n_md} md files; storyboard where built)")
    # basecamp knowledge (objects, seeds, contentions, packets, works corpus)
    bck = Path("/root/projects/basecamp/knowledge")
    if bck.is_dir():
        for kind, sub in (("essay-object", "essay-objects"), ("essay-seed", "essay-seeds"),
                          ("contention", "contentions"), ("info-packet", "information-packets")):
            base = bck / sub
            if base.is_dir():
                for f in sorted(base.iterdir()):
                    add(f"basecamp:{f.stem}", kind, title_of(f) if f.is_file() else f.name,
                        f, f"{kind} (basecamp)")
        works = bck / "works"
        if works.is_dir():
            n = sum(1 for _ in works.iterdir())
            add("basecamp:works-corpus", "research-corpus",
                f"basecamp works corpus ({n} pubmed/bridge JSONs)", works,
                "aggregate node (neuroscience research corpus)")
    # imported ochema2 docs (frozen reading mirror in-repo)
    imp = HERE / "imports" / "ochema2"
    if imp.is_dir():
        for f in sorted(imp.rglob("*.md")):
            if f.name in ("PROVENANCE.md", "FINDINGS.md"):
                continue
            rel = f.relative_to(imp)
            add(f"import:{rel.parent}/{f.stem}", "imported-doc", title_of(f),
                f, "frozen mirror (upstream: prx0r/ochema2)")
    # volume essayviz builds
    evb = Path("/mnt/HC_Volume_106959365/root/projects/essayviz-workspace/build")
    if evb.is_dir():
        for d in sorted(p for p in evb.iterdir() if p.is_dir()):
            add(f"essayviz:{d.name}", "video-build", d.name, d, "essayviz build dir (volume)")
    # sanskritree platinum essays (R2, per-file; small set)
    # R2 corpora aggregates (opt-in: network + creds)
    if opts.r2:
        try:
            import boto3
            s3 = boto3.client("s3", endpoint_url="https://954612afb5a97bb15dddcdc70176813d.r2.cloudflarestorage.com",
                              aws_access_key_id=os.environ["R2_PATALA_ACCESS_KEY_ID"],
                              aws_secret_access_key=os.environ["R2_PATALA_SECRET_ACCESS_KEY"])
            pg = s3.get_paginator("list_objects_v2")
            plats = []
            for page in pg.paginate(Bucket="sanskritree", Prefix="platinum/"):
                for o in page.get("Contents", []):
                    if o["Key"].endswith("/"):
                        continue
                    plats.append((o["Key"], o["Size"]))
            for k, s in plats:
                add(f"platinum:{Path(k).stem}", "platinum-essay", Path(k).stem,
                    f"r2:sanskritree/{k}", f"platinum essay ({s}B, R2)")
            for bucket, prefix, kind in [("research-datasets", "bridge-essays/", "bridge-corpus"),
                                         ("blog-video-assets", "renders/essay", "essay-render")]:
                n = 0
                for page in pg.paginate(Bucket=bucket, Prefix=prefix):
                    n += len(page.get("Contents", []))
                    if n > 8000:
                        break
                add(f"r2:{bucket}/{prefix}", kind, f"{bucket}/{prefix} ({n} objects)",
                    f"r2:{bucket}/{prefix}", "aggregate node (corpus too large per-file)")
        except Exception as e:
            print(f"R2 section skipped: {str(e)[:100]}")
    from collections import Counter
    counts = {"by_category": dict(Counter(s["category"] for s in seeds)),
              "by_kind": dict(Counter(s["kind"] for s in seeds))}
    doc = {"format": "trika-essay-seeds/1", "seeds": seeds, "counts": counts,
           "note": ("statuses are kind-defaults; per-item review lives in owning lanes. "
                    "blogengine: not found anywhere (box, volume, R2, GitHub) — recorded absent, not missing")}
    (HERE / "data" / "essay-seeds.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print(f"essay seeds: {len(seeds)}")
    for k, v in sorted(counts["by_category"].items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
