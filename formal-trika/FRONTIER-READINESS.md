# G2/G3/G4 — frontier readiness + comparison scaffold (2026-11-06, verified live)

## G2: e-text acquisition (checked this session)

| Target | MIRI IAST library | GRETIL | Verdict |
|---|---|---|---|
| Kularatnoddyota 5.84–101 (sprint 1) | ABSENT (full index grepped) | ABSENT | **BLOCKED on acquisition** — NGMPP A 149/1 microfilm request or scholar channel; do NOT start without source |
| Śrīmatottara 7 | ABSENT | ABSENT (not checked exhaustively; presumed absent) | BLOCKED (same path: NAK 2/214) |
| Tantrasadbhāva 2 | ABSENT | ABSENT | BLOCKED (NAK 5/445; Bang diss is CC BY control) |
| KMT 17.94–109 | ancillaries only | PRESENT (xml+html+txt, CC BY-NC-SA) | **READY — executable first target** |
| ṢaṭSS 7.5–38 | PRESENT (`SatSahasrakAlottarAgama-M00249-IAST.txt`) | — | **READY second** (fetch on sprint start; CC BY-NC 4.0 MIRI terms) |
| MVT 3 / SYM 3 / TSB 3.96–132 (controls) | MVT: `mAlinIvijayottaratan…` PRESENT | — | controls available |

**Executable order flips to: KMT-17 → ṢaṭSS → KuRatnUdd (on acquisition).**
MIRI terms: CC BY-NC 4.0 e-texts, scholar use; record license per packet.

## G3: five-maps comparison scaffold

`formal-trika/data/five-maps.json` (this session): per map {source, format,
license, status} + comparison dimensions (phoneme→locus→śakti→iconography;
agreement = rule-set diff, NOT prose diff) + the question each pair
answers (e.g. TĀ15 vs KMT17: same 50? same loci? where diverge = finding).
Populated for TĀ15 (local: passages+T1+ARGMAP) + matrika_body_map (key);
KMT17/SYM3/MVT3/TSB3 rows marked FETCH-ON-SPRINT with URLs.

## G4: Triśirobhairava reconstruction inputs (located, not fetched)

- Jayaratha TĀV on TĀ 15.121–125b (the quotation) — BEYOND local
  tantraloka-a15 range (15.1–120); needs TĀV edition (KSTS or MIRI).
- KMT 17.94–109 (GRETIL ✓), MVT 3 (MIRI ✓), SYM 3 (Törzsök thesis),
  TSB 3 (Bang diss, CC BY). Inventory only; reconstruction starts when
  all five are on disk with licenses recorded.
