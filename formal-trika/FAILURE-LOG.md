# FAILURE LOG — numbered, with body counts (2026-11-06 onward)

Every entry: what broke, what was reverted/discarded, the rule it produced.
Prose lessons live in PROCESS-NOTES; this file is the count sheet. New
failures append with the next number — never edit a closed entry.

- **F1 (2026-11-06): over-broad twin.** BrokenLadder cycle mutant broke 3
  theorems; `must_fail.py` demands exactly one refusal per file. Rejected;
  split into 3 surgical twins (Chain/Leap/Beyond), all green. Rule: one
  refusal per twin file; law-coupling must be redesigned, not waived.
- **F2 (2026-11-06): bounded-quantifier escape.** Terminal formulated over
  ranks 0–3; mutant (3,4) escaped the bound and passed. Caught pre-run.
  Reformulated pair-quantified. Rule: bounds are claims too — check twin
  escape before running.
- **F3 (2026-11-06): JSON comma surgery doubled a comma.** Script assumed a
  comma-less line-end without asserting. Repaired + revalidated (28 works).
  Rule: assert line-end state before comma surgery.
- **F4 (2026-11-06): branch-artifact drift.** `arrivals.py` read a feature
  branch HEAD as upstream pin (false DRIFT). Rebasing + returned to master.
  Rule: canonical checkout (master) before pins; tool reports branch name.
- **F5 (2026-11-06): premature tal-a15 volume wiring.** Manifest recorded
  for unfinished lane work (their TAL queue runs last). Reverted uncommitted
  (1 file removed, tree left clean). Rule: finished ground first; proposals,
  not wires, for live lanes.
- **F6 (2026-11-06): marker-shape mismatch.** PUSHBACK linker needs
  `[work:target]` brackets without spaces; first draft used prose cites —
  0/15 paras objected across mock + live. Fixed shapes, 1 objection landed.
  Rule: write machine-citable markers from the start; finding: claim tables
  stay UNCITED (linker gap, open item).
- **F7 (2026-11-06): receipt slug collision.** roboscholar runs sharing a
  day-slug overwrote each other's drafts (3 runs, 1 survivor). Fixed with
  UTC HHMMSS slugs. Rule: every receipt id must be unique at write time.
- **F8 (2026-11-06): built-but-uncommitted files.** Scorecard + arrivals
  tool sat untracked for hours across 6 commits (found by status check,
  not by process). Rule: `git status` is part of every commit command —
  no push without reading it.
- **F9 (2026-11-06): conditional line surgery.** A list-comp that
  "preserved" commas dropped one and added another across two EVIDENCE
  inserts (three repair rounds). Rule: build inserted lines as final
  strings, validate the joined STRING before writing (never write-then-
  validate when the file must stay green between runs).
- **F10 (2026-11-06): noisy JSON surgery.** Three failed whole-file
  validations came from over-clever insert scripts, not the data (lines
  parsed individually every time). Rule: simplest possible insert (find
  line, append comma, splice validated lines) — no transforms on the way
  in; F9 validate-before-write held the file safe throughout.
