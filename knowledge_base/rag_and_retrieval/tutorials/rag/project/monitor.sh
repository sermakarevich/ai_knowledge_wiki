#!/usr/bin/env bash
# Monitor the chapter-07 experiment batch.
# Usage: monitor.sh <pid>
# Exit codes: 0 = all 12 done, 1 = process died (partial), 2 = no progress 45 min
# Logs to /tmp/aseu6_status.log. Polls every 5 min.
set -u
PID="$1"
cd /Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag/project
LOG=/tmp/aseu6_status.log
TOTAL=12
INTERVAL=300
NOGROW_SECS=0
CHAT_DELTA=$(find data/cache/chat -type f 2>/dev/null | wc -l | tr -d ' ')
DONE_DELTA=$(ls runs/07_*/metrics.json 2>/dev/null | wc -l | tr -d ' ')
echo "[$(date +%H:%M:%S)] monitor started for pid=$PID (baseline done=$DONE_DELTA chat=$CHAT_DELTA)" >> "$LOG"
while :; do
    sleep "$INTERVAL"
    NOW_ISO=$(date +%H:%M:%S)
    if ! kill -0 "$PID" 2>/dev/null; then
        DONE=$(ls runs/07_*/metrics.json 2>/dev/null | wc -l | tr -d ' ')
        LAST=$(tail -1 /tmp/rerank_eval_v2.log 2>/dev/null)
        echo "[$NOW_ISO] pid $PID DEAD — done=$DONE/$TOTAL last=$LAST" >> "$LOG"
        echo "MONITOR_EXIT=1 reason=process_died done=$DONE total=$TOTAL"
        exit 1
    fi
    DONE=$(ls runs/07_*/metrics.json 2>/dev/null | wc -l | tr -d ' ')
    CHAT=$(find data/cache/chat -type f 2>/dev/null | wc -l | tr -d ' ')
    if [ "$DONE" -ge "$TOTAL" ]; then
        echo "[$NOW_ISO] ALL $TOTAL DONE" >> "$LOG"
        echo "MONITOR_EXIT=0 reason=all_done done=$DONE total=$TOTAL"
        exit 0
    fi
    if [ "$CHAT" -eq "$CHAT_DELTA" ] && [ "$DONE" -eq "$DONE_DELTA" ]; then
        NOGROW_SECS=$((NOGROW_SECS + INTERVAL))
    else
        NOGROW_SECS=0
    fi
    CHAT_DELTA=$CHAT
    DONE_DELTA=$DONE
    if [ "$NOGROW_SECS" -ge 2700 ]; then
        echo "[$NOW_ISO] SUSPECTED HANG — 45 min no new cache writes or metrics. done=$DONE chat=$CHAT" >> "$LOG"
        echo "MONITOR_EXIT=2 reason=suspected_hang done=$DONE total=$TOTAL"
        exit 2
    fi
    LAST=$(tail -1 /tmp/rerank_eval_v2.log 2>/dev/null)
    echo "[$NOW_ISO] ok pid=$PID done=$DONE/$TOTAL chat_cache=$CHAT no_grow=${NOGROW_SECS}s last=$LAST" >> "$LOG"
done