# RENDER-GAP — why bytes/claims checks missed a render bug (2026-11-10)

## The bug (owner-reported, live on svatantrya.net)

Work `ipv` (Īśvarapratyabhijñāvimarśinī (laghvī)) on the reader in
`sa-deva` view rendered:

```
### Pरोवेनन्चे: GRETIL (Iयेर्/Pअन्देय्एद्।) · CC BY-NC-SA 4।0
### Sओउर्चे fइले: 6_सस्त्र/3_फिल्/...txt
```

ASCII metadata transliterated into Devanagari.

## Chain (all verified by repro)

1. `ipv` has no bundled `data/ipv.json` (our bundle is `data/ipvv.json`,
   different id — ipvv-vivrti is a recorded alias gap).
2. Candidate 1/2 (`ipvv-a8u .../layers|translations/ipv.json`) return SPA
   HTML with HTTP 200 → `JSON.parse` throws → treated as absent (correct).
3. Last-resort path: `works-index.json` → `abhinavagupta:ipv` → raw
   `ipvv/site/data/sanskrit/ipv.txt`.
4. File lines 1–3 are `###` headers → paragraph split promoted them to §1.
5. `saWords(sa-deva)` ran `IAST_DEVA.convert()` on them; the converter
   greedily matches Latin keys → "P" passthrough + "rovenance"→रोवेनन्चे.

## Why no existing check caught it

- **Bytes/claim checks** (seo_check, emit --check, verify-pack, red team
  T02–T19): all operate on static claim pages + trace/pack hashes. Claim
  pages are IAST-only and clean — the bug lived in the **reader's dynamic
  render path** fed by a **mutable live source** (by design: canonical-first).
- **Node suites** assert wiring/fingerprints, not rendered glyphs.
- Class: we verified WHAT the data was, never WHAT THE SCREEN SHOWED.

## Fixes (all shipped this session)

1. `extractProvenance()` (app.js): `###` lines, `#Label` + same-line body
   (bodhapancadasika class), and header-only paragraphs pulled out of the
   verse flow at load — for every work, every view. Renders verbatim in a
   Source & licence box (left column only).
2. `IAST_DEVA.convert()` guard: source/licence markers (`#`, Provenance:,
   Source file:, Vendored:, CC BY, GRETIL, *.txt/json/md, respect licence)
   pass through unchanged. Punctuation (`||`) still converts.
3. `data/bodhapancadasika.json`: stripped shipped `# Text  ` marker prefix
   (lane-authored bundle, our file — manifest regenerated).
4. Owner directives: 'Sanskrit text, Devanagari' desc removed; work-title
   dedupe when lane label == page title; width/size controls restyled as
   segmented pills; source box styled.

## New checks (tests/render-integrity.test.cjs, runs in node suite + CI)

- A: property — metadata strings survive `convert()`; real Sanskrit still
  converts; `||` still → danda.
- B: golden — extraction: headers verbatim, no `###` in verses, `# Text`
  split keeps body, converter-identity on extracted lines.
- C: bundle sanitizer — no `data/*.json` ships `#`-leading sanskrit.
  (Caught a real one: bodhapancadasika.)
- D: mixed-script scanner — no latin-letter glued to Devanagari on any
  published claim page (the mangling signature "Pरो").
- Real-data: actual `ipv.txt` from the sibling checkout extracts cleanly
  (skips with reason if checkout absent — CI precedent).

Rule added: **a gate that never renders can never prove rendering is right;
every display transform needs a fixture that runs the transform.**
