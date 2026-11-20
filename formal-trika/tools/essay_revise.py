#!/usr/bin/env python3
"""essay_revise.py — one revision pass that closes the scorecard's failing gaps.

The drafter and the reviser are the same honest machine: the reviser may add
prose, objections and replies, and may re-quote Sanskrit already present in the
draft, but it may not invent a verse, citation or quotation.

  python3 tools/essay_revise.py swarm/essay-*.md --score swarm/essay-*.score.json \
      --enquiry "the crux is esse vs cit" --words 4500 --out swarm/essay-*.rev1.md
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import go_client  # noqa: E402

SYSTEM = """You are revising a scholarly essay on Kashmirian Trika Saivism. You keep every
verbatim Sanskrit quotation and every citation already present. You may add prose,
objections, replies and questions. You may not invent Sanskrit, verses, citations or
quotations. Machine labels ('Exposition:', 'Draft gloss') must disappear."""

PROMPT = """Revise the draft below so it meets the scorecard targets.

FAILING CHECKS TO CLOSE:
{gaps}

TARGETS: words >= {words}; reply moves >= {replies}; Sanskrit quotations >= {sanskrit};
objection moves >= {objections}. Keep at least {secondary} secondary citations in the
form [Author Year, via Kaul 2022].

AUTHOR'S ENQUIRY (the argument the revision must answer):
{enquiry}

RULES
- Preserve every Sanskrit line already in the draft, verbatim. Do not add a verse that
  is not already quoted or cited in the draft.
- Preserve the nine-plus section architecture. Expand sections; do not add new topics.
- Remove all machine seams: no "Exposition:", no "Draft gloss (l3):".
- Give each added objection a real reply, not a summary.
- End with a desideratum paragraph.
- Output the full revised essay only, markdown.

DRAFT:
{draft}
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("draft", type=Path)
    ap.add_argument("--score", type=Path, required=True)
    ap.add_argument("--enquiry", default="")
    ap.add_argument("--words", type=int, default=4500)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--max-tokens", type=int, default=24000)
    a = ap.parse_args()
    text = a.draft.read_text(encoding="utf-8")
    sc = json.loads(a.score.read_text(encoding="utf-8"))
    m = sc["metrics"]
    gaps = ", ".join(sc["gaps"]) or "none"
    prompt = PROMPT.format(
        gaps=gaps, words=a.words, replies=max(20, m["reply_moves"] + 8),
        sanskrit=max(14, m["sanskrit_quotes"] + 4), objections=max(18, m["objection_moves"]),
        secondary=max(8, m["secondary_citations"]), enquiry=a.enquiry or "(none)",
        draft=text)
    try:
        r = go_client.complete(prompt, system=SYSTEM, max_tokens=a.max_tokens, temperature=0.55)
    except go_client.GoError as e:
        print(f"ERROR: revise failed: {e}", file=sys.stderr)
        return 2
    out = r["text"].strip()
    a.out.write_text(out + "\n", encoding="utf-8")
    rec = {"format": "essay-revise-receipt/1", "draft": a.draft.name, "out": a.out.name,
           "date": datetime.date.today().isoformat(), "model": r["model"],
           "fallback_used": r["fallback"], "gaps_in": sc["gaps"],
           "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
           "words_out": len(out.split()), "status": "MACHINE-COMPILED"}
    a.out.with_suffix(".receipt.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(f"revised -> {a.out} ({rec['words_out']} words) | model {r['model']} (fallback={r['fallback']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
