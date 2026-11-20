# Gold-standard essay: Kaul, “Causal Reasoning in the Trika Philosophy of Abhinavagupta”

Imported 2026-11-15 from R2 (`ayoutube/Causal_Reasoning_in_the_Trika_Philosophy.pdf`,
sha256 in `provenance.json`). This is the reference artefact for **what a finished
argumentative essay in our domain looks like** — the target that the `v6 prose`
stage of `ESSAY-PIPELINE.md` has so far been described but not demonstrated.

| File | What |
|---|---|
| `paper.pdf` | the chapter as uploaded (Springer, 2022) |
| `paper.txt` | `pdftotext -layout` extraction (hashed in provenance) |
| `structure.json` | machine skeleton + rhetorical feature table (`tools/essay_gold_analyze.py`) |
| `template.json` | normalised shape: section roles, word shares, move counts, verse protocol |

Rights: copyrighted, Springer Nature India. Vendored for **analysis only**; do not
serve `paper.pdf` or `paper.txt` publicly. Cite `10.1007/978-81-322-2577-5_31`.

## Re-run the analysis

```sh
cd /root/trika-x/formal-trika
python3 tools/essay_gold_analyze.py \
  bridge/essay-gold/kaul-causal-reasoning-2022/paper.txt \
  --title "Causal Reasoning in the Trika Philosophy of Abhinavagupta" \
  --out bridge/essay-gold/kaul-causal-reasoning-2022/structure.json
```

The tool is generic: give it any chapter PDF/`.txt` and it reports section
architecture, citation density, primary-source quotation discipline and
objection/reply moves. It measures **form only** — never whether a reading is
true.

See `../../ESSAY-GOLD-STANDARD.md` for the reverse-engineered template and how
it maps onto `ESSAY-SCHEMA.md` / `essay_compile.py`.
