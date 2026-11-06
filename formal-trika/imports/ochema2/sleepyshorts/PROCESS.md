# SLEEPSHORTS — Process Runbook

**How to turn an R2 longform talk into the full product line.**
Follow this exactly. The taste decisions live in `shortselectionref.md` and
`REFERENCE.md` — this file is the mechanical pipeline.

---

## 0. THE PRODUCT LINE

```
R2 raw lecture
  → sleepies/  (high-signal cuts, 30-60 min each, multiple for super-longs)
  → gems/      (shorts: 45s-4min, 5-10 per hour of talk, parent-labeled)
  → <slug>-compilation.mp3  (highlights reel: all gems, shelf order, 0.5s gaps)
```

Every talk folder ships: plan md + timed transcript + sleepies + gems +
compilation + GEMS.md (spec cards) — unless it's a series (see §7).

---

## 1. PICK A TALK

Library: `r2:longform-audio/<series>/<video-id>/<video-id> - <title>.mp3`
Transcripts: `r2:longform-audio/transcripts/<series>/<video-id>/<video-id>.en.vtt`

Verify the transcript is REAL before trusting it:
- Download it, count words (`<c>` tokens). ~10k+ words for 1h = good.
- **Mangled captions happen** (e.g. bettina session 1: 1,129 words in 83 min,
  mixed Devanagari garbage). If word count is tiny or text is broken, find
  another source or skip — do NOT transcribe locally (slow CPU job, avoid).

---

## 2. SET UP THE FOLDER

```bash
mkdir -p /root/projects/ochema2/sleepyshorts/<slug>
cd /root/projects/ochema2/sleepyshorts/<slug>
rclone copyto "r2:longform-audio/<series>/<id>/<id> - <title>.mp3" ./talk.mp3
rclone copyto r2:longform-audio/transcripts/<series>/<id>/<id>.en.vtt ./talk.en.vtt
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 talk.mp3
```

---

## 3. TIMED TRANSCRIPT (word-level, from the VTT)

The VTT embeds word timestamps as `<00:00:01.560><c> word</c>`. Convert:

```python
import re
vtt = open('talk.en.vtt').read()
words = []
for m in re.finditer(r'<(\d\d:\d\d:\d\d\.\d\d\d)><c>\s*(.*?)\s*</c>', vtt):
    words.append((m.group(1), m.group(2)))
out = []
for i in range(0, len(words), 3):
    chunk = words[i:i+3]
    out.append('[' + chunk[0][0] + '] ' + ' '.join(w for _, w in chunk))
open('talk_timed.txt', 'w').write('\n'.join(out))
```

---

## 4. BLOCK MAP + GEMS IN ONE PASS

Read the timed transcript once, extracting BOTH:
- **Block map**: ~15-min interval scans + boundary checks → section table with
  KEEP/CUT verdicts (cut: greetings, housekeeping, breaks, slide-pointing,
  audio-hostile demo, dead air).
- **Gem candidates**: windows that score ≥5 on the weighting cheat-sheet
  (shortselectionref.md §5). Target 5-10/hr. **Central-claim coverage first**
  (the thesis itself must be a gem).

**Conversational/salon note:** threads, not blocks. The panel/Q&A segment of a
workshop is the gem motherlode.

Write `<slug>_edit_plan.md`: source line, type, block map table, sleepy
segmentation, gem table (window + hook), ochema-alignment notes.

---

## 5. CUT (python script — never shell heredocs, they mangle filenames)

```python
#!/usr/bin/env python3
import subprocess, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
SLEEPIES = [("sleepy1", "00:02:00", "00:42:00"), ...]
GEMS = [("g1_slug", "00:04:30", "00:05:40"), ...]

def dur(p):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=nw=1:nk=1",p],capture_output=True,text=True)
    return round(float(out.stdout.strip()),1)

os.makedirs("sleepies", exist_ok=True); os.makedirs("gems", exist_ok=True)
for name, s, e in SLEEPIES:
    subprocess.run(["ffmpeg","-v","error","-y","-ss",s,"-to",e,"-i","talk.mp3",
        "-c:a","libmp3lame","-b:a","128k",f"sleepies/{name}.mp3"],check=True)
    print(name, dur(f"sleepies/{name}.mp3"))
for name, s, e in GEMS:
    sleepy = "sleepy1" if s < "SEAM1" else "sleepy2"  # per-talk
    out = f"gems/{name}.mp3"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",s,"-to",e,"-i","talk.mp3",
        "-c:a","libmp3lame","-b:a","128k",out],check=True)
    # PARENT TAG (non-negotiable — the gem must know its sleepy):
    subprocess.run(["ffmpeg","-v","error","-y","-i",out,"-c","copy","-metadata",
        f"comment=parent=<slug>:{sleepy}","/tmp/opencode/t.mp3"],check=True)
    os.replace("/tmp/opencode/t.mp3", out)
    print(name, dur(out))
```

**Gotchas:**
- NEVER run ffmpeg loops from a bash heredoc — filenames get eaten. Write a
  .py and run it.
- `-ss` before `-i` for fast seeking; 128k mp3 everywhere.
- Stitches (tease→reveal, question→answer): cut each window to /tmp, concat
  with the concat demuxer `-c copy`.
- For the reel: 0.5s silence between gems (anullsrc), concat `-c copy`.

---

## 6. COMPILATION REEL

```bash
ffmpeg -v error -y -f lavfi -i anullsrc=r=44100:cl=mono -t 0.5 \
  -c:a libmp3lame -b:a 128k silence.mp3
# compile.txt: file 'gems/<g1>.mp3' / file 'silence.mp3' / ... in SHELF ORDER (chronological)
ffmpeg -v error -y -f concat -safe 0 -i compile.txt -c copy <slug>-compilation.mp3
```

---

## 7. SERIES (course lectures — DIFFERENT FLOW)

Bettina Bäumer (pratyabhijñā / shiva sutras / vijnana bhairava) is a SERIES,
not standalone talks: sessions build on each other, and gems would repeat
across sessions. **Do not run the single-talk flow on a series.** Series
treatment (future work): session index → per-session sleepy → a series-level
gem shelf with cross-session dedup.

---

## 8. DELIVERABLE CHECKLIST (per talk)

- [ ] `<slug>_edit_plan.md` (block map + sleepies + gem table)
- [ ] `talk_timed.txt` (word-timed)
- [ ] `sleepies/*.mp3` (30-60 min each, coherent seams)
- [ ] `gems/*.mp3` (5-10/hr, ID3 comment=parent tag, ≥5 score)
- [ ] `<slug>-compilation.mp3` (shelf order, 0.5s gaps)
- [ ] `GEMS.md` (spec card per gem: Title ≤7 words / Parent / Why gold /
      Standalone / Ochema alignment)
- [ ] `cut_all.py` (rerunnable)

**Before publish (the taste gates):**
- Title ≤7 words, no numbers/colons/!, declarative (data-backed — see ref)
- Ear-check each conversational-window gem (10s listen — cold open lands?)
- Cross-talk dedup: same claim appearing in two talks = keep one (e.g. the
  planaria counterfactual-memory claim exists in levin-mind-of-the-body AND
  levin-how-does-it-know — that's a duplicate on a channel)

---

## 9. STATE (2026-08-09)

| Talk | Type | Sleepies | Gems | Reel |
|---|---|---|---|---|
| levin-mind-of-the-body | structured lecture | 1 | 16 (exemplar pool) | — |
| andres-substrate-neutral | dense stream | 1 | 7 | 11:08 |
| tsc-2025-workshop5 | workshop (4h) | 5 | 23 | 34:54 |
| levin-how-does-it-know | lecture | 1 | 10 | 15:12 |
| levin-nothing-in-biology | formal lecture | 2 | 12 | 17:06 |
| andres-talking-with-ivan | conversational | 2 | 10 | 15:06 |
| wolfram-bach-bigger-brains | salon (3h) | 3 | 15 | 23:14 |

**Not processed (in R2):** bettina series (different flow), ~50 more levin
talks, QRI talks (math/qualia/monads), cimc salons, TSC plenaries (27),
sivananda series (different flow).
