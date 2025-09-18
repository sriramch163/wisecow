@echo off
echo === LOCAL SYSTEM OPERATIONS ===

REM Install dependencies
pip install -r requirements-local.txt

REM Set local environment
set CPU_THRESHOLD=85
set MEMORY_THRESHOLD=85
set DISK_THRESHOLD=85
set SOURCE_DIR=.\test-data
set BACKUP_DIR=.\backups

echo.
echo 1. Running health check...
python system_monitor_local.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 2. Running backup...
    python backup_local.py
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo 🎉 All local operations completed!
        echo Check local_health.log and local_backup.log for details
        echo Backup files are in .\backups\
    ) else (
        echo.
        echo ❌ Backup failed
        exit /b 1
    )
) else (
    echo.
    echo ❌ Health check failed
    exit /b 1
)