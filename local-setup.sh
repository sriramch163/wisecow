#!/bin/bash

# Local setup script for Minikube cluster in Git Bash

echo "=== STEP 1: Using workflow-generated kubeconfig ==="
if [ -f "kubeconfig.yaml" ]; then
    export KUBECONFIG="$(pwd)/kubeconfig.yaml"
    echo "Using workflow kubeconfig: $(pwd)/kubeconfig.yaml"
else
    echo "kubeconfig.yaml not found! Download from GitHub Actions artifacts first."
    exit 1
fi

echo "=== STEP 2: Starting Minikube cluster ==="
minikube start --driver=docker

echo "=== STEP 3: Enabling ingress addon ==="
minikube addons enable ingress

echo "=== STEP 4: Starting Minikube tunnel (requires admin) ==="
minikube tunnel &
TUNNEL_PID=$!
echo $TUNNEL_PID > tunnel.pid
sleep 10

echo "=== STEP 5: Adding wisecow.local to hosts file ==="
echo "127.0.0.1 wisecow.local" >> /c/Windows/System32/drivers/etc/hosts

echo "=== STEP 6: Creating TLS secret ==="
kubectl create secret tls wisecow-tls --cert=tls/tls.crt --key=tls/tls.key --dry-run=client -o yaml | kubectl apply -f -

echo "=== STEP 7: Deploying wisecow application ==="
kubectl apply -f k8s/

echo "=== STEP 8: Waiting for ingress controller ==="
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=300s

echo "=== STEP 9: Waiting for application pods ==="
kubectl wait --for=condition=ready pod -l app=wisecow --timeout=300s

echo "=== STEP 10: Checking deployment status ==="
kubectl get pods
kubectl get svc
kubectl get ingress

echo ""
echo "=== DEPLOYMENT COMPLETE ==="
echo "✅ Access app at: https://wisecow.local"
echo "✅ Kubeconfig: export KUBECONFIG=$(pwd)/kubeconfig-local.yaml"
echo "✅ Stop tunnel: kill $(cat tunnel.pid)"
echo "✅ Stop Minikube: minikube stop"