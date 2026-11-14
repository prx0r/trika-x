# SVREAD SANSKRIT SURFACE — review + build spec (proposal, 2026-11-07)
*Status: PROPOSED. svread lane spec; their lane disposes.

 Status: PROPOSAL (trika-x lane). svread lane disposes. Nothing here edits
 svread, bookfactory, or translation-work. No auto-anything; owner gates stand.

## 0. Review: bookfactory 118b227 (2026-11-07, origin/master)

 `learn-sanskrit: formatting gate green + audio plan + site one-link`.
 Verdict: GREEN, honestly gated.
 - 10 lessons, "Learn Sanskrit with Abhinavagupta — Vol. I, Ten Passages from
   Sound to Recognition" (index.json): stage-1-sounds (l01–l02) →
   stage-2-language (l03–l04) → stage-3-instructions (l05–l08…) — sourced from
   real works (Bhairavastava bh-p02/bh-p01/bh-p09, Mahopadesha mpa-p01,
   Anuttarastika anu-p02, Paramarthasara…). Pedagogy is discover-before-
   paradigm (rule box 4: "-ti endings — discover before the paradigm").
 - Rule boxes cite Panini by sutra (rb-1: 6.1.101 akah savarne dirghah) +
   sandhi/case/verb patterns, each with reverse-reading notes. Curated
   content, not generated — keep it that way (generators propose rule boxes;
   humans sign them; same law as translations).
 - Audio plan (audio-plan.json v1.0): 20 clips, fish-audio verse + granny
   voices, content-hash cache keys. Render waits owner go (recorded in the
   commit). Correct — no render without go.
 - Gate: content → structure → formatting canonical; build has exactly 2
   DUE-LATER (per-entry ship handoff, PDF proof). Fail-closed, as designed.
 - Notes for adoption: (a) lesson HTML pulls Google Fonts CDN (visit leak;
   fonts/ vendored Tiro + Cormorant OFL in-repo — self-host at deploy);
   (b) :8600 serves on the lane's box only (nothing on this box's :8600 —
   verified); (c) index.json `source_ref`s (bh-p02, mpa-p01…) resolve against
   translation-work chunk locators — the bridge, not copies.

## 1. What the user asked (interpreted, kept separate from the words)

 A `Sanskrit` header item on svread.pages.dev, served with full feature
 parity (reader, chat, recitation, scholar context), plus a tab for complex
 grammatical breakdowns using the estate's ML stack (Mitra/Mitrasamgraha,
 Vidyut, ByT5, COMET-family, proof gate, persona renders), for learning
 Sanskrit alongside our works.

## 2. Routing + hosting (reality-checked against the live app)

 - Header: add `<li><a href="?view=sanskrit" id="navsanskrit">Sanskrit</a></li>`
   after Scholar in index.html (Browse Library / Text Search / Scholar /
   Pushing Lab pattern — see app.js `?view=scholar` hub at line 318).
 - View: `?view=sanskrit` route in app.js reusing the same gated loaders
   (hash-checked projections + release-manifest gate — the SAME gate controls
   every reader surface including audio and exports today).
 - Subdomain ("sanskrit.svread"): NOT directly provisionable — svread.pages.dev
   is a Pages-assigned domain (no nested sub-subdomains). Ranked options:
   (a) `?view=sanskrit` in the same app NOW — zero infra, ships with chat +
   recitation + scholar context; (b) separate Pages project later (e.g.
   sanskrit-svread) sharing the repo/static + a real custom domain
   (`sanskrit.<domain>`) when the owner configures one. Recommend (a) now.
 - Lesson payload: vendor frozen `prints/learn-sanskrit/site/*.html` +
   index.json + rule-boxes.json at release time (emit step like
   emit_scholar.py → data/sanskrit/, hash-pinned in release_manifest.json).
   Audio via existing R2 pattern (`R2/audio/{dir}/{clip}.mp3` + karaoke
   timings; reciteVerse/splayToggle reused). No live dependency on
   bookfactory outputs — release-time vendoring only.

## 3. Feature parity (same app, same laws)

 | Main page | Sanskrit view |
 |---|---|
 | Reader (verses + layers, hash-checked) | Same, lessons address chunk locators (bh-p02…) resolved via lingua/openpatala bridge; layer labels use PUBLIC names (layer-names.json: literal-gloss, argument-map…) with codes underneath |
 | Chat rail (chat box + pushing rotation) | Same component, Sanskrit-tuned placeholder; Qwen needs existing consent + quotas; no training on user text |
 | Right-rail voice chat | Same ScholarVoice client as Scholar, attached to the chat rail (Talk → transcribe → send as chat message → reply plays back via the same audio path). No new infra (§7) |
 | Recitation (R2 audio + karaoke, per-section play) | Fish Audio (`POST /api/read` → `read-v2` R2 cache); verse + granny voices from audio-plan.json AFTER owner go; the gate controls audio like every surface |
 | Scholar context (versions, signoff state) | Same panel (read-only here; signoff stays in Scholar) |
 | Pushing Lab link | Same; Sanskrit questions can enter the crux queue via existing exporter |

## 3b. Right-rail chat context contract (lesson + lore + Sanskrit aware)

 Same spine as home chat (`POST /api/chat/:work`: bge-m3 embed → gate-weighted
 retrieval PASS/PUBLISHED/OWNER only, BLOCKED=0 → pushing-probe template match
 + hound verdicts → diverse pick per work → bge-reranker → argument-packet
 graph walk → lexical fallback → Qwen drafts with relayed ids; sessions in
 D1). The Sanskrit rail differs only in SCOPE + PINNED CONTEXT:

 - Scope: `works` param = the lesson's work(s) (e.g. bhairavastava for l01).
   Retrieval never leaves the lesson's works unless the learner asks outward
   (then it behaves exactly like home chat).
 - Pinned context (prepended like the existing chainCtx prior-enquiry block,
   same mechanism, no new infra): the lesson's verse (Sanskrit + L2 +
   essence), its L0 key glosses, its rule boxes, and linked lore concept
   entries (translation-work lore/concepts + trika_glossary_index). Deterministic
   layers first (L0/rule boxes answer grammar questions directly); vectors
   second; ML candidates labelled per §4.
 - Lore-aware means: concept entries resolve through the same passage/chunk
   refs (no separate lore index to build — cite the concept file + its
   sources, same as essay citations).
 - Sanskrit-aware means: sandhi/morphology questions hit the L0 spine +
   rule boxes before any model; Vidyut/ByT5 outputs render as labelled
   candidates beside the deterministic answer, never instead of it.
 - Voice on the rail: Talk transcribes → transcript becomes the chat message
   (visible, editable before send — same consent shape as Scholar) → reply
   streams as text + plays as audio. Sessions persist in D1 per lesson.

## 4. Grammar-breakdown tab (which ML for which job — gated)

 Order: deterministic first, ML second, labelled always.

 - Breakdown spine (deterministic, no model): L0 options + chosen gloss +
   rule-box Panini refs + sandhi splits. This carries the tab; everything
   below is annotation, never the answer.
 - Segmentation/lemmatization CANDIDATES: Vidyut 0.4.0 (transliteration,
   meter with licensed meter file) + ByT5-Sanskrit (segmentation/lemmas).
   Status machine-generated-unreviewed (vidyut_candidates precedent); never
   writes T1/L0/Git/site; source hash recorded; Ghatakarpara rule stands
   (withheld until alignment repaired).
 - Meaning match: Mitrasamgraha 5,552 + 5,601 gold exemplars as the test set;
   chrF/BLEU baselines; COMET/COMETKiwi as THRESHOLDED SIGNAL ONLY (needs
   torch/GPU box) — never a verdict, never a publish gate.
 - Proof gate over anything generated: SOURCE_BINDING / COVERAGE /
   ABSTENTION / TERM_CONSISTENCY / CITATION_GROUNDING (translation_proof.py
   lineage). BLOCKED stays blocked; SMOKE tests (3×3) are plumbing, not proof
   (tau-b corrected, human gold required before any metric claim).
 - Register help (eli5 Panini, paradigm drills): persona/C2-style prompt
   renders with model/date recorded (persona LoRA = GPU-later; prompt renders
   now). A generated rule box is a proposal until a human signs it.
 - "Panini ML" (sutra application as a model): GAP — needs its own gold
   (sutra→example pairs) + prereg before any build. Rule boxes stay curated
   content until then. Do not ship a model that invents sutras.

## 5. Explicit non-goals

 No ship/render/publish tools in the view. No training on learner input. No
 cross-scholar style mixing. No auto-signed essays from chat. No second
 ledger, no second ID scheme (chunk locators resolve via the bridge).
 Voice/browser e2e gaps carry over (text first, same as Scholar).

## 7. Voice: reuse both existing paths, build nothing new

 Two voice jobs, two wired paths — the Sanskrit view reuses both:

 - Recitation (verse audio): Fish Audio via worker `POST /api/read` →
   R2 (`read-v2/<work>/<passage>_<lang>_<sha>.mp3`, s2.1-pro-free, cached,
   hash-keyed). The Learn Sanskrit audio-plan (verse + granny voices, 20
   clips) plugs in HERE once the owner gives the render go. Never use
   realtime for recitation (uncacheable, non-deterministic, eats quota).
 - Spoken conversation (lesson Q&A, repeat-after-me): Qwen realtime via the
   EXISTING stack — browser client `svread/scholar-voice.js` (push-to-talk,
   16kHz in / 24kHz out, OpenAI-realtime-style protocol) + worker WS proxy
   (`ipvv/worker/src/scholar-workspace.js:252-307`, allowlisted DashScope
   `/api-ws/v1/realtime`, model `qwen3.8-omni-flash-realtime`, key server-side,
   consent modal + quota warning + private transcripts in the Scholar UI).
   The Sanskrit view instantiates the same client with lesson context instead
   of essay context. No new infra.
 To switch on (owner-gated, all three): `QWEN_REALTIME_ENABLED=true` +
 `SCHOLAR_QWEN_FREE_TIER_CONFIRMED=true` + `SCHOLAR_DASHSCOPE_API_KEY` (+
 `SCHOLAR_DASHSCOPE_API_KEY` for text), then a browser e2e session (wire
 proven, session unverified — SPEC §8). Gap (not built): explicit
 pronunciation scoring (the model hears learner audio conversationally today;
 phoneme-level feedback needs its own design + gold, same rules as Panini-ML).

## 6. Acceptance (one slice)

 `?view=sanskrit` shows lesson l01 (mamātmā) with its verse, literal-gloss
 breakdown, rule boxes rb-1/rb-2, recitation IF audio shipped (owner go),
 chat answering from the same evidence spine with receipts, and a grammar
 tab where every ML line is labelled with model+status. An outsider replays
 lesson → locator → ledger bytes → gate. Until that slice, display ML
 outputs as research records only.
