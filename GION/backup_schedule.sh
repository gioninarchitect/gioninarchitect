#!/bin/bash

# Configuration
REPO_DIR="/Users/botmaster/GION/SynergyWellness2.0"
BACKUP_DIR="$REPO_DIR/backups"
TASK_DIR="$REPO_DIR/tasks"
LOG_FILE="$REPO_DIR/backup_schedule.log"
DB_PATH="$REPO_DIR/backend/instance/synergy_wellness.db"

# Create directories if they don't exist
mkdir -p $BACKUP_DIR
mkdir -p $TASK_DIR

# Task execution function
execute_task() {
    local task_file=$1
    local task_log="$TASK_DIR/$(basename $task_file).log"
    
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Starting task: $task_file" >> $LOG_FILE
    
    # Execute task and log output
    bash $task_file >> $task_log 2>&1
    
    if [ $? -eq 0 ]; then
        echo "[$(date +"%Y-%m-%d %H:%M:%S")] Task completed successfully: $task_file" >> $LOG_FILE
        mv $task_file "$TASK_DIR/completed/"
    else
        echo "[$(date +"%Y-%m-%d %H:%M:%S")] Task failed: $task_file" >> $LOG_FILE
        mv $task_file "$TASK_DIR/failed/"
    fi
}

# Main loop
while true; do
    # Create backup
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    backup_file="$BACKUP_DIR/synergy_wellness_$timestamp.db"
    cp $DB_PATH $backup_file
    gzip $backup_file
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] Created backup: ${backup_file}.gz" >> $LOG_FILE

    # Process pending tasks
    mkdir -p "$TASK_DIR/pending"
    mkdir -p "$TASK_DIR/completed"
    mkdir -p "$TASK_DIR/failed"
    
    for task in $(ls $TASK_DIR/pending/*.sh 2>/dev/null); do
        execute_task $task
    done

    # Wait 1 hour between cycles
    sleep 3600
done
