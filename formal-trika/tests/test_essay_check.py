#!/usr/bin/env python3
"""test_essay_check.py — the gate must refuse forgeries, not just bad shapes.

PR #7 reproduced: an invented T-tier bullet with a different claim ID,
nonexistent chunk and only a matching receipt slug returned PASS. These
synthetic fixtures prove each forgery class now fails closed.
"""
import json
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "essay_check.py"
SOURCE = "madhyavikāsāc cidānandalābhaḥ"
SOURCE_HASH = hashlib.sha256(SOURCE.encode("utf-8")).hexdigest()


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
                      **{k: c[k] for k in
                         ("span", "span_sha256", "source_sha256", "source_edition", "source_binding_version") if k in c}}
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
                            else [{"id": f"CLM-{c['id']}", "text": c["text"],
                                   **({k: c[k] for k in
                                       ("tier", "span", "span_sha256", "source_sha256", "source_edition", "source_binding_version") if k in c}
                                      if c["tier"] == "T" else {})}
                                  for c in claims]),
          "theorems": (receipt_theorems if receipt_theorems is not None
                       else list(theorems))}
    (tmp / f"{slug}.receipt.json").write_text(
        json.dumps(rc, ensure_ascii=False, indent=1), encoding="utf-8")


def run(slug, tmp):
    env = {**os.environ, "TRANSLATION_WORK": str(tmp / "translation-work")}
    r = subprocess.run([sys.executable, str(TOOL), "--slug", slug,
                        "--swarm", str(tmp)], capture_output=True, text=True, env=env,
                       timeout=120)
    return r.returncode, r.stdout + r.stderr


GOOD = [{"id": "001", "text": "eight terms", "verse_id": "v",
         "tier": "R"}]


class TestEssayCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.ledger = self.dir / "translation-work" / "phrdaya" / "passages.jsonl"
        self.ledger.parent.mkdir(parents=True)
        self.row = {"locator": "phr-p05", "sanskrit": SOURCE,
                    "source_edition": "GRETIL"}
        self.ledger.write_text(json.dumps(self.row, ensure_ascii=False) + "\n", encoding="utf-8")

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

    def text_claim(self, span="madhyavikāsāc"):
        return {"id": "001", "text": "textual reading", "tier": "T", "span": span,
                "span_sha256": hashlib.sha256(span.encode("utf-8")).hexdigest(),
                "source_sha256": SOURCE_HASH, "source_edition": "GRETIL", "source_binding_version": 2}

    def test_valid_text_claim_binds_source_and_receipt(self):
        triple(self.dir, "real", claims=[self.text_claim()])
        rc, out = run("real", self.dir)
        self.assertEqual(rc, 0, out)

    def test_invented_span_fails_even_with_matching_self_hash(self):
        triple(self.dir, "fake", claims=[self.text_claim("invented quotation")])
        rc, out = run("fake", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("span absent from source passage", out)

    def test_changed_source_passage_fails(self):
        triple(self.dir, "stale", claims=[self.text_claim()])
        self.row["sanskrit"] += " changed"
        self.ledger.write_text(json.dumps(self.row, ensure_ascii=False), encoding="utf-8")
        rc, out = run("stale", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("source passage digest mismatch", out)

    def test_changed_edition_fails(self):
        triple(self.dir, "edition", claims=[self.text_claim()])
        self.row["source_edition"] = "Different source"
        self.ledger.write_text(json.dumps(self.row, ensure_ascii=False), encoding="utf-8")
        rc, out = run("edition", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("source edition mismatch", out)

    def test_duplicate_ledger_locator_fails(self):
        triple(self.dir, "duplicate", claims=[self.text_claim()])
        with self.ledger.open("a", encoding="utf-8") as f:
            f.write(json.dumps(self.row, ensure_ascii=False) + "\n")
        rc, out = run("duplicate", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("duplicated", out)

    def test_changed_receipt_source_fails(self):
        claim = self.text_claim()
        receipt = {"id": "CLM-001", **{k: claim[k] for k in
                   ("text", "tier", "span", "span_sha256", "source_sha256", "source_edition", "source_binding_version")}}
        receipt["source_sha256"] = "changed"
        triple(self.dir, "changedsource", claims=[claim], receipt_claims=[receipt])
        rc, out = run("changedsource", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("source_sha256 differs", out)

    def test_directory_traversal_in_chunk_fails(self):
        triple(self.dir, "traversal", claims=GOOD, chunk="../phrdaya:phr-p05")
        rc, out = run("traversal", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("chunk unparsable", out)

    def test_prereview_with_signoff_fails(self):
        triple(self.dir, "signed", claims=GOOD,
               extra_ej={"signoff": {"by": "x"}})
        rc, out = run("signed", self.dir)
        self.assertNotEqual(rc, 0)
        self.assertIn("signoff", out)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
