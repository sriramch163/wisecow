# File Organization

## CI/CD Files (`/cicd/`)
**Purpose**: Optimized for automated workflows

| File | Purpose |
|------|---------|
| `system_monitor_ci.py` | Lightweight health check (70% thresholds) |
| `backup_ci.py` | Artifact backup to S3 |
| `requirements-ci.txt` | CI/CD dependencies |

**Usage in Workflows**:
```yaml
- run: pip install -r cicd/requirements-ci.txt
- run: python cicd/system_monitor_ci.py
- run: python cicd/backup_ci.py
```

## Local Files (`/local/`)
**Purpose**: Detailed local development and testing

| File | Purpose |
|------|---------|
| `system_monitor_local.py` | Detailed monitoring (85% thresholds) |
| `backup_local.py` | Full backup with test data creation |
| `run_local.py` | Python runner script |
| `run_local.bat` | Windows batch runner |
| `requirements-local.txt` | Local dependencies |

**Local Execution**:
```bash
# Python (recommended)
cd local && python run_local.py

# Windows
cd local && run_local.bat

# Individual scripts
cd local && python system_monitor_local.py
cd local && python backup_local.py
```

## Key Differences

| Aspect | CI/CD | Local |
|--------|-------|-------|
| **Thresholds** | Strict (70%) | Relaxed (85%) |
| **Logging** | Console only | File + Console |
| **Data** | Real artifacts | Creates test data |
| **Backup** | S3 focused | Local + optional S3 |
| **Purpose** | Pipeline validation | Development/testing |

## Migration from Root Files
- `system_monitor.py` → `cicd/system_monitor_ci.py` + `local/system_monitor_local.py`
- `backup_solution.py` → `cicd/backup_ci.py` + `local/backup_local.py`
- `requirements.txt` → `cicd/requirements-ci.txt` + `local/requirements-local.txt`
- `run_monitoring.sh/.bat` → `local/run_local.py/.bat`