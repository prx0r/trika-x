# Blind re-derivation note — Upaya family-2 (cross-family replication)

**Date:** 2026-11-06. **Protocol:** tools/blind_family2.py (same prompt,
stateless calls, receipts with prompt sha). Families: Mistral (mistral-small-3.1-24b)
+ Alibaba (qwen3-30b-a3b-fp8) — two organizations, rotation-valid. One qwen
call returned null content (logged as ERROR, fail-closed, not data); retry succeeded.

## Verdicts (graded by box agent against checked-in recognition/Upaya.lean)

| Claim | Checked-in | Mistral | Qwen | Verdict |
|---|---|---|---|---|
| śāmbhava = readiness | `s.ready` | `s.ready` | `s.ready` | SAME ×2 |
| śākta = ready ∧ pure | `s.ready && s.pure` | identical | identical | SAME ×2 |
| purity witness | filtered-length > 0 | `{ready, ¬pure}` exhibited | `⟨true,false⟩` + theorems | SAME ×2 |
| śākta ⊆ śāmbhava | empty-difference count | ∀-Prop | `fun s h => and.left h` proof | SAME ×2 (shapes vary, content identical) |
| count = 2 | `length = 2` | def only (unevaluated) | `= 2 := rfl` | SAME (qwen exact; mistral def-correct) |
| āṇava formulable? | NO (Nat param) | UNFORMULABLE + why | UNFORMULABLE + why | GAP ×3 (three families agree) |

## Status

The śāmbhava/śākta half is REPLICATED (family-1 box-agent pilot + two
independent families, same rules, same gap). The āṇava VOCAB-GAP is now a
three-family consensus: {ready, pure} cannot express repetition — the vocab
extension (Nat transition indices, lead-agent decision) is confirmed as the
right next step, not a workaround. T-C2 (human rater-2) still owed for the
criteria themselves; replication covers encoding fidelity only.
