FROM python:3.9-slim

# Install necessary dependencies including gnupg for adding the Kubernetes APT key
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    && curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /etc/apt/trusted.gpg.d/kubernetes.asc \
    && echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list \
    && apt-get update \
    && apt-get install -y kubectl

# Install other dependencies like requests
RUN pip install kubernetes
# Copy action files
COPY deployment.yaml /action/deployment.yaml
COPY configmap.yaml /action/configmap.yaml
COPY troubleshoot.py /action/troubleshoot.py
COPY entrypoint.sh /action/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/action/entrypoint.sh"]

