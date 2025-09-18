#!/usr/bin/env python3
import psutil
import logging
import os

# CI/CD Configuration - stricter thresholds
CPU_THRESHOLD = int(os.getenv('CPU_THRESHOLD', 70))
MEMORY_THRESHOLD = int(os.getenv('MEMORY_THRESHOLD', 70))
DISK_THRESHOLD = int(os.getenv('DISK_THRESHOLD', 70))

# Setup logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('system_health.log')
    ]
)

def check_system_health():
    """CI/CD system health check"""
    logging.info("=== CI/CD HEALTH CHECK ===")
    
    # CPU check
    cpu = psutil.cpu_percent(interval=1)
    if cpu > CPU_THRESHOLD:
        logging.error(f"CPU: {cpu}% > {CPU_THRESHOLD}%")
        return False
    logging.info(f"CPU: {cpu}%")
    
    # Memory check
    memory = psutil.virtual_memory().percent
    if memory > MEMORY_THRESHOLD:
        logging.error(f"Memory: {memory}% > {MEMORY_THRESHOLD}%")
        return False
    logging.info(f"Memory: {memory}%")
    
    # Disk check
    disk = (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100
    if disk > DISK_THRESHOLD:
        logging.error(f"Disk: {disk:.1f}% > {DISK_THRESHOLD}%")
        return False
    logging.info(f"Disk: {disk:.1f}%")
    
    logging.info("✅ CI/CD Health check passed")
    return True

if __name__ == "__main__":
    exit(0 if check_system_health() else 1)