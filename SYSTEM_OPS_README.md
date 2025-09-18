# System Operations Scripts

## Overview
Automated system health monitoring and backup solution with CI/CD integration.

## Scripts

### 1. System Health Monitor (`system_monitor.py`)
Monitors system resources and alerts on threshold breaches.

**Checks:**
- CPU usage > 80%
- Memory usage > 80% 
- Disk usage > 80%
- Critical processes running

**Usage:**
```bash
python system_monitor.py
```

**Environment Variables:**
```bash
export CPU_THRESHOLD=80
export MEMORY_THRESHOLD=80
export DISK_THRESHOLD=80
```

### 2. Backup Solution (`backup_solution.py`)
Automated backup with local and cloud storage support.

**Features:**
- Creates compressed tar.gz backups
- Uploads to AWS S3 (optional)
- Automatic cleanup of old backups
- Comprehensive logging

**Usage:**
```bash
export SOURCE_DIR=/app/data
export S3_BUCKET=my-backup-bucket
python backup_solution.py
```

## Quick Start

### Local Execution
```bash
# Install dependencies
pip install -r requirements.txt

# Run both scripts
./run_monitoring.sh
```

### CI/CD Integration
The workflow runs automatically:
- Every 6 hours (scheduled)
- On script changes (push trigger)
- Manual trigger via GitHub Actions

## GitHub Secrets Required
```
AWS_ACCESS_KEY_ID      # AWS access key
AWS_SECRET_ACCESS_KEY  # AWS secret key  
S3_BUCKET             # S3 bucket name
```

## Output Files
- `system_health.log` - Health monitoring logs
- `backup.log` - Backup operation logs
- `/tmp/backups/` - Local backup files

## Monitoring Thresholds
| Metric | Default | Environment Variable |
|--------|---------|---------------------|
| CPU    | 80%     | CPU_THRESHOLD       |
| Memory | 80%     | MEMORY_THRESHOLD    |
| Disk   | 80%     | DISK_THRESHOLD      |

## Backup Configuration
| Setting | Default | Environment Variable |
|---------|---------|---------------------|
| Source  | /app/data | SOURCE_DIR        |
| Local   | /tmp/backups | BACKUP_DIR     |
| Retention | 7 days | -                 |

## Integration Examples

### Kubernetes CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: system-ops
spec:
  schedule: "0 */6 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: system-ops
            image: python:3.11-slim
            command: ["./run_monitoring.sh"]
            env:
            - name: SOURCE_DIR
              value: "/app/data"
```

### Docker Compose
```yaml
services:
  system-ops:
    build: .
    environment:
      - CPU_THRESHOLD=75
      - S3_BUCKET=my-backups
    volumes:
      - ./data:/app/data
    command: ./run_monitoring.sh
```