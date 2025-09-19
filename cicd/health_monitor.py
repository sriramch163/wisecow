#!/usr/bin/env python3
import psutil
import os
from datetime import datetime

# Thresholds
CPU_LIMIT = 80
MEMORY_LIMIT = 80
DISK_LIMIT = 80
PROCESS_LIMIT = 200

def log_message(msg):
    os.makedirs('health-logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = f'health-logs/health-{datetime.now().strftime("%Y%m%d")}.log'
    
    print(f"{timestamp} - {msg}")
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - {msg}\n")

def check_health():
    log_message("=== HEALTH CHECK START ===")
    
    # Check CPU
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_LIMIT:
        log_message(f"ALERT: CPU {cpu}% > {CPU_LIMIT}%")
    else:
        log_message(f"CPU: {cpu}% OK")
    
    # Check Memory
    memory = psutil.virtual_memory().percent
    if memory > MEMORY_LIMIT:
        log_message(f"ALERT: Memory {memory}% > {MEMORY_LIMIT}%")
    else:
        log_message(f"Memory: {memory}% OK")
    
    # Check Disk
    disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/').percent
    if disk > DISK_LIMIT:
        log_message(f"ALERT: Disk {disk:.1f}% > {DISK_LIMIT}%")
    else:
        log_message(f"Disk: {disk:.1f}% OK")
    
    # Check Processes
    processes = len(psutil.pids())
    if processes > PROCESS_LIMIT:
        log_message(f"ALERT: Processes {processes} > {PROCESS_LIMIT}")
    else:
        log_message(f"Processes: {processes} OK")
    
    log_message("=== HEALTH CHECK END ===")

if __name__ == "__main__":
    check_health()