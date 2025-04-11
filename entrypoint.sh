#!/bin/bash
kubectl get pods -A
echo "🚀 Applying Kubernetes manifests..."
kubectl apply -f configmap.yaml || echo "⚠️ ConfigMap apply failed"
kubectl apply -f deployment.yaml || echo "⚠️ Deployment apply failed"

echo "🐍 Running Python Troubleshooter..."
python3 troubleshoot.py



# Run the Python troubleshooting script
python3 /action/troubleshoot.py
