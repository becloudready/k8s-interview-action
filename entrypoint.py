#!/usr/bin/env python3

import os
import subprocess
import sys

def run_command(command):
    """Run shell commands safely and capture output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {command}\n{e.stderr}")
        sys.exit(1)

def setup_kubeconfig():
    """Set up Kubernetes configuration from environment variable."""
    print("🔹 Setting up Kubernetes configuration")
    kubeconfig = os.getenv("KUBECONFIG", "")

    if not kubeconfig:
        print("❌ KUBECONFIG environment variable is missing!")
        sys.exit(1)

    os.makedirs(os.path.expanduser("~/.kube"), exist_ok=True)
    kubeconfig_path = os.path.expanduser("~/.kube/config")

    # Directly write the KUBECONFIG secret to the kubeconfig file
    with open(kubeconfig_path, "w") as f:
        f.write(kubeconfig)

    os.environ["KUBECONFIG"] = kubeconfig_path
    run_command("kubectl version --client")
    run_command("kubectl cluster-info")

def deploy_scenario(name, yaml_content):
    """Deploy a given Kubernetes scenario."""
    print(f"🔹 Deploying {name}")
    command = f"echo '{yaml_content}' | kubectl apply -n {namespace} -f -"
    run_command(command)

def verify_deployments():
    """Verify that deployments are created successfully."""
    print("🔹 Verifying deployments")
    run_command(f"kubectl get deployments -n {namespace}")

# Get namespace from environment variable or use default
namespace = os.getenv("NAMESPACE", "troubleshooting-scenarios")

def main():
    setup_kubeconfig()

    print(f"🔹 Ensuring namespace: {namespace}")
    run_command(f"kubectl create namespace {namespace} --dry-run=client -o yaml | kubectl apply -f -")

    # Define YAML manifests for different troubleshooting scenarios
    oom_scenario = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oom-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: oom-app
  template:
    metadata:
      labels:
        app: oom-app
    spec:
      containers:
      - name: oom-container
        image: becloudready/k8s-troubleshooting-scenarios:2.0.0
        env:
        - name: FAILURE_MODE
          value: "oom"
        resources:
          limits:
            memory: "128Mi"
    """

    missing_file_scenario = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: missing-file-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: missing-file-app
  template:
    metadata:
      labels:
        app: missing-file-app
    spec:
      containers:
      - name: missing-file-container
        image: becloudready/k8s-troubleshooting-scenarios:2.0.0
        env:
        - name: FAILURE_MODE
          value: "missing_file"
    """

    dns_issues_scenario = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dns-issues-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dns-issues-app
  template:
    metadata:
      labels:
        app: dns-issues-app
    spec:
      dnsPolicy: Default
      containers:
      - name: dns-issues-container
        image: becloudready/k8s-troubleshooting-scenarios:2.0.0
        env:
        - name: FAILURE_MODE
          value: "dns"
    """

    scheduling_issue_scenario = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scheduling-issue-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: scheduling-issue-app
  template:
    metadata:
      labels:
        app: scheduling-issue-app
    spec:
      nodeSelector:
        non-existent-label: "true"
      containers:
      - name: scheduling-issue-container
        image: becloudready/k8s-troubleshooting-scenarios:2.0.0
    """

    taint_toleration_scenario = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tolerations-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tolerations-app
  template:
    metadata:
      labels:
        app: tolerations-app
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "gpu"
        effect: "NoSchedule"
      containers:
      - name: tolerations-container
        image: becloudready/k8s-troubleshooting-scenarios:2.0.0
    """

    affinity_scenario = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: affinity-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: affinity-app
  template:
    metadata:
      labels:
        app: affinity-app
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - affinity-app
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: affinity-container
        image: becloudready/k8s-troubleshooting-scenarios:2.0.0
    """

    # Deploy Scenarios
    deploy_scenario("Out-of-Memory (OOM) scenario", oom_scenario)
    deploy_scenario("Missing File scenario", missing_file_scenario)
    deploy_scenario("DNS Issues scenario", dns_issues_scenario)
    deploy_scenario("Scheduling Issue scenario", scheduling_issue_scenario)
    deploy_scenario("Taint/Toleration scenario", taint_toleration_scenario)
    deploy_scenario("Affinity/Anti-Affinity scenario", affinity_scenario)

    # Verify Deployments
    verify_deployments()

if __name__ == "__main__":
    main()
