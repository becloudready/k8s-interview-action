FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates gnupg && \
    rm -rf /var/lib/apt/lists/*

# Download and install kubectl (with checksum verification)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256" && \
    echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl kubectl.sha256

# Copy action files

WORKDIR /action
COPY deployment.yaml configmap.yaml troubleshoot.py entrypoint.sh ./
# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/action/entrypoint.sh"]
