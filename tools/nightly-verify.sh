#!/bin/sh
# Nightly read-only verification (no commits, no deploys, no writes to repos).
# Logs to /tmp/nightly-verify.log. Install (owner call): crontab -e -> 0 3 * * * /root/trika-x/tools/nightly-verify.sh
export PATH="$HOME/.elan/bin:$PATH"
LOG=/tmp/nightly-verify.log
echo "=== $(date -u +%FT%TZ) ===" >> "$LOG"
python3 /root/trika-x/formal-trika/tools/evidence_check.py >> "$LOG" 2>&1
python3 /root/trika-x/formal-trika/tools/table.py --check >> "$LOG" 2>&1
python3 /root/trika-x/formal-trika/tools/arrivals.py >> "$LOG" 2>&1
python3 /root/trika-x/formal-trika/tools/bridge_resolve.py --check --tw /root/translation-work >> "$LOG" 2>&1
python3 -m unittest discover -s /root/trika-x/formal-trika/tests >> "$LOG" 2>&1
su postgres -c "psql -d openpatala -t -c 'SELECT count(*) FROM passages;'" >> "$LOG" 2>&1
echo "rc=$?" >> "$LOG"
