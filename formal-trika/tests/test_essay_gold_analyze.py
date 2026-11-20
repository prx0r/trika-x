#!/usr/bin/env python3
"""test_essay_gold_analyze.py — the gold-standard reader must measure, not guess.

Hermetic fixtures (a synthetic chapter in a temp dir, no network). Proves:
section splitting finds the named roles; front matter is separated from body;
objection/reply moves are counted; the reference block is not mistaken for an
argument section. If the analyzer regresses, these go red before a stale
template ships.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "essay_gold_analyze.py"

CHAPTER = """\
A Synthetic Chapter on Causality

Abstract

This is an abstract with one sentence. It states the problem.

Keywords

causality · synthesis

Introduction

Why does this matter? The question has been asked before. We will see.

Historical Context

The tradition developed over centuries. See Author 2000 and Other 2001.

Encountering Buddhists

The opponent argues that mere succession is enough. Abhinavagupta says no.
Therefore the rival position fails.

Conclusion

The contribution is a new reading. A desideratum remains.

References

Primary Sources

Tantraloka of Abhinavagupta, KSTS 23.

Secondary Sources

Author, A. 2000. A book. Delhi: Press.
Other, B. 2001. Another book. Delhi: Press.
"""


def run(text: str):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "chapter.txt"
        p.write_text(text, encoding="utf-8")
        out = Path(d) / "s.json"
        r = subprocess.run([sys.executable, str(TOOL), str(p), "--out", str(out),
                            "--title", "Synthetic"],
                           capture_output=True, text=True, timeout=60)
        data = out.read_text() if out.is_file() else None
        return r, data


class GoldAnalyze(unittest.TestCase):
    def test_sections_and_roles(self):
        r, out = run(CHAPTER)
        self.assertEqual(r.returncode, 0, r.stderr)
        doc = json.loads(out)
        roles = [s["role"] for s in doc["sections"]]
        for want in ("abstract", "keywords", "introduction", "history",
                     "interlocutor", "conclusion", "references"):
            self.assertIn(want, roles)
        self.assertEqual(doc["format"], "essay-gold-structure/1")

    def test_body_excludes_front_and_references(self):
        r, out = run(CHAPTER)
        doc = json.loads(out)
        skeleton = [s["role"] for s in doc["skeleton"]]
        for excluded in ("abstract", "keywords", "references"):
            self.assertNotIn(excluded, skeleton)
        self.assertIn("introduction", skeleton)

    def test_move_counts(self):
        r, out = run(CHAPTER)
        doc = json.loads(out)
        self.assertGreaterEqual(doc["totals"]["objection_moves"], 1)
        self.assertGreaterEqual(doc["totals"]["reply_moves"], 1)
        self.assertGreaterEqual(doc["totals"]["citations_narrative"], 1)

    def test_missing_input_exits_2(self):
        r = subprocess.run([sys.executable, str(TOOL), "/nonexistent/x.txt"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 2)
        self.assertIn("no such file", r.stderr)


if __name__ == "__main__":
    unittest.main()
