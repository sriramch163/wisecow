#!/usr/bin/env python3
import subprocess
import datetime
import sys
import os

# Configuration
SOURCE_DIR = "/path/to/backup"
REMOTE_HOST = "user@remote-server.com"
REMOTE_DIR = "/backup/destination"
LOGFILE = "backup.log"

def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {message}"
    print(log_entry)
    with open(LOGFILE, "a") as f:
        f.write(log_entry + "\n")

def backup_directory():
    if not os.path.exists(SOURCE_DIR):
        log_message(f"ERROR: Source directory {SOURCE_DIR} does not exist")
        return False
    
    rsync_cmd = [
        "rsync", "-avz", "--delete",
        SOURCE_DIR + "/",
        f"{REMOTE_HOST}:{REMOTE_DIR}/"
    ]
    
    try:
        log_message(f"Starting backup: {SOURCE_DIR} -> {REMOTE_HOST}:{REMOTE_DIR}")
        result = subprocess.run(rsync_cmd, capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0:
            log_message("SUCCESS: Backup completed successfully")
            return True
        else:
            log_message(f"ERROR: Backup failed with exit code {result.returncode}")
            log_message(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        log_message("ERROR: Backup timed out after 1 hour")
        return False
    except Exception as e:
        log_message(f"ERROR: Backup failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        SOURCE_DIR = sys.argv[1]
    if len(sys.argv) > 2:
        REMOTE_HOST = sys.argv[2]
    if len(sys.argv) > 3:
        REMOTE_DIR = sys.argv[3]
    
    success = backup_directory()
    sys.exit(0 if success else 1)