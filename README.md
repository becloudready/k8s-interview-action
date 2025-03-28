# 🚀 Kubernetes Troubleshooting Action

This GitHub Action deploys Kubernetes troubleshooting scenarios to help users practice debugging real-world cluster issues.  

It supports multiple failure scenarios, including:  
- 🛑 **Out-of-Memory (OOM)**  
- ❌ **Missing File Errors**  
- 🌐 **DNS Resolution Issues**  
- ⏳ **Slow-Starting Containers**  
- ⚠ **Scheduling Issues**  
- 🖥 **Taints & Tolerations**  
- 🔄 **Affinity/Anti-Affinity Constraints**  

---

## 📌 **Usage**

### **1️⃣ Add to Your Workflow**
```yaml
name: Debug Kubernetes Issues

on:
  workflow_dispatch:
    inputs:
      namespace:
        description: "Namespace to deploy to"
        required: false
        default: "troubleshooting"

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Kubernetes Troubleshooting Action
        uses: becloudready/k8s-interview-action@v1
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}
          namespace: "troubleshooting"
          failure_mode: "oom"
