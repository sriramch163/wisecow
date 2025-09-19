# Wisecow Project Structure & Workflow

## 📁 Directory Structure

```
demo/
├── .github/workflows/          # GitHub Actions CI/CD
│   ├── main-pipeline.yml       # Main orchestration pipeline
│   ├── docker-build.yml        # Docker build & K8s deploy
│   └── system-ops.yml          # Health monitoring & backup
├── cicd/                       # CI/CD utilities
│   ├── health_monitor.py       # System health checker
│   ├── backup_ci.py           # CI backup solution
│   ├── requirements-ci.txt     # CI dependencies
│   └── requirements-backup.txt # Backup dependencies
├── k8s/                        # Kubernetes manifests
│   ├── wisecow-deployment.yaml # App deployment
│   ├── wisecow-service.yaml    # Service definition
│   └── wisecow-ingress.yaml    # Ingress with TLS
├── local/                      # Local development tools
│   ├── run_local.py           # Local runner script
│   ├── system_monitor_local.py # Local health monitor
│   ├── backup_local.py        # Local backup tool
│   ├── run_local.bat          # Windows batch runner
│   └── requirements-local.txt # Local dependencies
├── tls/                        # TLS certificates
│   ├── tls.crt                # SSL certificate
│   └── tls.key                # SSL private key
├── wisecow.sh                  # Main application script
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Local Docker setup
├── local-setup.sh             # Local setup script
├── LOCAL_SETUP.md             # Local setup guide
└── README.md                  # Main documentation
```

## 🔧 Required Components by Directory

### Root Directory
- **wisecow.sh**: Main bash application serving cow wisdom on port 4499
- **Dockerfile**: Multi-stage container build with Ubuntu base
- **docker-compose.yml**: Local development container setup

### .github/workflows/
**Required GitHub Secrets:**
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password
- `AWS_ACCESS_KEY_ID`: AWS access key (optional for S3 backup)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (optional)
- `BACKUP_S3_BUCKET`: S3 bucket name (optional)

**Workflow Files:**
- `main-pipeline.yml`: Orchestrates build → system operations
- `docker-build.yml`: Builds Docker image, deploys to Minikube
- `system-ops.yml`: Runs health checks and backups every 6 hours

### k8s/
**Kubernetes Resources:**
- `wisecow-deployment.yaml`: 2 replicas, resource limits
- `wisecow-service.yaml`: ClusterIP service on port 4499
- `wisecow-ingress.yaml`: NGINX ingress with TLS termination

**Required Updates:**
- Update `wisecow.local` domain in ingress.yaml
- Update Docker image name in deployment.yaml

### cicd/
**Python Dependencies:**
- `psutil`: System monitoring
- `boto3`: AWS S3 integration (optional)

**Scripts:**
- `health_monitor.py`: CPU/Memory/Disk monitoring
- `backup_ci.py`: Automated backup with S3 support

### local/
**Local Development Tools:**
- `run_local.py`: Main local runner
- `system_monitor_local.py`: Local health monitoring
- `backup_local.py`: Local backup solution
- `run_local.bat`: Windows execution wrapper

### tls/
**TLS Certificates:**
- `tls.crt`: SSL certificate for HTTPS
- `tls.key`: Private key for SSL

## 🔄 Workflow Explanation

### 1. Development Workflow
```
Code Push → GitHub → Docker Build → Minikube Deploy → Health Check → Backup
```

### 2. CI/CD Pipeline Flow

#### Main Pipeline (main-pipeline.yml)
```
Push to main branch
├── Trigger docker-build.yml
│   ├── Build Docker image
│   ├── Push to Docker Hub
│   ├── Deploy to Minikube
│   └── Test HTTPS endpoint
└── Trigger system-ops.yml
    ├── Health monitoring
    ├── Backup creation
    └── S3 upload (optional)
```

#### Docker Build Pipeline (docker-build.yml)
```
1. Checkout code
2. Login to Docker Hub
3. Build & push image (latest + build number tags)
4. Setup Minikube with ingress addon
5. Start tunnel for LoadBalancer
6. Update /etc/hosts with domain mapping
7. Create TLS secret from certificates
8. Deploy K8s manifests
9. Wait for pods ready
10. Test HTTPS endpoint
```

#### System Operations (system-ops.yml)
```
Scheduled every 6 hours:
1. Health Check Job
   ├── Install Python dependencies
   ├── Run health_monitor.py
   └── Upload health logs
2. Backup Job
   ├── Create backup archive
   ├── Upload to S3 (if configured)
   └── Store as GitHub artifact
3. Notification Job
   └── Report job statuses
```

### 3. Local Development Flow
```
Local Setup:
├── Install dependencies (requirements-local.txt)
├── Run system_monitor_local.py
├── Run backup_local.py
└── Check logs (local_health.log, local_backup.log)
```

## 🚀 Quick Start Guide

### Prerequisites
- Docker & Docker Hub account
- Kubernetes cluster (Minikube for CI)
- Python 3.11+
- GitHub repository with secrets configured

### 1. GitHub Setup
```bash
# Set required secrets in GitHub repository settings
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password
```

### 2. Local Development
```bash
# Option 1: Python runner
python local/run_local.py

# Option 2: Windows batch
local/run_local.bat

# Option 3: Manual
pip install -r local/requirements-local.txt
python local/system_monitor_local.py
python local/backup_local.py
```

### 3. Kubernetes Deployment
```bash
# Update domain in k8s/wisecow-ingress.yaml
# Update image name in k8s/wisecow-deployment.yaml
kubectl apply -f k8s/
```

### 4. Docker Compose (Local)
```bash
docker-compose up -d
curl http://localhost:4499
```

## 🔍 Monitoring & Health Checks

### Health Metrics Monitored
- **CPU Usage**: Alert if > 80%
- **Memory Usage**: Alert if > 80%
- **Disk Usage**: Alert if > 80%
- **Process Count**: Alert if > 200

### Backup Strategy
- **Local**: ./backups/ directory
- **CI**: GitHub Artifacts + optional S3
- **Schedule**: Every 6 hours via GitHub Actions
- **Retention**: Configurable per storage type

## 🔐 Security Features

### TLS/HTTPS
- Self-signed certificates in tls/ directory
- NGINX ingress with SSL termination
- Automatic HTTP → HTTPS redirect

### Container Security
- Non-root user execution
- Minimal Ubuntu base image
- Resource limits enforced

## 📊 Outputs & Artifacts

### Log Files
- `health-logs/health-YYYYMMDD.log`: Health check results
- `local_health.log`: Local health monitoring
- `local_backup.log`: Local backup operations

### Backup Files
- `./backups/`: Local backup storage
- GitHub Artifacts: CI backup storage
- S3 bucket: Optional cloud backup

### Monitoring Reports
- `backup_report.json`: Backup operation status
- GitHub Actions logs: CI/CD pipeline status

## 🛠️ Customization

### Environment Variables
```bash
# Health thresholds
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
DISK_THRESHOLD=80
PROCESS_LIMIT = 200

# Backup settings
SOURCE_DIR=./k8s
BACKUP_DIR=./backups
S3_BUCKET=your-backup-bucket

# Application settings
SRVPORT=4499
TLS_ENABLED=false
```

### Domain Configuration
1. Update `wisecow.local` in `k8s/wisecow-ingress.yaml`
2. Update `/etc/hosts` or DNS records
3. Generate new TLS certificates if needed

This structure provides a complete DevOps pipeline with containerization, Kubernetes deployment, automated testing, health monitoring, and backup solutions.