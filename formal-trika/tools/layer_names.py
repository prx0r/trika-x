#!/usr/bin/env python3
"""layer_names.py — internal codes <-> public names for translation layers.

Internal codes (T1, L0, ARGMAP, L2, C1, C2, L3, L4, SOURCE) are load-bearing:
validators, gates, ledgers, packs, lingua and the essay compiler key on them.
Callers should never have to say 'l0' — resolve through here.

  to_public('L0')               -> 'literal-gloss'
  to_internal('literal-gloss')  -> 'L0'
  to_internal('L0')             -> 'L0'   (codes pass through)
  describe('c2')                -> {code, public, label, blurb, comment}

Matching is case-insensitive; '-'/'_'/whitespace are equivalent. Unknown
names raise ValueError (fail-closed — never guess a layer).
"""
from __future__ import annotations

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "layer-names.json"


def _load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def _norm(s: str) -> str:
    return "".join(ch for ch in s.strip().lower() if ch.isalnum())


def _index() -> tuple[dict, dict, dict]:
    doc = _load()
    by_code, by_public, full = {}, {}, {}
    for layer in doc["layers"]:
        code = layer["code"]
        full[code] = layer
        by_code[_norm(code)] = code
        by_public[_norm(layer["public"])] = code
        by_public[_norm(layer["label"])] = code
    return by_code, by_public, full


def to_internal(name: str) -> str:
    """Any caller-facing name or internal code -> canonical code. Fail-closed."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("empty layer name")
    by_code, by_public, _ = _index()
    key = _norm(name)
    if key in by_code:
        return by_code[key]
    if key in by_public:
        return by_public[key]
    raise ValueError(f"unknown layer: {name!r}")


def to_public(code: str) -> str:
    """Canonical code -> public slug. Fail-closed."""
    _, _, full = _index()
    if not isinstance(code, str):
        raise ValueError("empty layer code")
    key = code.strip().upper()
    if key in full:
        return full[key]["public"]
    # accept a public name and normalise it
    return full[to_internal(code)]["public"]


def describe(name: str) -> dict:
    """Full record {code, public, label, blurb, comment} for docs/errors."""
    _, _, full = _index()
    return dict(full[to_internal(name)])


def codes() -> list[str]:
    _, _, full = _index()
    return [layer["code"] for layer in _load()["layers"]]


def publics() -> list[str]:
    _, _, full = _index()
    return [layer["public"] for layer in _load()["layers"]]
