#!/usr/bin/env python3
import boto3
import os
import sys
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp}: {message}")

def backup_to_s3(source_dir, bucket_name, prefix=""):
    s3 = boto3.client('s3')
    
    try:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, source_dir)
                s3_key = f"{prefix}/{relative_path}".replace("\\", "/")
                
                s3.upload_file(local_path, bucket_name, s3_key)
                log_message(f"Uploaded: {relative_path}")
        
        log_message("SUCCESS: S3 backup completed")
        return True
        
    except Exception as e:
        log_message(f"ERROR: S3 backup failed: {str(e)}")
        return False

if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else os.getenv('SOURCE_DIR')
    bucket = sys.argv[2] if len(sys.argv) > 2 else os.getenv('S3_BUCKET')
    prefix = sys.argv[3] if len(sys.argv) > 3 else os.getenv('S3_PREFIX', '')
    
    success = backup_to_s3(source, bucket, prefix)
    sys.exit(0 if success else 1)