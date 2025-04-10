FROM python:3.9-slim

# Install kubectl
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https \
    ca-certificates \
    && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | tee -a /etc/apt/sources.list.d/kubernetes.list \
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

