# Backup CI/CD

## Overview
Automated backup solution for CI/CD pipelines using rsync and GitHub Actions.

## Requirements
- rsync installed on runner
- SSH access to remote server
- GitHub repository secrets configured

## Files
- `backup_cicd.sh` - CI/CD optimized backup script
- `.github/workflows/backup.yml` - GitHub Actions workflow

## Configuration

### GitHub Secrets
```
SSH_PRIVATE_KEY    # SSH private key for remote access
REMOTE_HOST        # Remote server hostname
REMOTE_USER        # Remote server username
REMOTE_DIR         # Remote backup directory path
SOURCE_DIR         # Source directory to backup
```

## Usage

### Manual Execution
```bash
./backup_cicd.sh /source/path user@server.com /backup/path
```

### GitHub Actions
- Runs daily at 2 AM UTC
- Manual trigger via workflow_dispatch
- Automatic on push to main branch

## Features
- **rsync**: Efficient incremental backups
- **SSH**: Secure remote transfer
- **Logging**: Timestamped backup reports
- **GitHub Annotations**: Success/error notifications
- **Artifacts**: Backup logs uploaded

## Output Format
```
2024-01-15 02:00:15: Starting backup: /app/data -> user@server.com:/backups
2024-01-15 02:01:45: SUCCESS: Backup completed successfully
```

## Workflow Triggers
- `schedule`: Daily at 2 AM UTC
- `workflow_dispatch`: Manual trigger
- `push`: On main branch changes

## Error Handling
- Source directory validation
- SSH connection verification
- rsync exit code checking
- GitHub Actions failure notifications

## Log Files
- `backup.log` - Local backup operations log
- GitHub Actions artifacts for audit trail