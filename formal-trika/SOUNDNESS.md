# Soundness position for trika-x / formal-trika
*Status: CANONICAL for this repo. What is claimed, what is not, and what would
change it. (2026-11-17.)*

---

## 1. What we claim

**Non-vacuity, not soundness.** The checker is exercised by 62 hand-written
mutants, each a one-definition corruption that a precisely named proposition
must refute. `tools/must_fail.py` accepts a mutant only when Lean itself reports
that the named proposition is false, and refuses a mutant that fails for any
other reason (a generic compile error is not a pass). This proves one thing: **the
instrument bites.** A formalisation that is wrong in the stated way does not
pass.

What non-vacuity buys: confidence that a passing theorem was genuinely
enumerated or proved inside the stated finite model — not merely not-checked.
What it does not buy: anything about the world, the texts, or the tradition.

## 2. What we do not claim

- **No soundness theorem.** We do not prove that any encoding is true of its
  subject matter.
- **No faithfulness.** We do not prove that the formal objects preserve the
  meanings of the Sanskrit terms they are named after. (Names are labels; the
  EVIDENCE registry pins which passages a row is registered against, and states
  the tier at which the registration holds.)
- **No completeness.** We prove 10% of the passages and claim nothing about the
  rest.
- **No core.** `formalization.json` records `core: 0, frontier: 139+`: every
  theorem is a machine-built frontier row. Nothing has been human-reviewed into
  the core.

## 3. Why the honest alternative to soundness is the named limitation

An axiomatic formalisation can prove soundness against a model it defines — and
thereby inherit whatever the axioms smuggle. A finite-table formalisation cannot
have a non-trivial soundness statement, because there is no semantics to be
sound *with respect to*. Its only honest guarantee is: **the checker refuses
this specific, named wrongness.** Sixty refusals is a discipline, not a proof,
and presenting it as soundness would be the exact inflation this estate exists
to prevent.

## 4. What would change this note

| Claim | What would have to exist | Status today |
|---|---|---|
| Soundness | a stated semantics for each encoding + a proof the checker respects it | missing |
| Faithfulness | an independent mapping (a second encodings team, blind replication) | missing |
| Completeness | 154/154 passages registered | 16/154 |
| Core | named human sign-off per theorem | 0 |

**Rule for anyone building here:** a twin must fail at exactly one named
proposition; a generic compiler error does not count; every twin lives next to
the file it breaks; `control/run.sh` and `recognition/run.sh` enumerate them.
