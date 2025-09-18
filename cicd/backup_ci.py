#!/usr/bin/env python3
import os
import tarfile
import boto3
import logging
from datetime import datetime

# CI/CD Configuration
SOURCE_DIR = os.getenv('SOURCE_DIR', './k8s')
S3_BUCKET = os.getenv('S3_BUCKET')

# Setup logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backup.log')
    ]
)

def backup_for_ci():
    """CI/CD backup - artifacts only"""
    logging.info("=== CI/CD BACKUP ===")
    
    if not os.path.exists(SOURCE_DIR):
        logging.error(f"Source not found: {SOURCE_DIR}")
        return False
    
    # Create backup directory and file
    backup_dir = "/tmp/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f"ci_backup_{timestamp}.tar.gz")
    
    with tarfile.open(backup_file, "w:gz") as tar:
        tar.add(SOURCE_DIR, arcname="artifacts")
    
    logging.info(f"Created: {backup_file}")
    
    # Upload to S3 if configured
    if S3_BUCKET:
        try:
            s3 = boto3.client('s3')
            s3.upload_file(backup_file, S3_BUCKET, f"ci-backups/{backup_file}")
            logging.info(f"Uploaded to S3: {S3_BUCKET}/ci-backups/{backup_file}")
        except Exception as e:
            logging.warning(f"S3 upload failed: {e}")
    
    logging.info("✅ CI/CD Backup completed")
    return True

if __name__ == "__main__":
    exit(0 if backup_for_ci() else 1)