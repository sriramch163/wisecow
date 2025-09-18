#!/usr/bin/env python3
import psutil
import datetime

# Thresholds
CPU_THRESHOLD = 80
MEM_THRESHOLD = 80
DISK_THRESHOLD = 80
LOGFILE = "system_monitor.log"

def alert(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_msg = f"{timestamp}: ALERT - {message}"
    print(alert_msg)
    with open(LOGFILE, "a") as f:
        f.write(alert_msg + "\n")

# Get metrics
cpu_usage = psutil.cpu_percent(interval=1)
mem_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent
process_count = len(psutil.pids())

# Check thresholds
if cpu_usage > CPU_THRESHOLD:
    alert(f"CPU usage: {cpu_usage:.1f}%")
if mem_usage > MEM_THRESHOLD:
    alert(f"Memory usage: {mem_usage:.1f}%")
if disk_usage > DISK_THRESHOLD:
    alert(f"Disk usage: {disk_usage:.1f}%")

print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: CPU: {cpu_usage:.1f}% | MEM: {mem_usage:.1f}% | DISK: {disk_usage:.1f}% | PROCESSES: {process_count}")