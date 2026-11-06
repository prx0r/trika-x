#!/usr/bin/env python3
"""slang_pack.py — E1: slang-into-chat pack (pointer manifest + consent gate).

The Tantrasāra slang editions (plain-register teacher voice) are the
chat/peaching register. This tool builds a POINTER manifest (no copies:
paths + bytes + sha256 + head excerpt) for consent-gated chat-context
loading, plus the gate doc. Chat may load a slang file ONLY with an
explicit per-session grant (owner or scholar), recorded with the file's
sha; revocation drops it from context immediately. Slang NEVER replaces
cited sources — it renders them; every answer still cites T-tier spans.
Usage: python3 formal-trika/tools/slang_pack.py [--out DIR]
"""
import argparse
import hashlib
import json
from pathlib import Path

ESTATE = Path("/root/visuals/outputs/awesome-essays-extracted/awesome-essays")
FILES = ["tantrasara1", "tantrasara2", "tantrasara3", "tantrasara3-5",
         "tantrasara6-9", "tantrasara9-13", "tantrasara13-19",
         "tantrasara19-22", "shivasutrasfinal"]

GATE_DOC = """# Slang-into-chat consent gate (E1)

1. Slang files are RENDERINGS, never sources. Answers cite T-tier spans;
   slang supplies the voice.
2. Loading any slang file into chat context requires an explicit
   per-session grant (owner, or scholar for their own sessions),
   recorded as {file, sha256, granted_by, at}. No grant, no load.
3. Revocation = immediate context drop (no stale reads).
4. Slang must never soften gated content: requires-diksha units stay
   STUDY-with-conditions in every register, including slang.
5. Manifest is pointers (path+sha), never copies — one truth, no drift.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path("/root/trika-x/formal-trika/data"))
    a = ap.parse_args()
    manifest = []
    for name in FILES:
        p = ESTATE / name
        if not p.is_file():
            manifest.append({"file": name, "status": "MISSING"})
            continue
        b = p.read_bytes()
        manifest.append({"file": name, "path": str(p), "bytes": len(b),
                         "sha256": hashlib.sha256(b).hexdigest(),
                         "head": b.decode("utf-8", "replace")[:160],
                         "status": "READY"})
    (a.out / "slang-manifest.json").write_text(
        json.dumps({"register": "tantrasara-slang/1", "files": manifest,
                    "gate": "per-session grant (see CONSENT-SLANG-CHAT.md)"},
                   ensure_ascii=False, indent=1) + "\n")
    (a.out / "CONSENT-SLANG-CHAT.md").write_text(GATE_DOC)
    ready = sum(1 for m in manifest if m["status"] == "READY")
    print(f"slang files: {ready}/{len(manifest)} READY -> {a.out}")


if __name__ == "__main__":
    raise SystemExit(main())
