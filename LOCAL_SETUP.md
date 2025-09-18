# Local Setup Guide

## Quick Start

### Option 1: Python Script (Recommended)
```bash
python local_setup.py
```

### Option 2: Shell Script (Linux/Mac)
```bash
chmod +x run_monitoring.sh
./run_monitoring.sh
```

### Option 3: Batch File (Windows)
```cmd
run_monitoring.bat
```

## Manual Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Health Check Only
```bash
python system_monitor.py
```

### 3. Run Backup Only
```bash
# Set source directory
export SOURCE_DIR=./k8s
export BACKUP_DIR=./backups

python backup_solution.py
```

### 4. Run Both with Custom Settings
```bash
export CPU_THRESHOLD=75
export MEMORY_THRESHOLD=85
export SOURCE_DIR=./test-data
export BACKUP_DIR=./backups

python system_monitor.py
python backup_solution.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| CPU_THRESHOLD | 80 | CPU usage alert threshold |
| MEMORY_THRESHOLD | 80 | Memory usage alert threshold |
| DISK_THRESHOLD | 80 | Disk usage alert threshold |
| SOURCE_DIR | ./k8s | Directory to backup |
| BACKUP_DIR | ./backups | Local backup storage |
| S3_BUCKET | - | AWS S3 bucket (optional) |

## Output Files
- `system_health.log` - Health monitoring logs
- `backup.log` - Backup operation logs
- `./backups/` - Local backup files
- `./test-data/` - Sample data (created by local_setup.py)

## AWS S3 Setup (Optional)
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export S3_BUCKET=your-bucket
export AWS_DEFAULT_REGION=us-east-1
```