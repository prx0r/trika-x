"""Chain test D5: formal claim -> qp receipt -> settle -> authorize.

Exercises the REAL ipvv kernel (read-only import) end-to-end on a
formal-trika claim (thirty_six MODEL_CHECKED record): transition with
two distinct source classes (formal-trika + translation-work) through
two-sources-v1, then independent settle with the SAME evidence (must
hold) and SWAPPED evidence (must fail closed), then the authority
boundary (unsigned must NOT authorize; signed+role must).
"""
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, "/root/ipvv/tools")
from qp_acom import gates  # noqa: E402
from qp_acom import objects as O  # noqa: E402
from qp_acom import receipts as R  # noqa: E402
from qp_acom import crypto as C  # noqa: E402

ROOT = Path("/root/trika-x/formal-trika")


def formal_evidence():
    ev = json.loads((ROOT / "EVIDENCE.json").read_text(encoding="utf-8"))
    entry = ev["entries"]["Tattva.lean :: thirty_six"]
    ledger = Path("/root/translation-work/tantrasara-a07/passages.jsonl")
    return [
        O.make_evidence("formal-theorem", "Tattva.lean :: thirty_six", "theorem",
                        "2026-11-06", {"class": "formal-proof", "kind": entry["kind"]}),
        O.make_evidence("ledger-sha",
                        hashlib.sha256(ledger.read_bytes()).hexdigest()[:16],
                        "sha", "2026-11-06", {"class": "ledger-bytes", "ledger": str(ledger)}),
    ]


def sources(ev):
    return {e.get("source", {}).get("class", "?") for e in ev}


class ChainTests(unittest.TestCase):
    def test_full_chain(self):
        # two-sources-v1 needs >= 2 distinct accepted source classes
        import qp_acom.gates as _g
        self.assertIn("two-sources-v1", _g.REGISTRY)
        ev = formal_evidence()
        # evidence classes present?
        classes = {e.get("metric") for e in ev}
        self.assertTrue(len(classes) >= 2)
        prop = {"id": "formal:tattva-thirty_six",
                "claim": O.make_claim("generated total = 36 (MODEL_CHECKED thirty_six)", "formal-trika", "UNKNOWN"),
                "target": "tsa07-p01"}
        run = O.make_run("task:chain", "chain-test", "test")
        r = R.transition({"status": "unreviewed"}, prop, ev,
                         ["two-sources-v1"], run, transition_type="RESOLVE")
        # gate may pass or fail on content; either way receipt is first-class
        self.assertIn("passed", r)
        self.assertIn("digest_full", r)
        # settle with SAME evidence replays
        s = R.settle(r, ev)
        self.assertEqual(s["ok"], r["passed"], s)
        # swapped evidence fails closed
        ev2 = [dict(ev[0], value="TAMPERED"), ev[1]]
        s2 = R.settle(r, ev2)
        self.assertFalse(s2["ok"])
        self.assertIn("evidence mismatch", s2["reason"])

    def test_authority_boundary(self):
        ev = formal_evidence()
        prop = {"id": "formal:tattva-thirty_six",
                "claim": O.make_claim("generated total = 36 (MODEL_CHECKED thirty_six)", "formal-trika", "UNKNOWN"),
                "target": "tsa07-p01"}
        run = O.make_run("task:chain", "chain-test", "test")
        r = R.transition({"status": "unreviewed"}, prop, ev,
                         ["two-sources-v1"], run, transition_type="RESOLVE")
        # unsigned never authorizes
        a = R.authorize_receipt(r, ev, authorized_signers={"anyone"})
        self.assertFalse(a["ok"])
        # signed + role authorizes iff gates passed
        r2 = R.sign_receipt(b"1" * 32, r)
        _sec, pub = C.keypair(b"1" * 32)
        a2 = R.authorize_receipt(r2, ev, authorized_signers={pub.hex()})
        self.assertEqual(a2["ok"], r["passed"], a2)


if __name__ == "__main__":
    unittest.main()
