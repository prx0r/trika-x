# SLEEPSHORTS — longform audio → sleepy cuts → gems → compilation

The product line for the R2 longform-audio library:
**raw talk → high-signal sleepies (30-60 min) → gem shorts (5-10/hr) → highlights reel.**

## The three docs (read in this order)

1. **`shortselectionref.md`** — THE SELECTION CRITERIA. What makes a gem, the
   scoring cheat-sheet, title rules, cardinal rules (central-claim coverage,
   parent labeling, 5-10/hr, depth beats brevity).
2. **`REFERENCE.md`** — THE VALUE SYSTEM. The ochema moral (consciousness via
   frontier math/science + Tantrāloka/Sanskrit/Greek), talk types → cut
   strategies, the product line, the short-spec format.
3. **`PROCESS.md`** — THE RUNBOOK. The mechanical pipeline: pull from R2 →
   timed transcript → block map + gems in one pass → cuts → reel → checklist.

## Folder conventions

```
sleepyshorts/<slug>/
├── <slug>_edit_plan.md   # block map + sleepies + gem table
├── talk_timed.txt        # word-timed transcript
├── sleepies/             # 30-60 min units (slug per talk: sleepy1, sleepy2...)
├── gems/                 # g1_...mp3 ... (ID3 comment = parent)
├── <slug>-compilation.mp3
├── GEMS.md               # spec cards
├── cut_all.py            # rerunnable
└── publish/              # THE PUBLISH TREE (upload-ready)
    ├── shorts/NN-<slug>/ # per short: short.mp4 (slot, pending visuals),
    │                     #   transcript.txt (caption words), meta.json
    │                     #   (title, parent, windows, duration, description,
    │                     #    link placeholders {PARENT_URL}/{COMPILATION_URL})
    └── compilation/      # compilation.mp4 + chapters.txt (per-gem chapters)
                          # + compilation.meta.json
```

**Publishing:** rebuild with `build_publish.py` after any gem change. The
auto-uploader reads `publish/shorts/*/meta.json` (title + description + links)
and `publish/compilation/chapters.txt` (YouTube chapters). Link placeholders
are filled with the actual video URLs at upload time.

Series (bettina baumer etc.) use a different flow — see PROCESS.md §7.

## State

7 talks processed (15 sleepies, 77 gems, 6 reels) — inventory table in
PROCESS.md §9.
