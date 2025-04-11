#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile

def run_command(command):
    """Run shell commands safely and capture output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")
        sys.exit(1)


def deploy_faulty_yaml():
    """Deploy the DNS + ConfigMap issue scenario."""
    print("🔹 Deploying DNS + ConfigMap issue scenario")

    yaml_content = r"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: interview-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: interview
  template:
    metadata:
      labels:
        app: interview
    spec:
      dnsPolicy: "Default"
      dnsConfig:
        nameservers:
          - "203.0.113.123"
        searches:
          - google.com
        options:
         - name: ndots
           value: "1"
      containers:
      - name: main
        image: becloudready/k8s-troubleshooting-scenarios:7.0.0
        command: ["python3", "/app/troubleshoot_scenarios.py"]
        volumeMounts:
        - name: config-vol
          mountPath: /etc/app
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
      volumes:
      - name: config-vol
        configMap:
          name: app-config
          items:
          - key: config1.yml
            path: config.yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  config.yml: |
    database:
      host: db-service
      port: 5432
    logging:
      level: debug
    """

    with tempfile.NamedTemporaryFile("w", delete=False) as temp_yaml:
        temp_yaml.write(yaml_content)
        temp_path = temp_yaml.name

    run_command(f"kubectl apply -f {temp_path}")

def verify_pods():
    """Fetch pod and logs to confirm error behavior."""
    print("🔹 Verifying pod status and logs...")
    run_command("kubectl get pods -o wide")

    result = subprocess.run(
        "kubectl get pods --no-headers -o custom-columns=\":metadata.name\"",
        shell=True, capture_output=True, text=True
    )
    pod_name = result.stdout.strip().split("\n")[0]

    if pod_name:
        print(f"🔹 Logs from pod: {pod_name}")
        run_command(f"kubectl logs {pod_name} || true")
    else:
        print("❌ No pod found to get logs from.")

def main():
    deploy_faulty_yaml()
    verify_pods()

if __name__ == "__main__":
    main()


