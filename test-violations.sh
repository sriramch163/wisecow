#!/bin/bash

echo "Testing KubeArmor policy violations..."


POD_NAME=$(kubectl get pods -l app=wisecow -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD_NAME" ]; then
    echo "No wisecow pods found. Deploy the application first."
    exit 1
fi

echo "Testing on pod: $POD_NAME"

echo "Test 1: Attempting to run unauthorized command (ls)..."
kubectl exec $POD_NAME -- ls / 2>&1 | head -5


echo "Test 2: Attempting to write to unauthorized location..."
kubectl exec $POD_NAME -- touch /etc/test-file 2>&1 | head -5


echo "Test 3: Attempting unauthorized network access..."
kubectl exec $POD_NAME -- nc -z google.com 80 2>&1 | head -5


echo "Test 4: Verifying allowed operations (fortune + cowsay)..."
kubectl exec $POD_NAME -- /usr/games/fortune | head -2

echo "Policy violation tests completed. Check KubeArmor logs for blocked activities."