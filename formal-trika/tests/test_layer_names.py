#!/usr/bin/env python3
"""test_layer_names.py — internal codes <-> public names stay honest."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from layer_names import codes, describe, publics, to_internal, to_public


class TestLayerNames(unittest.TestCase):
    def test_roundtrip_all(self):
        for code in codes():
            public = to_public(code)
            self.assertEqual(to_internal(public), code)
            self.assertEqual(to_internal(code), code)

    def test_case_and_separator_tolerance(self):
        self.assertEqual(to_internal("Literal-Gloss"), "L0")
        self.assertEqual(to_internal("literal_gloss"), "L0")
        self.assertEqual(to_internal("  l0 "), "L0")
        self.assertEqual(to_internal("Argument Map"), "ARGMAP")
        self.assertEqual(to_internal("song"), "L4")
        self.assertEqual(to_public("c2"), "register-render")

    def test_fail_closed(self):
        for bad in ["", "  ", "L5", "gloss", "translation", None, 0]:
            with self.assertRaises(ValueError):
                to_internal(bad)
        with self.assertRaises(ValueError):
            to_public("L9")

    def test_codes_stable(self):
        # Internal codes are load-bearing: this list may only grow by
        # appending with a schema major bump, never by rename/reorder.
        self.assertEqual(codes(), ["SOURCE", "T1", "L0", "ARGMAP", "L2",
                                  "C1", "C2", "L3", "L4"])

    def test_comments_present(self):
        for code in codes():
            d = describe(code)
            for key in ("code", "public", "label", "blurb", "comment"):
                self.assertTrue(d.get(key), f"{code} missing {key}")

    def test_publics_unique(self):
        self.assertEqual(len(set(publics())), len(publics()))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
