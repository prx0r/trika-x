# PORTRAIT ENGINE — HANDOFF FOR CHATGPT

**Repo:** github.com/prx0r/clean · branch `main` · commit `e1ce0ef`
**Scope:** MOTHERFUCKER Skia engine → native 1080×1920 shorts (the sleepyshorts product line)
**Gold benchmark:** the PIL platinum `.py` files (self-contained procedural films, e.g. `/root/projects/clean/queue2/body_remembers_shape_platinum.py`) — we must match that quality.

---

## 1. WHAT WAS BUILT (committed, tests green, landscape byte-identical)

The core bug was a rubber-sheet transform in `primitives.mjs`:
`ctx.setTransform(width/1280, 0, 0, height/720, 0, 0)` — anisotropic stretch. A 1080×1920 render stretched the 1280×720 world vertically ~3×.

**The fix — two logical worlds + uniform scale:**

- `MOTHERFUCKER/layout.mjs` (NEW):
  - `logicalViewport(width, height, orientation?)` → `{orientation:"portrait",width:720,height:1280}` when `height > width` (or explicit), else `{orientation:"landscape",width:1280,height:720}`.
  - `setLogicalTransform(ctx,w,h)` → **uniform** scale `min(w/vw, h/vh)`, centered. Never independent X/Y stretching.
  - Topology helpers (landscape branch reproduces legacy coords exactly; portrait reflows vertically):
    `stage`, `center`, `pair`, `triplet`, `comparison`, `hub`, `nested`, `axis`, `journey`, `body`.
    E.g. `pair(view)` = side-by-side in landscape, B-above-A in portrait.
- `theme.mjs`: added `PORTRAIT_LOGICAL_WIDTH/HEIGHT` (720×1280); landscape constants untouched.
- `primitives.mjs`: `createStableBackground`/`drawBorder` are viewport-aware (landscape = exact legacy numbers, byte-identical output); `drawFooter` disabled in portrait (karaoke captions own that band).
- `renderer.mjs`: computes `env.viewport` and threads it into every motif; `drawBorder(ctx, theme, alpha, viewport)`.

**Mechanism migration pattern** (per mechanism, in `semantic-visuals.mjs`, `systems-visuals.mjs`):
```js
const view = env.viewport ?? { orientation:"landscape", width:1280, height:720 };
const portrait = view.orientation === "portrait";
const { x: cx, y: cy } = center(view, { x: 640, y: 290 }); // landscape = exact original
```
- Category A (radial/centered: lotus, orb, field, rings, chakras) → `center()` + radii scaled by `view.width/1280`.
- Category B (A→B, A→B→C, left/right, comparison) → `pair()`/`triplet()`/`comparison()` → vertical stack in portrait.
- Rows (5 lenses, grids) → vertical stacks down `0.18H→0.84H`.

**Verified:**
- All 31 base mechanisms (15 semantic-visuals + 16 systems-visuals) are **pixel-identical in landscape** (0 diffs vs pre-change renderer, PIL compare every 2nd px).
- Native portrait 1080×1920 renders work; content centered (dark-pixel centroid x≈540, y 700–1250).
- All tests green (`node --test tests/`).

**shorts-v2 pipeline:**
- `shorts-v2/runtime/*` (34 `portrait-*` mechanisms) migrated to `env.viewport` (helpers.mjs: `whiteStage(view)`, `portraitBodyParams(scene,view)` — body scale `≈H*0.74/350` so anatomy fills the portrait world; `viewLayout(env)` gives CX/CY/sr helpers).
- `shorts-v2/tools/render-short-v2.mjs`: mechanism scenes now render **directly at 1080×1920** (native), crop path kept only for legacy-landscape scenes. Pack: `render:{width:1080,height:1920,orientation:"portrait"}` + image beats (Ken Burns) unchanged.

---

## 2. END-TO-END TEST STATE (levin g06 "The Body Remembers", 130s gem)

Test pack `/tmp/opencode/g06-native.json`: 6 real-image beats + 4 native portrait mechanisms (constraint-field, recognition-transaction, dependency-network, multiscale-agent). Image paths mapped to `/root/projects/ochema2/sleepyshorts/_visuals/`.

**6/10 scenes rendered natively at 1080×1920** (~1 min/scene, so a full short ≈ 10–12 min). Then a **DEADLOCK**:

**BLOCKER 1 — `portrait-dependency-network` (s07) hangs the render pipe.**
- Raw video stops growing mid-write; the ffmpeg subprocess idles at ~0 CPU; `renderVideo` waits forever (the `stream.write → once('drain')` pump never resolves). s03 constraint-field and s05 recognition-transaction render fine; only this mechanism deadlocks.
- Likely suspects: something in the mechanism (heavy `seededRandom` loop? a canvas op that never returns at 1080×1920?) OR the frame pump. NOT reproduced at poster (single-frame) resolution — only during a long `renderVideo` run.
- Debug so far: killed at ~262KB of a 14s raw. Need: run the mechanism in isolation, add progress logging, find the exact frame where it stalls.

**BLOCKER 2 — corrupt image assets.**
- Half the `_visuals/` planaria images are 2KB stubs that ffmpeg can't decode (`No JPEG data found`). With `-loop 1` they make ffmpeg spin forever. Corrupt: `planaria_bdellocephala.jpg`, `planaria_neoblasts.jpg`, `Bdellocephala_punctata.jpg`, `A_Planarian_neoblasts__...jpg`. Valid ones: `planaria_kempi.jpg`, `planaria_torva_eye.jpg`, axolotl set, `bioelectric_patterns.png`, `neuron_*`, `xenopus_development.jpg`.
- The pipeline needs a pre-flight image validator (probe each beat's `media.src` before render) so a corrupt asset fails fast instead of hanging.

---

## 3. OPEN QUESTIONS FOR YOU (ChatGPT)

1. **The s07 deadlock** — best debugging approach / likely root cause? (renderVideo pipe pump vs a specific Skia op vs the mechanism.)
2. **Speed** — ~1 min/scene at 1080×1920 (24fps, medium x264). Mechanisms are the cost. Is there a cheap win (render 1280×2560 logical then scale? presets? batching?)? PIL `.py` files render comparable frames much faster.
3. **Benchmark gap** — the PIL files read as *denser, richer, more cinematic* (procedural fill, layered palettes, full-frame composition). The MOTHER mechanisms are clean-but-sparse. To match PIL quality in portrait, which levers matter most: composition density, color, motion, or just better scene selection?
4. **Artisan scripts** — `shorts-v2/artisan/wolfram-bach-artisan.mjs` + `andres-substrate-artisan.mjs` still use hardcoded `W=1280,H=720` and are NOT migrated. Worth migrating, or abandon for the image-first + base-mechanism approach?
5. **Is the two-world logical viewport the right call**, or should we add a `portraitStrategy` field per mechanism (radial/vertical-pair/vertical-triplet/body/axis/journey/legacy-landscape) as the spec originally suggested, so unmigrated packs degrade gracefully (letterboxed) instead of breaking?
6. **The footer-off decision** — portrait renders have no title/subtitle chrome (karaoke captions own the bottom). Good or should there be a minimal title plate in the first/last beat?

---

## 4. NEXT STEPS (my plan unless you advise otherwise)

1. Diagnose + fix `portrait-dependency-network` deadlock (isolate frame count).
2. Add asset pre-flight validation to `render-short-v2.mjs` (reject corrupt images up front).
3. Finish g06 render → mux `gems/g6_body_remembers.mp3` + `g6_subs.ass` (karaoke) → a finished native short.
4. Side-by-side benchmark vs `body_remembers_shape_platinum.py` scene renders (objective fill/ink stats + human look).
5. Decide artisan migration vs image-first per your advice in Q4.
