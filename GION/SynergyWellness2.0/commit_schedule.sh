#!/bin/bash

REPO_DIR="/Users/botmaster/GION/SynergyWellness2.0"
LOG_FILE="$REPO_DIR/commit_schedule.log"

cd $REPO_DIR || exit 1

while true; do
    # Small commit every 5 minutes
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    git add . >> $LOG_FILE 2>&1
    git commit -m "Auto commit $timestamp" >> $LOG_FILE 2>&1
    
    # Wait 5 minutes
    sleep 300
    
    # Major commit every 30 minutes
    if (( $(date +%M) % 30 == 0 )); then
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")
        git add . >> $LOG_FILE 2>&1
        git commit -m "Major commit $timestamp" >> $LOG_FILE 2>&1
    fi
done
