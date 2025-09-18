#!/bin/bash

# Configuration
SOURCE_DIR="${1:-/path/to/backup}"
REMOTE_HOST="${2:-user@remote-server.com}"
REMOTE_DIR="${3:-/backup/destination}"
LOGFILE="backup.log"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S'): $1" | tee -a "$LOGFILE"
}

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    log_message "ERROR: Source directory $SOURCE_DIR does not exist"
    exit 1
fi

log_message "Starting backup: $SOURCE_DIR -> $REMOTE_HOST:$REMOTE_DIR"

# Perform backup using rsync
if rsync -avz --delete "$SOURCE_DIR/" "$REMOTE_HOST:$REMOTE_DIR/"; then
    log_message "SUCCESS: Backup completed successfully"
    exit 0
else
    log_message "ERROR: Backup failed with exit code $?"
    exit 1
fi