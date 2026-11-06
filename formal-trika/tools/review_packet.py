#!/usr/bin/env python3
"""review_packet.py — peer-review packets for compiled essays (scholar lane).

Builds one packet per expansion receipt: draft pointer, claim summary,
audit summary, openpatala identity, reviewer checklist, honesty notes.
Packets are what a human reviewer opens; drafts stay machine-proposed
until a decision lands. No backend, no submission — handoff files only.

  python3 tools/review_packet.py --receipt swarm/expansion-*.receipt.json
Writes swarm/review-packets/<slug>.md. Exit 0.
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--receipt", type=Path, required=True)
    a = ap.parse_args()
    r = json.loads(a.receipt.read_text(encoding="utf-8"))
    slug = r.get("essay", a.receipt.stem)
    op = r.get("openpatala", {})
    lines = [
        f"# REVIEW PACKET — {slug}",
        "",
        f"- date: {r.get('date')} | format: {r.get('format')}",
        f"- draft: `swarm/{slug}.md` (machine-compiled, never canonical)",
        f"- owner quotes: {r.get('owner_quotes')} (verbatim) | banked units: {r.get('banked_units')} (R)",
        f"- theorems: {', '.join(r.get('theorems', [])) or 'none cited'}",
        f"- claims: {r.get('claims')}",
        f"- frozen: {len(r.get('frozen_claims', []))} | orphans: {r.get('coverage', {}).get('orphan_bullets')}",
        f"- l3 untraced: {r.get('l3') or 'n/a'} | l4 drifts: {(r.get('l4') or {}).get('drift_paras', 'n/a')}",
        "",
        "## Openpatala identity (how this essay relates to openpatala)",
        "",
        f"- work_id: `{op.get('openpatala_work_id')}` | mapping: {op.get('mapping_status')}",
        f"- record: {op.get('record_status')} `{str(op.get('record_sha256'))[:12]}`",
        f"- edition: {op.get('edition_label')}",
        f"- note: {op.get('note')}",
        "",
        "## Reviewer checklist (human decides; agent triage only)",
        "",
        "- [ ] Quotes verbatim against owner source (spot-check 3)?",
        "- [ ] Each R-claim traceable to its verse premises?",
        "- [ ] Tiers honest (no R promoted, no T without binds)?",
        "- [ ] Formal references registry-checked (not proof claims)?",
        "- [ ] Open questions genuinely open (nothing smoothed)?",
        "- [ ] Witness limits stated (UNPINNED everywhere)?",
        "- [ ] Decision: accept / revise (what) / reject (why)?",
        "",
        "## Honesty notes (from receipts)",
        "",
        f"- {r.get('note', '')}",
        "- Supplied audit sources are argmap excerpts (R-grounds), not authenticated bundles.",
        "- Verdicts here are machine-proposed until a human signs.",
        "",
    ]
    outdir = HERE / "swarm" / "review-packets"
    outdir.mkdir(exist_ok=True)
    (outdir / f"{slug}.md").write_text("\n".join(lines))
    print(f"packet -> swarm/review-packets/{slug}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
