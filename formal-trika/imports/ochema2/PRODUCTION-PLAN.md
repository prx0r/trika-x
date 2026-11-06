# PRODUCTION PLAN — High-Quality Content via Hermes

**Version 1.0 — 2026-08-04.** The only goal: produce high-quality
content using Hermes, enabling the automation plans. This document
inventories what we already have that is high quality, and maps the
path from research → essay → film → publish.

---

## 1. WHAT WE HAVE THAT IS HIGH QUALITY (the starting inventory)

### 1.1 Complete, unique films (GOOD — verified)

| Film | Length | What it is | Where |
|---|---|---|---|
| **The World Between Worlds** | 639s (10.7 min) | Corbin's imaginal world — 102 narration-locked shots, threshold→eye→Guide→bridge transformation | `clean/MOTHERFUCKER/film-packs/corbin-world-between-worlds/` |
| **The Stones Are Watching You** | 697s (11.6 min) | Stones as observers — unique visuals, verified 0% shared | `clean/MOTHERFUCKER/film-packs/stones-are-watching/` |
| **The Infinite Learned** | 44-shot film | Full pack: MP4, storyboard, visual program, validation | `clean/MOTHERFUCKER/infinite_learned_film_pack/` |
| **Song with No Singer** | 88-scene film | Dependent origination + memory + recognition | `clean/MOTHERFUCKER/song-no-singer-delivery/` |

These four are the PROOF: the pipeline produces unique long-form
films. They are the templates AND the first publishable content.

### 1.2 The PIL material library (the unique visuals — 276 files, 6385 scenes)

**`clean/MOTHERFUCKER/pillywilly/pil/` — 299 PIL video renderers**,
the unique original visuals. The audit (`pil-audit.json`) found:
- 6385 scenes across 276 files
- 1022 unique visual-registry keys
- Clustered: radial-and-generative (255), observer-and-recognition
  (169), field-and-transformation (137), nested-scale (120),
  sequence-and-time (100), boundary-and-selection (68),
  quantitative (56), network (32)

**These are the original content.** They are the crown jewels the
user remembers: "loads of length PIL files that are good original
content." They are NOT yet films — they're scene functions trapped
in scripts — but they are the unique visual vocabulary, and the
converter exists to import them.

### 1.3 The essay base (ready-to-film content)

The what-the-heck-is essays (sobered v1.32.2) — the readiness audit
names the first six: intelligence, feeling, rasa, loop-quantum-
gravity, merkabah, walter-russell. Plus the 50-essay companion's
specs. Plus the subtle-body research base (the most complete).

---

## 2. THE PIL → SKIA CONVERTER (the spec exists — the work is partial)

**The user's memory is correct: we spec'd it.** The full import spec
is `clean/MOTHERFUCKER/extensionpacks/CAPABILITY-PACK-ARCHITECTURE.md`:

**The classification rule** — every imported PIL idea gets exactly
one type: kernel infrastructure / style token / primitive /
mechanism / parameter / preset / worked example / reject.

**The mining passes:**
- **Pass A** — remove duplicated infrastructure (backgrounds, fonts,
  borders, FFmpeg = kernel concerns, not ported)
- **Pass B** — extract style into theme tokens
- **Pass C** — fingerprint every scene (claim, relation, source/
  target state, preserved invariant, marks, temporal change,
  misreading, domain)
- **Pass D** — deduplicate (same fingerprint → preset; new topology →
  new mechanism)
- **Pass E** — implement native Skia (visual middle layer only)
- **Pass F** — register + prove (manifest, provenance, tests, demo,
  render t=0/0.5/0.72/1.0)

**The acceptance gates** (a mechanism joins the library only if all
pass): correspondence, motion proof, caption independence, parameter
bounds, style independence, determinism, resolution, continuity,
provenance, novelty.

**The current state (what's ported):**
- **39 mechanisms live** in capability-packs: human-anatomy (9),
  invariant-composition (12), neurocognition (8), pathkit-geometry
  (3), yogic-subtle-body (7) — plus 13 more pack skeletons with 0
  mechanisms (base, tantric-cosmology, tantric-geometry, systems-
  dynamics, scientific-diagrams, data-visualization,
  comparative-epistemology, textual-scholarship, temporal-processes,
  embodied-phenomenology, intelligent-others, particle-fields,
  audio-reactive)
- The **platinum science inventory** (24 files, 371 scenes, 40
  visual-registry keys, 8 clusters) — the mining output, but
  mechanisms: 0 → **the mining was done, the porting was not**

**The gap:** the PIL visuals are AUDITED but not PORTED. 1022 visual
registry keys exist as PIL functions; 39 mechanisms exist as Skia.
The converter spec tells us exactly how to bridge them; the work is
mechanical (fingerprint → classify → implement → prove).

---

## 3. THE AUTOMATION PATH (hermes → content)

### The stack (all exists)

```
CONTENT        research docs (frontier, rasa, subtle body, essays)
     ↓
ESSAY          what-the-heck-is format (ochema2 claim-file discipline)
     ↓
FILM           ochema-vid skill (PRIMARY — argument IR → candidates →
               selection → pack → render → mux → shorts)
               ↑ tantraloka-film for Tantrāloka content
     ↓
ASSEMBLY       publish-video-fablecut (storyboard → voiceover → art →
               subtitles → FableCut timeline → export)
     ↓
PUBLISH        ochema-site pipeline (manifest + quality badges)
               + check-uniqueness.py GATE (must pass before publish)
```

### The three tracks

**Track A — Port the PIL library (the uniqueness engine).**
Run the mining → porting passes on the 299 PIL files. Target: the
1022 visual keys become ~150-250 Skia mechanisms across the 13 empty
pack skeletons. This is the highest-leverage work: it converts the
unique original content into the reusable vocabulary that makes every
future film GOOD. The acceptance gates make it deterministic.

**Track B — Publish the four GOOD films now.**
The World Between Worlds + The Stones Are Watching You (already on
R2, already in the site manifest as GOOD) + The Infinite Learned +
Song with No Singer. These are publishable TODAY. Add the latter two
to R2 + manifest, verify with the uniqueness gate, publish.

**Track C — The first new films from the essay queue.**
The subtle body (research base complete) or the tetrahedron (essay +
math pack exist) or essay 01–05 (spec complete). Run through ochema-
vid end-to-end: essay → argument IR → continuity → candidates →
selection → pack → render → gate → shorts → publish.

### The automation loop (once Track A is done)

```
1. Pick essay from the queue (readiness audit or 50-essay companion)
2. Hermes: ochema-vid skill — full production order (15 steps)
3. Hermes: publish-video-fablecut — assembly + export
4. GATE: check-uniqueness.py must pass (unique visuals, enough looks)
5. Publish to site (manifest + badges)
6. Extract shorts (hook/turn/proof/close, 9:16)
7. Repeat
```

The automation plans depend on the pipeline being deterministic —
which is exactly what the MOTHERFUCKER framework (deterministic Skia,
seed-controlled) + the acceptance gates (determinism required) + the
uniqueness gate (verified) provide.

---

## 4. THE WORK ORDER (what to do first)

1. **Publish the 4 GOOD films** (hours, no new work — they exist)
2. **Port the PIL library** (the main effort — mining is done, the
   porting passes A–F on 299 files, starting with the 255
   radial-and-generative + 169 observer-and-recognition clusters,
   which cover most of the Tantrāloka's visual content)
3. **First new film from the queue** (subtle body or tetrahedron —
   proves the loop end-to-end)
4. **Automate the loop** (queue → essay → film → gate → publish)

---

## 5. THE PRODUCTION SKILLS (reference)

- **ochema-vid** (PRIMARY): `/mnt/HC_Volume_106427611/ochema/skills/ochema-vid/SKILL.md`
- **tantraloka-film**: `/root/.hermes/skills/tantraloka-film/SKILL.md`
- **publish-video-fablecut**: `/root/.hermes/skills/publish-video-fablecut/SKILL.md`
- **The framework**: `/root/projects/clean/MOTHERFUCKER/` (AGENT-GUIDE.md,
  CAPABILITY-PACK-ARCHITECTURE.md, agent-guide/docs/01-08)
- **The PIL library**: `/root/projects/clean/MOTHERFUCKER/pillywilly/pil/` (299 files)
- **The audit**: `pillywilly/pil-audit.json` (6385 scenes, 1022 keys)
- **The mining spec**: `extensionpacks/CAPABILITY-PACK-ARCHITECTURE.md`
- **The essay queue**: `ochema/essayvizport.d/11-OCHEMA-VID-READINESS-AUDIT.md`
- **The 50-essay roadmap**: `tantraloka/notes/frontier_50_essay_research_companion.md`
