# Kubernetes Interview Troubleshooting Action

This GitHub Action simulates DNS and ConfigMap issues in a Kubernetes environment and helps troubleshoot them. It allows you to simulate common Kubernetes issues like misconfigured DNS and incorrect ConfigMap references to aid in debugging and testing Kubernetes deployments.

## Features

- Simulates DNS misconfigurations using a custom DNS policy and invalid nameservers.
- Simulates a ConfigMap error by referencing a non-existent key in the deployment.
- Provides a Python script to troubleshoot and detect the simulated issues.
- Can be triggered manually through GitHub Actions' `workflow_dispatch`.

## Prerequisites

- A valid Kubernetes `kubeconfig` file to authenticate with your cluster. The `kubeconfig` should be stored as a GitHub secret.

## Setup

### Step 1: Store `kubeconfig` as a GitHub Secret

1. Go to your GitHub repository.
2. Navigate to **Settings** > **Secrets** > **New repository secret**.
3. Name the secret `KUBECONFIG` and paste the content of your `kubeconfig` file.

### Step 2: Define the Workflow in Your Repository

In your repository, create a GitHub Actions workflow to use the `k8s-interview-action`. Create the file `.github/workflows/k8s-interview.yml` with the following content:

```yaml
name: 'Kubernetes Interview Troubleshooting'

on:
  workflow_dispatch:  # Only triggers when manually initiated from the GitHub UI

jobs:
  run-interview-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Use Kubernetes Troubleshooting Action
        uses: becloudready/k8s-interview-action@v10
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}


