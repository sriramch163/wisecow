# AWS S3 Backup

## Overview
Automated backup solution for uploading directories to AWS S3 storage.

## Requirements
```bash
pip install boto3
```

## Files
- `backup_aws.py` - AWS S3 backup script

## Configuration

### AWS Credentials
```bash
# Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### GitHub Secrets (for CI/CD)
```
AWS_ACCESS_KEY_ID      # AWS access key
AWS_SECRET_ACCESS_KEY  # AWS secret key
S3_BUCKET             # S3 bucket name
S3_PREFIX             # Optional folder prefix
SOURCE_DIR            # Directory to backup
```

## Usage

### Command Line
```bash
python backup_aws.py /source/dir my-bucket backup-folder
```

### Environment Variables
```bash
export SOURCE_DIR=/app/data
export S3_BUCKET=my-backup-bucket
export S3_PREFIX=daily-backups
python backup_aws.py
```

## Features
- **Recursive Upload**: Backs up entire directory trees
- **Path Preservation**: Maintains folder structure in S3
- **Progress Logging**: Shows upload progress
- **Error Handling**: Comprehensive error reporting
- **Flexible Input**: Command line or environment variables

## Output Format
```
2024-01-15 10:30:15: Uploaded: config/app.conf
2024-01-15 10:30:16: Uploaded: data/users.db
2024-01-15 10:30:20: SUCCESS: S3 backup completed
```

## S3 Structure
```
my-bucket/
├── backup-folder/
│   ├── config/
│   │   └── app.conf
│   └── data/
│       └── users.db
```

## Error Handling
- AWS credential validation
- S3 bucket access verification
- File upload error reporting
- Network connectivity issues

## Integration
- Works with GitHub Actions
- Supports IAM roles in AWS environments
- Compatible with AWS CLI configuration