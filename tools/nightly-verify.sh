#!/bin/sh
# Read-only verification; the process fails if any required check fails.
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd) || exit 2
TW=${TRANSLATION_WORK:-"$(dirname "$ROOT")/translation-work"}
LOG=${NIGHTLY_LOG:-/tmp/nightly-verify.log}
STATUS=0
export PATH="$HOME/.elan/bin:$PATH"
printf '=== %s ===\n' "$(date -u +%FT%TZ)" >> "$LOG" || exit 2

run_step() {
    name=$1
    shift
    if "$@" >> "$LOG" 2>&1; then
        printf 'PASS %s\n' "$name" >> "$LOG"
    else
        rc=$?
        printf 'FAIL %s (exit %s)\n' "$name" "$rc" >> "$LOG"
        STATUS=1
    fi
}

run_step evidence python3 "$ROOT/formal-trika/tools/evidence_check.py" --root "$TW"
run_step table python3 "$ROOT/formal-trika/tools/table.py" --check
run_step arrivals python3 "$ROOT/formal-trika/tools/arrivals.py" --tw "$TW"
run_step bridge python3 "$ROOT/formal-trika/tools/bridge_resolve.py" --check --tw "$TW"
run_step review_status python3 "$ROOT/formal-trika/tools/review_status.py" --check
run_step tests python3 -m unittest discover -s "$ROOT/formal-trika/tests"
if [ -n "${OPENPATALA_DSN:-}" ]; then
    run_step database psql "$OPENPATALA_DSN" -t -c 'SELECT count(*) FROM passages;'
else
    printf 'SKIP database (OPENPATALA_DSN not set)\n' >> "$LOG"
fi
printf 'SKIP Lean (run the pinned control and recognition checks separately)\n' >> "$LOG"
printf 'nightly result: %s\n' "$STATUS" >> "$LOG"
exit "$STATUS"
