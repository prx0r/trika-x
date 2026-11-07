#!/usr/bin/env python3
"""federation_pretest.py — static pre-tests for the federated MCP contract.

No live servers, no DB, no network. Checks the checked-in state:
(a) prefixed tool-name uniqueness, (b) banned-substring scan over tool names
+ server source files, (c) FailOpen routing pure function, (d) identity
contract block (UNRESOLVED -> draft-only). EXIT 0 = contract holds.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Expected federated surface (specs + existing servers). Children not yet
# landed keep their spec'd names here so the test stays valid on arrival.
EXPECTED = {
    "openpatala": ["openpatala__resolve", "openpatala__bundle",
                   "openpatala__search", "openpatala__coverage"],
    "translation": ["translation__works", "translation__work",
                    "translation__passages", "translation__coverage",
                    "translation__ids", "translation__proof"],
    "scholar": ["scholar__passage_evidence", "scholar__audit_draft",
                "scholar__link_claims", "scholar__pushback",
                "scholar__resolve_ref"],
    "book": ["book__inspect", "book__quote", "book__verify"],
    "video": ["video__plan", "video__gates"],
    "formal": ["formal__bridge", "formal__evidence", "formal__table",
               "formal__gaps", "formal__runs", "formal__axioms"],
}

BANNED_EXACT = {"ship", "render", "seal", "publish", "send", "spend",
                "post", "isbn", "isbn_issue", "grant_rights", "signoff",
                "submit"}
BANNED_PREFIX = tuple(b + "_" for b in BANNED_EXACT) + tuple(
    b + "-" for b in BANNED_EXACT)


def banned_name(name: str) -> str | None:
    """Check a bare tool name (no child prefix). Returns the matched ban."""
    base = name.split("__")[-1]
    if base in BANNED_EXACT:
        return base
    for p in BANNED_PREFIX:
        if base.startswith(p):
            return p.rstrip("_-")
    return None

SCAN_FILES = [
    ROOT / "PARENT-CONTRACT-SPEC-2026-11-07.md",
    ROOT / "FORMAL-MCP-SPEC-2026-11-07.md",
    pathlib.Path("/root/svread/mcp/scholar_server.py"),
    pathlib.Path("/root/openpatala/patala/mcp_server.py"),
]


def check_unique() -> list[str]:
    seen: dict[str, str] = {}
    problems: list[str] = []
    for child, tools in EXPECTED.items():
        for t in tools:
            if not t.startswith(child + "__"):
                problems.append(f"prefix: {t} does not start with {child}__")
            if t in seen:
                problems.append(f"collision: {t} in {seen[t]} and {child}")
            seen[t] = child
    return problems


def check_banned() -> list[str]:
    import re
    problems: list[str] = []
    for t in [t for tools in EXPECTED.values() for t in tools]:
        hit = banned_name(t)
        if hit:
            problems.append(f"banned tool name: {t} (action {hit!r})")
    for f in SCAN_FILES:
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            problems.append(f"unreadable scan file: {f}")
            continue
        for m in re.finditer(r"\('([a-z_0-9]+)'|\bdef ([a-z_0-9]+)\b", text):
            name = m.group(1) or m.group(2)
            if len(name) < 3 or name.startswith(("test_", "check_")):
                continue
            hit = banned_name(name)
            if hit:
                problems.append(f"banned in {f.name}: {name} (action {hit!r})")
    return problems


def route(tool: str, down: set[str]) -> str:
    """Pure routing model: prefix -> child; down child -> FailOpen rest."""
    child = tool.split("__", 1)[0] if "__" in tool else ""
    if not child or child not in EXPECTED:
        return "Unknown tool"
    if tool not in EXPECTED[child]:
        return "Unknown tool"
    if child in down:
        rest = [c for c in EXPECTED if c not in down]
        return "ERROR: all targets down" if not rest else f"FailOpen: {child} down, serving {len(rest)} rest"
    return f"route:{child}"


def check_routing() -> list[str]:
    problems: list[str] = []
    if route("formal__gaps", set()) != "route:formal":
        problems.append("healthy route failed")
    if "FailOpen" not in route("book__quote", {"book"}):
        problems.append("single-down should FailOpen to rest")
    if route("book__quote", set(EXPECTED)) != "ERROR: all targets down":
        problems.append("all-down should error")
    if route("book__ship", set()) != "Unknown tool":
        problems.append("ship must be Unknown tool")
    if route("video__render", set()) != "Unknown tool":
        problems.append("render must be Unknown tool")
    if route("whatever", set()) != "Unknown tool":
        problems.append("unprefixed must be Unknown tool")
    return problems


def contract_status(openpatala_work_id: str | None) -> str:
    if not openpatala_work_id or openpatala_work_id in ("UNRESOLVED", "TBD"):
        return "draft-only"
    return "gated (still needs gates + human)"


def check_contract() -> list[str]:
    problems: list[str] = []
    if contract_status("UNRESOLVED") != "draft-only":
        problems.append("UNRESOLVED must be draft-only")
    if contract_status(None) != "draft-only":
        problems.append("missing id must be draft-only")
    if contract_status("tantrasara") == "draft-only":
        problems.append("resolved id must not be draft-only")
    return problems


def main() -> int:
    failures: list[str] = []
    for label, fn in (("prefix", check_unique), ("banned", check_banned),
                      ("routing", check_routing), ("contract", check_contract)):
        ps = fn()
        print(f"{label}: {'PASS' if not ps else 'FAIL (' + str(len(ps)) + ')'}")
        for p in ps:
            print(f"  - {p}")
        failures.extend(ps)
    print(f"federation_pretest: {'GREEN' if not failures else 'RED'} "
          f"({sum(len(v) for v in EXPECTED.values())} expected tools)")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
