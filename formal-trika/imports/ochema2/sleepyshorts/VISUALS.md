# SHORT VISUALS STANDARD — 9:16 shorts from gem audio

**Applies to:** every `gems/*.mp3` → finished vertical YouTube Short.
**Key difference from the essay-TTS pipeline:** our gems are the SPEAKER'S REAL
VOICE. No TTS, no dual-voice. Subs are ground-truth from the VTT word stamps.

---

## 1. THE RULES (from the essay→short handover + our flow)

1. **Karaoke subs at the BOTTOM** — `margin_v = 0.10*H`, bold sans (Arial
   Black 72), heavy stroke + shadow, per-word active highlight.
2. **Ground-truth caption text, never whisper-transcription** — the VTT word
   stamps of the gem window ARE the timing; no re-transcription needed. (Mangled
   terms in auto-captions are cleaned by hand in the caption text — timing
   stays.)
3. **No repeated images** — every beat visually distinct (CF vision holistic
   check + pixel-diff).
4. **Visuals must match the claim** — decide what each beat NEEDS before
   searching (the image-requirements discipline).
5. **THE SOURCING DECISION (2026-08-09, after review):**
   - **Abstract/conceptual claims → RENDER ENGINE** (the default). The 26
     `shorts-*` mechanisms from `clean/MOTHERFUCKER` via `render-short.mjs`
     (1080x1920, white bg). Deterministic, unique (zero repeat risk across all
     gems), brand-consistent, no sourcing. Concept→mechanism map: memory →
     `short-memory-consolidation`/`short-causal-memory`, self/identity →
     `short-recognition-transaction`/`short-polyphonic-identity`, field/unity →
     `short-semantic-transition`, transformation → `short-transformation-
     invariance`, geometry → `short-lotus-unfold`/`short-yantra-construction`,
     breath/body → anatomy pack.
   - **Concrete empirical claims → CURATED IMAGE POOL** (planaria, worm,
     embryo, frog leg, brain, xenobots...). Build each topic's pool ONCE (a
     handful of high-res verified images per topic in `sleepyshorts/_visuals/`),
     CF-vision-verify ONCE, reuse across the talk's gems. No per-gem ad-hoc
     web searching.
   - **The mix is ideal**: real image beat(s) + mechanism beat(s) within the
     same gem (concrete setup → abstract payoff).
6. **1080x1920, Ken Burns, `contain` on white**, gentle zoom ≤1.12, focus on
   the subject (`focusX/focusY` — CF vision locates it).
7. **Re-encode crf 23-26** — keep < ~20MB.

> **Source-video clips (the real-talk route): BLOCKED as of 2026-08-09.**
> yt-dlp resolves formats (720p max) but media segments 403 and alt clients are
> bot-checked. When a fresh cookie export works again, lecture gems should use
> the ACTUAL video window of the speaker (cut via `--download-sections`) — the
> most relevant possible visual. Re-test before every batch.

---

## 2. THE PIPELINE

### Step 1 — word timing from the VTT (no whisper)

Extract the gem's word tokens from `talk.en.vtt` within the gem's source
windows; for STITCHED gems, concatenate windows and offset each window's
timestamps by the removed gap.

```python
import re, json
vtt = open('talk.en.vtt').read()
tokens = []  # (ms, word)
for m in re.finditer(r'<(\d\d:\d\d:\d\d\.\d\d\d)><c>\s*(.*?)\s*</c>', vtt):
    t = m.group(1); h,mm,s = t.split(':'); ms = (int(h)*3600+int(mm)*60+float(s))*1000
    tokens.append((ms, m.group(2)))
# keep tokens inside window(s), apply stitch offsets, then build whisper-format:
words = [{"word": w, "start": s/1000, "end": (s+400)/1000} for s, w in window_tokens]
json.dump({"segments":[{"words": words}]}, open('words.json','w'))
```

(400ms per-word duration is a fallback; the VTT gives word starts only — if the
caption has word ENDS (some tracks do), prefer those.)

### Step 2 — karaoke .ass

```bash
python3 karaoke_ass.py words.json --mode per-word --out subs.ass --sidecar subs.srt
```

### Step 3 — image requirements (per beat, from the claim)

Write what each beat NEEDS (subject, NOT-something) before searching. Sources
in order:
1. **Web search** (Wikimedia `Special:MediaSearch` via webfetch) — the default
2. **Local corpus** — `blog/content/sources/...`, `blog/public/thumbnails/...`
3. **R2** — `r2:sacred-art/`, `r2:essayviz-videos/`
4. **Mechanism render** — for abstract claims (valence, self, field): the 26
   `shorts-*` mechanisms from `clean/MOTHERFUCKER` (render-short.mjs, 1080x1920,
   white bg) — pick by concept (see shorts-from-essay SKILL §DIAGRAM RENDER).

### Step 4 — beats → Ken Burns

```json
{ "width": 1080, "height": 1920, "fps": 24, "scenes": [
  { "image": "/abs/beat1.jpg", "duration": <secs>, "motion": "zoom_in",
    "zoomStart": 1.0, "zoomEnd": 1.12, "fit": "contain", "bgColor": "#ffffff",
    "focusX": 0.5, "focusY": 0.4 } ] }
```

Beat durations = measured from the word timing (each beat sized to its audio
slice — NEVER one static image for the whole gem).

```bash
node kenburns.mjs scenes.json --out beats.mp4
```

### Step 5 — mux

```bash
ffmpeg -i beats.mp4 -i gem.mp3 -vf "ass=subs.ass" -c:v libx264 -crf 23 \
  -c:a aac -map 0:v:0 -map 1:a:0 -shortest final.mp4
```

### Step 6 — validate (CF vision)

Extract a still per beat → `@cf/meta/llama-3.2-11b-vision-instruct`: relevant
to claim? DISTINCT from others? subject framed? Fix → re-render. Plus pixel
check on diagram beats (content present, no cut margins).

---

## 3. BEAT-COUNT GUIDE

| Gem length | Beats | Notes |
|------------|-------|-------|
| < 60s | 1-2 | one image + optional zoom |
| 60-120s | 2-3 | rotate at claim changes |
| > 120s | 3-5 | every major claim gets its own beat |

Beat change points = topic shifts in the window's own transcript (you have the
timed text — use it).

---

## 4. TITLE CARD (optional but recommended)

First 2.5s: the YouTube title (≤7 words) as a clean typographic card on the
mechanism-render or the first image — satisfies the "1-3 designed words" rule
without burning it into the whole video.

---

## 5. QUALITY GATES

- [ ] every beat relevant (vision states WHY)
- [ ] every beat distinct (holistic review catches crops/dupes)
- [ ] subs = ground truth, bottom, word-synced
- [ ] no mis-transcribed technical terms
- [ ] file < ~20MB, crf 23-26
- [ ] ear-check: audio cold-opens cleanly (no clipped sentence start)
