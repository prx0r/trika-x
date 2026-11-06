# VIDEO TEMPLATES — How to Make a Good Film

The two GOOD films (corbin-world-between-worlds, stones-are-watching)
prove the pipeline. This is the structure they used, extracted as a
reusable template. The film-pack template lives in
`imports/film-packs/` (blueprint + visual program + source essay).

## THE STRUCTURE (from the working films)

```
ESSAY (source_essay.md)
  ↓ exact prose quoted as narration
STORYBOARD (storyboard.json/csv — 102 narration-locked shots, 5-10s each)
  ↓
VISUAL PROGRAM (visual_program.json):
  ├── visual_thesis    ← one sentence: what the film shows
  ├── palette          ← 5 colors, fixed
  ├── entities         ← the persistent objects (id, archetype, continuity)
  ├── operators        ← the transformations (reveal, mediate, mirror, bridge...)
  └── shots            ← each: id, start/end, spoken_text, mode, events
  ↓
RENDER (render script) → clips → concat → full film
  ↓
VALIDATE (uniqueness gate: check-uniqueness.py)
```

## THE RULES (what makes it GOOD, not template)

1. **Every shot has a spoken_text** — the narration is locked first,
   the visuals serve it. The 27 NOT-GOOD renders had no essay
   driving them; the GOOD films are essay-first.
2. **The visual program is per-film** — a visual THESIS, a palette,
   entities with continuity, operators that TRANSFORM the entities.
   Never a shared template with different titles.
3. **Entities transform** — the world-between-worlds film is one
   threshold that becomes eye → north → Guide → thread → face →
   fire → bridge → portal. That transformation IS the film. A
   template has no transformation.
4. **Operators are the vocabulary** — reveal, mediate, orient,
   embody, illuminate, connect, cut, rejoin, mirror, radiate,
   ascend, burn, bridge, reciprocate, interiorize. These are the
   film's grammar (matches the 50-essay companion's visual
   grammar: field, aperture, partition, bridge, fork...).
5. **Palette is fixed and small** — paper/ink/porphyry/lapis/gold.
   The visual identity comes from the palette, not from complexity.

## THE PIPELINE (essay → film)

1. **Write the essay** (what-the-heck-is format, from a claim file
   and the 50-essay companion's structure).
2. **Extract the narration** — the essay's own prose, quoted exactly.
3. **Write the storyboard** — one shot per paragraph/claim, 5-10s.
4. **Design the visual program** — thesis, palette, entities,
   operators, per-shot events. THIS IS THE UNIQUENESS STEP.
5. **Render** via the essayviz core / render scripts (the 600+ in
   the material library are the reference for how concepts render).
6. **Gate it** — check-uniqueness.py must pass (0% shared frames
   with other films, enough distinct looks per film).
7. **Assemble** in FableCut, add narration audio, publish.

## THE MATERIAL LIBRARY

The 600+ render scripts (tantraloka/goldrender + moderngl + platinum
+ clean queues) encode the concepts as visual programs. For a new
film: find the concept's script, study its visual moves, design a
NEW visual program for the NEW essay. Copy the grammar, never the
renders.

## THE FIRST TARGETS (essays with the research base ready)

1. **The Subtle Body** — research base complete (corrected-position,
   three-body decomposition, resolution reading). Essay →
   storyboard (the three bodies as three visual programs: form /
   regulation / image) → film.
2. **Essay 01–05 of the 50-essay companion** — the manifestness
   block. Visual grammar already specced (field, aperture,
   partition, bridge, missing edge).
3. **The Tetrahedron** — the essay already exists
   (essayviz-workspace/what-the-heck-is-tetrahedron.md) and the
   math pack exists (packs/math/). The shortest path to a GOOD
   film.

## THE PRODUCTION SKILL (the actual tool)

The primary film builder is the **ochema-vid** skill:
`/mnt/HC_Volume_106427611/ochema/skills/ochema-vid/SKILL.md` (+
`references/mechanism-routing.md`, `references/commands.md`).

**Skill hierarchy:**
- `ochema-vid` — PRIMARY. End-to-end essay→film: argument IR →
  continuity systems → 3+ candidates/beat → selection → scene pack →
  narration → review frames → render → mux → shorts extraction
  (hook/turn/proof/close, 9:16) → process notes.
- `tantraloka-film` (hermes/skills/) — Tantrāloka content production
  (made the GOOD film-packs). Same discipline, 6 style packs.
- `publish-video-fablecut` — post-production only (timeline, export,
  site integration) after an MP4 exists.

**The readiness audit** (`ochema/essayvizport.d/11-OCHEMA-VID-READINESS-AUDIT.md`)
already names the first essay queue with their packs:
intelligence, feeling, rasa, loop-quantum-gravity, merkabah,
walter-russell.

**Why the 27 renders failed:** the batch renderer (render-all.mjs)
bypassed ochema-vid entirely — no argument IR, no candidate
selection, no uniqueness gate. The skill IS the quality control; the
batch skipped it.
