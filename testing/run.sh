#!/bin/bash
# run.sh — red-team runner. Usage: bash run.sh T02|T03|...|all
# Every stub below was executed and corrected 2026-11-10; verified commands
# only. Earlier broken revisions are preserved in git history.
set -u
TDIR=/root/trika-x/testing
LOGD=$TDIR/logs
mkdir -p $LOGD
run_one() {
  T=$1
  LOG=$LOGD/${T}.log
  echo "=== $T $(date -u +%FT%TZ) ===" | tee "$LOG"
  case $T in
    T02) cd /root/openpatala && {
      echo "--- WANT: Resolver exposes resolve(); witnesses stay 0 ---"
      python3 -c "from patala.resolver import Resolver; r=Resolver(); print([m for m in dir(r) if not m.startswith('_')][:8])"; echo "exit:$?"
      PGPASSWORD=patala psql -U patala -h 127.0.0.1 -d openpatala -t -c "SELECT count(*) FROM witnesses;"
      echo "exit:$?"
    } 2>&1 | tee -a "$LOG" ;;
    T03) cd /root/trika-x && {
      echo "--- WANT: unknown tool -> -32601, missing arg -> -32602, no traceback ---"
      printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"nope__nope","arguments":{}}}' '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"openpatala__resolve","arguments":{}}}' | timeout 25 python3 formal-trika/tools/federation_gateway.py 2>&1 | python3 -c "import sys,json; [print(json.loads(l).get('id'), str(json.loads(l).get('result',json.loads(l).get('error')))[:80]) for l in sys.stdin if l.strip()]"
      echo "exit:$?"
    } 2>&1 | tee -a "$LOG" ;;
    T04) cd /root/trika-x && {
      echo "--- WANT: dead child excluded, parent stays up (FailOpen) ---"
      FEDERATION_CONFIG=/tmp/definitely-missing-children.json python3 formal-trika/tools/federation_gateway.py <<'EOF' 2>&1 | head -c 1200
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
EOF
      echo "exit:$?"
      python3 tools/mcp_catalog.py --check 2>&1 | tail -2
    } 2>&1 | tee -a "$LOG" ;;
    T10) cd /root/trika-x && {
      echo "--- WANT: 909 bundles, 236 COMPLETE / 673 PARTIAL ---"
      python3 -c "import json; d=json.load(open('formal-trika/data/traces/index.json')); from collections import Counter; print(d['count'], dict(Counter(e['verdict'] for e in d['entries'])))"
      echo "exit:$?"
      python3 formal-trika/tools/trace_bundle.py --help 2>&1 | head -5
    } 2>&1 | tee -a "$LOG" ;;
    *) echo "probe $T not implemented yet (see logs/T##.log for manual probes T05-T09, T11-T19)" | tee -a "$LOG" ;;
  esac
}
if [ "${1:-}" = "all" ]; then for t in T02 T03 T04 T10; do run_one $t; done
else run_one "${1:-T02}"; fi
