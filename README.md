# Cow wisdom web server

## Prerequisites

```
sudo apt install fortune-mod cowsay -y
```

## How to use?

1. Run `./wisecow.sh`
2. Point the browser to server port (default 4499)

## What to expect?
![wisecow](https://github.com/nyrahul/wisecow/assets/9133227/8d6bfde3-4a5a-480e-8d55-3fef60300d98)

# Problem Statement
Deploy the wisecow application as a k8s app

## Features Implemented
✅ Dockerfile and Kubernetes manifests  
✅ GitHub Actions CI/CD pipeline  
✅ Continuous Deployment to Kubernetes  
✅ TLS/HTTPS support with cert-manager  

## Quick Deploy
```bash
# Update domain in k8s/wisecow-ingress.yaml and k8s/cert-manager.yaml
./deploy.sh
```

## GitHub Secrets Required
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password  
- `KUBECONFIG`: Base64 encoded kubeconfig for deployment

## TLS Setup
1. Install NGINX Ingress Controller
2. Update domain in `k8s/wisecow-ingress.yaml`
3. Update email in `k8s/cert-manager.yaml`
4. Deploy using `./deploy.sh`
