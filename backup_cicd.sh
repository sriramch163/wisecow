#!/bin/bash

SOURCE_DIR="$1"
REMOTE_HOST="$2"
REMOTE_DIR="$3"
LOGFILE="backup.log"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a "$LOGFILE"
}

if [ ! -d "$SOURCE_DIR" ]; then
    log_message "ERROR: Source directory $SOURCE_DIR does not exist"
    exit 1
fi

log_message "Starting backup: $SOURCE_DIR -> $REMOTE_HOST:$REMOTE_DIR"

if rsync -avz --delete -e "ssh -o StrictHostKeyChecking=no" "$SOURCE_DIR/" "$REMOTE_HOST:$REMOTE_DIR/"; then
    log_message "SUCCESS: Backup completed successfully"
    echo "::notice::Backup completed successfully"
    exit 0
else
    log_message "ERROR: Backup failed with exit code $?"
    echo "::error::Backup failed"
    exit 1
fi