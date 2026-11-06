#!/usr/bin/env python3
"""blind.py — generate blind/ variants (comment-stripped Lean for blind readers).

Thon Ly's formal-abhidhamma has model/blind/ (comment-stripped Lean given to
a second encoder who never saw the original). Ours: strip file headers and
line comments, keep docstrings (/-- ... -/) as field meanings, keep all
code. The blind reader sees types, rules, and theorem statements — nothing
of how they were written.

  python3 tools/blind.py           regenerate blind/
  python3 tools/blind.py --check   exit 1 if blind/ is stale (CI)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLIND = ROOT / "blind"
SOURCES = [
    "control/Mala.lean", "control/Pramatr.lean", "control/Kancuka.lean",
    "control/Recognition.lean", "control/AnswerKey.lean", "control/Tattva.lean",
    "recognition/Transitions.lean", "recognition/NonEntail.lean",
    "recognition/Conjuncts.lean", "recognition/Memory.lean",
    "recognition/Tractatus.lean", "recognition/Coords.lean",
    "recognition/KancukaCorr.lean", "recognition/Grace.lean",
    "recognition/Upaya.lean",
]


def strip(text):
    # drop file headers (/- ... -/) and line comments; keep docstrings
    text = re.sub(r"/-(?!-).*?-/", "", text, flags=re.S)
    text = re.sub(r"(?m)^\s*--.*\n", "", text)
    # collapse blank runs
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def build():
    chunks = []
    for rel in SOURCES:
        src = ROOT / rel
        if not src.is_file():
            continue
        name = Path(rel).name
        body = strip(src.read_text(encoding="utf-8"))
        chunks.append(f"-- blind/{name} (from {rel})\n{body.rstrip()}\n")
    return "\n".join(chunks)


def main():
    want = build()
    if "--check" in sys.argv:
        cur = (BLIND / "ALL.lean").read_text(encoding="utf-8") if (BLIND / "ALL.lean").is_file() else ""
        if cur != want:
            print("blind/ALL.lean is STALE — run tools/blind.py")
            return 1
        print("blind/ALL.lean is current")
        return 0
    BLIND.mkdir(exist_ok=True)
    (BLIND / "ALL.lean").write_text(want, encoding="utf-8")
    n = want.count("-- blind/")
    print(f"blind/ALL.lean: {n} files, {want.count(chr(10))} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
