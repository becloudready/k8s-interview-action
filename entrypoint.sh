#!/bin/bash

# Set up kubeconfig
echo "$1" > ~/.kube/config

# Apply the Kubernetes resources
kubectl apply -f /action/deployment.yaml
kubectl apply -f /action/configmap.yaml

# Run the Python troubleshooting script
python3 /action/troubleshoot.py
