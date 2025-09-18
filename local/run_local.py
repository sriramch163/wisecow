#!/usr/bin/env python3
"""Local execution runner"""

import subprocess
import sys
import os

def run_local_operations():
    """Run local system operations"""
    print("=== LOCAL SYSTEM OPERATIONS ===")
    
    # Install dependencies
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-local.txt'])
    
    # Set local environment
    os.environ.update({
        'CPU_THRESHOLD': '85',
        'MEMORY_THRESHOLD': '85',
        'DISK_THRESHOLD': '85',
        'SOURCE_DIR': './test-data',
        'BACKUP_DIR': './backups'
    })
    
    # Run health check
    print("\n1. Running health check...")
    health_result = subprocess.run([sys.executable, 'system_monitor_local.py'])
    
    if health_result.returncode == 0:
        print("\n2. Running backup...")
        backup_result = subprocess.run([sys.executable, 'backup_local.py'])
        
        if backup_result.returncode == 0:
            print("\n🎉 All local operations completed!")
            print("Check local_health.log and local_backup.log for details")
            print("Backup files are in ./backups/")
        else:
            print("\n❌ Backup failed")
            return 1
    else:
        print("\n❌ Health check failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(run_local_operations())