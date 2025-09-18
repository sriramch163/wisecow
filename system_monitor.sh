#!/bin/bash

# Thresholds
CPU_THRESHOLD=80
MEM_THRESHOLD=80
DISK_THRESHOLD=80
LOGFILE="/var/log/system_monitor.log"

# Get current metrics
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
PROCESS_COUNT=$(ps aux | wc -l)

# Alert function
alert() {
    echo "$(date): ALERT - $1" | tee -a $LOGFILE
}

# Check thresholds
[ ${CPU_USAGE%.*} -gt $CPU_THRESHOLD ] && alert "CPU usage: ${CPU_USAGE}%"
[ $MEM_USAGE -gt $MEM_THRESHOLD ] && alert "Memory usage: ${MEM_USAGE}%"
[ $DISK_USAGE -gt $DISK_THRESHOLD ] && alert "Disk usage: ${DISK_USAGE}%"

echo "$(date): CPU: ${CPU_USAGE}% | MEM: ${MEM_USAGE}% | DISK: ${DISK_USAGE}% | PROCESSES: $PROCESS_COUNT"