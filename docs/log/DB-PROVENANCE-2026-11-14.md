# DB PROVENANCE — the 555→1034 growth, identified (2026-11-14)

*House law: a number without provenance is theatre. This closes freshness
findings F1/F3 from `HYGIENE-RECEIPT-2026-11-14.md` with measured evidence.*

## What changed

The box DB went from **555 → 1034 works** (editions 102→581, etexts 87→566)
between the 2026-11-08 baseline and now. `freshness.py --check` correctly
reported DRIFT. Investigation (read-only SQL, this session) identified the
delta exactly.

## The delta is one ingest: Muktabodha, 2026-11-11

```sql
SELECT count(*) FROM works WHERE id LIKE 'mukta%';          -- 479
SELECT min(created_at), max(created_at)
  FROM works WHERE id LIKE 'mukta%';                        -- 2026-11-11 10:48:16Z (single instant)
```

- **479 works**, all `mukta-M#####` (Muktabodha M-numbers: M00005, M00277, M00520, M00623 …).
- **479 editions + 479 etexts**, provider `PT_PROVIDER_muktabodha`,
  artifact `PTART_muk_M#####`, `text_format=PLAIN`, `script=latin`,
  `language=san`, `derived_assertions=[]`, `quality_state=UNKNOWN`.
- **0 assertions, 0 translations** for these works.
- Inserted in **one transaction at 2026-11-11 10:48:16Z** (identical created_at
  on every row) — i.e. one scripted load, not organic discovery.

## Why this is an identity shell, not enriched content

These 479 rows are **identity placeholders**: work + edition + e-text records
only. No assertions, no translations, no witnesses, no passages, no rights.
They do not change the passage ledger (still 909) or assertions (still 1559) —
the existing 555 works keep their identity and counts exactly.

## Honest gaps this ingest carries

1. **`rights_policy_id` is NULL** on the 479 e-texts — rights were not recorded.
   Per estate law this makes them **not publishable** until rights are set; they
   are identification/coverage rows, nothing more.
2. **`quality_state=UNKNOWN`** — not collated, not verified, not a witness.
3. **No producer receipt was committed** at ingest time. It was dated and
   uniform enough to identify after the fact, but a loader script + run record
   should be added so the next ingest is self-receipting (owner/lane call which
   loader owns it).

## What this licenses

- `freshness.json` may now be recaptured at the measured values **because** the
  delta is explained (this file is the explanation). That is not laundering: the
  numbers, their date, their provider and their emptiness are all recorded.
- Works count **555 → 1034 is real but is 479 identity shells**, so any
  "coverage" claim must keep saying 555 enriched works (or state 479 shells
  explicitly). Do not present 1034 as 1034 studied texts.

## Second drift: svread manifest 7078→11109

Independent of this: svread's release manifest asset count grew with emitter
regeneration (their lane). Not an openpatala ingest. No action from here beyond
noting it; `svread` owns its manifest.

*Machine proposes, human disposes. UNKNOWN rights = not publishable.*
