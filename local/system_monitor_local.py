#!/usr/bin/env python3
import psutil
import logging
import os
from datetime import datetime

# Local Configuration - relaxed thresholds
CPU_THRESHOLD = int(os.getenv('CPU_THRESHOLD', 85))
MEMORY_THRESHOLD = int(os.getenv('MEMORY_THRESHOLD', 85))
DISK_THRESHOLD = int(os.getenv('DISK_THRESHOLD', 85))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('local_health.log'),
        logging.StreamHandler()
    ]
)

def detailed_system_check():
    """Detailed local system monitoring"""
    logging.info("=== LOCAL SYSTEM HEALTH CHECK ===")
    
    # CPU details
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    logging.info(f"CPU: {cpu_percent}% ({cpu_count} cores)")
    
    # Memory details
    memory = psutil.virtual_memory()
    logging.info(f"Memory: {memory.percent}% ({memory.used//1024//1024}MB used)")
    
    # Disk details
    disk = psutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    logging.info(f"Disk: {disk_percent:.1f}% ({disk.free//1024//1024//1024}GB free)")
    
    # Process count
    process_count = len(psutil.pids())
    logging.info(f"Processes: {process_count}")
    
    # Check thresholds
    issues = []
    if cpu_percent > CPU_THRESHOLD:
        issues.append(f"High CPU: {cpu_percent}%")
    if memory.percent > MEMORY_THRESHOLD:
        issues.append(f"High Memory: {memory.percent}%")
    if disk_percent > DISK_THRESHOLD:
        issues.append(f"High Disk: {disk_percent:.1f}%")
    
    if issues:
        for issue in issues:
            logging.warning(issue)
        return False
    
    logging.info("✅ Local health check passed")
    return True

if __name__ == "__main__":
    exit(0 if detailed_system_check() else 1)