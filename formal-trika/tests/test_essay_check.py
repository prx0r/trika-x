#!/usr/bin/env python3
"""test_essay_check.py — the gate must refuse forgeries, not just bad shapes.

PR #7 reproduced: an invented T-tier bullet with a different claim ID,
nonexistent chunk and only a matching receipt slug returned PASS. These
synthetic fixtures prove each forgery class now fails closed.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "essay_check.py"


def triple(tmp, slug, *, claims, theorems=(), chunk="phrdaya:phr-p05",
           status="MACHINE-COMPILED", receipt_claims=None,
           receipt_theorems=None, extra_md="", extra_ej=None,
           receipt_essay=None):
    (tmp / f"{slug}.md").write_text(
        "# Draft\n\n" + "".join(
            f"- {c['text'][:40]} [{c.get('verse_id', '')}] "
            f"({c['tier']}) [CLM-{c['id']}]\n" for c in claims) + extra_md,
        encoding="utf-8")
    ej = {"id": f"essay:{slug}", "title": "t", "date": "2026-11-08",
          "chunk": chunk, "verses": ["v"], "voice": [],
          "claims": [{"id": f"CLM-{c['id']}", "text": c["text"],
                      "verse_id": c.get("verse_id", "v"),
                      "tier": c["tier"], "kind": "premise",
                      **({"span": c["span"],
                          "span_sha256": c["span_sha256"]}
                         if "span" in c else {})}
                     for c in claims],
          "theorems": [{"name": t, "tier": "UNVERIFIED"} for t in theorems],
          "tracks": ["F1"],
          "openpatala": {"openpatala_work_id": "phrdaya",
                         "mapping_status": "CANDIDATE",
                         "edition_label": "ed"},
          "status": status}
    if extra_ej:
        ej.update(extra_ej)
    (tmp / f"{slug}.essay.json").write_text(
        json.dumps(ej, ensure_ascii=False, indent=1), encoding="utf-8")
    rc = {"format": "expansion-receipt/3", "essay": receipt_essay or slug,
          "frozen_claims": (receipt_claims if receipt_claims is not None
                            else [{"id": f"CLM-{c['id']}", "text": c["text"]}
                                  for c in claims]),
          "theorems": (receipt_theorems if receipt_theorems is not None
                       else list(theorems))}
    (tmp / f"{slug}.receipt.json").write_text(
        json.dumps(rc, ensure_ascii=False, indent=1), encoding="utf-8")


def run(slug, tmp):
    r = subprocess.run([sys.executable, str(TOOL), "--slug", slug,
                        "--swarm", str(tmp)], capture_output=True, text=True,
                       timeout=120)
    return r.returncode, r.stdout + r.stderr


GOOD = [{"id": "001", "text": "eight terms", "verse_id": "v",
         "tier": "R"}]


class TestEssayCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_triple_passes(self):
        triple(self.dir, "good", claims=GOOD)
        rc, out = run("good", self.dir)
        self.assertEqual(rc, 0, out)

    def test_invented_tier_bullet_fails(self):
        # PR #7 forgery: invented T-tier bullet, different claim id.
        triple(self.dir, "forged", claims=GOOD,
               extra_md="- invented doctrine [vX] (T) [CLM-999]\n")
        rc, out = run("forged", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("CLM-999", out)

    def test_nonexistent_chunk_fails(self):
        triple(self.dir, "nochunk", claims=GOOD, chunk="phrdaya:phr-p99")
        rc, out = run("nochunk", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("absent from", out)

    def test_changed_receipt_fails(self):
        triple(self.dir, "changed", claims=GOOD,
               receipt_claims=[{"id": "CLM-001", "text": "altered text"}])
        rc, out = run("changed", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("CLM-001", out)

    def test_receipt_claim_mismatch_fails(self):
        claims = GOOD + [{"id": "002", "text": "ninth term",
                          "verse_id": "v", "tier": "R"}]
        triple(self.dir, "mismatch", claims=claims,
               receipt_claims=[{"id": "CLM-001", "text": "eight terms"}])
        rc, out = run("mismatch", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("CLM-002", out)

    def test_tier_t_without_span_fails(self):
        triple(self.dir, "tb", claims=[
            {"id": "001", "text": "absolute", "verse_id": "v", "tier": "T"}])
        rc, out = run("tb", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("span", out)

    def test_prereview_with_signoff_fails(self):
        triple(self.dir, "signed", claims=GOOD,
               extra_ej={"signoff": {"by": "x"}})
        rc, out = run("signed", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("signoff", out)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
