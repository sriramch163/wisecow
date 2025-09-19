#!/usr/bin/env python3
import os
import sys
import tarfile
import boto3
import subprocess
import json
from datetime import datetime

def create_archive(source_dir, backup_name):
    """Create tar.gz archive"""
    try:
        with tarfile.open(f"{backup_name}.tar.gz", "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        return f"{backup_name}.tar.gz"
    except Exception as e:
        raise Exception(f"Archive failed: {str(e)}")

def upload_s3(file_path, bucket, key):
    """Upload to S3"""
    try:
        s3 = boto3.client('s3')
        s3.upload_file(file_path, bucket, key)
        return f"s3://{bucket}/{key}"
    except Exception as e:
        raise Exception(f"S3 upload failed: {str(e)}")

def upload_remote(file_path, host, path, key=None):
    """Upload to remote server"""
    try:
        cmd = ["scp"]
        if key:
            cmd.extend(["-i", key])
        cmd.extend([file_path, f"{host}:{path}"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"SCP failed: {result.stderr}")
        return f"{host}:{path}"
    except Exception as e:
        raise Exception(f"Remote upload failed: {str(e)}")

def generate_report(status, details, location=None):
    """Generate backup report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "details": details,
        "backup_location": location
    }
    
    with open("backup_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"BACKUP {status.upper()}")
    print(f"Time: {report['timestamp']}")
    print(f"Details: {details}")
    if location:
        print(f"Location: {location}")

def main():
    source_dir = os.getenv('SOURCE_DIR', sys.argv[1] if len(sys.argv) > 1 else './artifacts')
    storage_type = os.getenv('STORAGE_TYPE', 's3')
    destination = os.getenv('DESTINATION', os.getenv('S3_BUCKET', 'backup-bucket/ci-backups'))
    
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        if not os.path.exists(source_dir):
            raise Exception(f"Source directory not found: {source_dir}")
        
        archive_path = create_archive(source_dir, backup_name)
        
        if storage_type == "s3":
            bucket, key = destination.split("/", 1)
            location = upload_s3(archive_path, bucket, f"{key}/{os.path.basename(archive_path)}")
        elif storage_type == "remote":
            host, path = destination.split(":", 1)
            ssh_key = os.getenv('SSH_KEY')
            location = upload_remote(archive_path, host, path, ssh_key)
        else:
            raise Exception(f"Unsupported storage type: {storage_type}")
        
        generate_report("success", "Backup completed successfully", location)
        
    except Exception as e:
        generate_report("failed", str(e))
        sys.exit(1)
    finally:
        if os.path.exists(f"{backup_name}.tar.gz"):
            os.remove(f"{backup_name}.tar.gz")

if __name__ == "__main__":
    main()