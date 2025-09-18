#!/usr/bin/env python3
import os
import shutil
import tarfile
import boto3
import logging
from datetime import datetime
from pathlib import Path

# Local Configuration
SOURCE_DIR = os.getenv('SOURCE_DIR', './test-data')
BACKUP_DIR = os.getenv('BACKUP_DIR', './backups')
S3_BUCKET = os.getenv('S3_BUCKET')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('local_backup.log'),
        logging.StreamHandler()
    ]
)

def create_test_data():
    """Create sample data for local testing"""
    os.makedirs(SOURCE_DIR, exist_ok=True)
    
    files = {
        'config.json': '{"app": "wisecow", "env": "local"}',
        'data.txt': f'Sample data created at {datetime.now()}',
        'logs/app.log': 'Application log entries...'
    }
    
    for file_path, content in files.items():
        full_path = os.path.join(SOURCE_DIR, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
    
    logging.info(f"Created test data in {SOURCE_DIR}")

def local_backup():
    """Comprehensive local backup"""
    logging.info("=== LOCAL BACKUP PROCESS ===")
    
    # Create test data if source doesn't exist
    if not os.path.exists(SOURCE_DIR):
        create_test_data()
    
    # Create backup directory
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f"local_backup_{timestamp}.tar.gz")
    
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(SOURCE_DIR, arcname=os.path.basename(SOURCE_DIR))
    
    file_size = os.path.getsize(backup_file)
    logging.info(f"Created backup: {backup_file} ({file_size} bytes)")
    
    # Optional S3 upload
    if S3_BUCKET:
        try:
            s3 = boto3.client('s3')
            s3.upload_file(backup_file, S3_BUCKET, f"local-backups/{os.path.basename(backup_file)}")
            logging.info(f"Uploaded to S3: {S3_BUCKET}")
        except Exception as e:
            logging.warning(f"S3 upload failed: {e}")
    
    # Cleanup old backups (keep last 5)
    backup_files = sorted(Path(BACKUP_DIR).glob("local_backup_*.tar.gz"))
    for old_backup in backup_files[:-5]:
        old_backup.unlink()
        logging.info(f"Removed old backup: {old_backup.name}")
    
    logging.info("✅ Local backup completed")
    return True

if __name__ == "__main__":
    exit(0 if local_backup() else 1)