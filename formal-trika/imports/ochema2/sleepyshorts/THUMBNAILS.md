# SLEEPY THUMBNAIL STANDARD — 16:9 thumbnails for the 30-60 min longforms

**Data-backed** (blog dataset: 94 channels, 1,879 thumbnails via Vision API,
CLIP + XGBoost — see `blog/data/research/layer2/findings-summary.md` +
`thumbnails-analysis-summary.json`).

---

## 1. THE RULES

| Rule | Evidence |
|------|----------|
| **Designed graphic > photo** | "Animation" +7%, "Graphics" +6% on breakout |
| **1-3 designed words of text** | ESOTERICA breakouts avg 6 words; 1-3 is the sweet spot |
| **No faces (neutral)** | 0.000 XGBoost importance — don't force, don't avoid; topic decides |
| **No book covers / publications** | -10% on thumbnail |
| **High contrast, readable at small size** | standard CTR practice |
| **Title-thumbnail alignment** | CLIP alignment 25-35 (concrete subject ↔ title) |
| **Numbers in thumbnail text** | follows the title rule: avoid |

---

## 2. THE SPEC

- **Format:** 1280x720 (16:9), JPEG, < 300KB.
- **Composition:** a designed graphic from the talk's core visual (the Skia
  mechanism that best encodes the sleepy's spine — we have the whole
  MOTHERFUCKER engine to render it), on the left or center; the text block
  (1-3 words) top-left or bottom, large, high-contrast.
- **Text:** the sleepy's gem-worthy phrase, NOT the full title. Examples:
  - TSC S5 (panel) → "SEVEN THEORIES" + a field/thread graphic
  - levin how-does-it-know S1 → "THE BODY REMEMBERS" + planaria graphic
  - wolfram S2 → "BIGGER BRAINS" + branchial-space graphic
- **The 1-3 words** = the claim, not the topic: "REMEMBERS" over "PLANARIA".
- **No speaker photos, no conference stage shots, no book covers.**
- **Alignment:** the thumbnail must literally show what the title claims (CLIP
  check ≥ 25).

---

## 3. PRODUCTION PATH

1. Pick the sleepy's core visual mechanism (from the talk's block map — the
   mechanism that renders its spine).
2. Render it at 1280x720 via the MOTHERFUCKER pack pipeline (existing
   `render-pack.mjs` / pack.json machinery; landscape mode).
3. Overlay 1-3 words (large, bold, high-contrast, safe-margin aware).
4. Validation: CF vision — does the graphic match the title's subject? is text
   legible? (CLIP proxy).

---

## 4. RELATIONSHIP TO THE SHORTS

The shorts (9:16) reuse the SAME core visual language — a viewer who saw the
short "The Body Remembers What It Would Do" sees the same planaria motif in the
sleepy thumbnail. Series identity: consistent graphic treatment per speaker
(levin = bioelectric field motif, andres = symmetry/valence motif, TSC =
conference-grid motif).
