FROM python:3.11-alpine
 
 # Install required dependencies
RUN apk add --no-cache \
    curl \
    bash \
    ca-certificates

# Install kubectl (latest stable)
RUN curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && mv kubectl /usr/local/bin/kubectl && \
    kubectl version --client
 
 # Set working directory
 WORKDIR /app
 
 # Copy entrypoint script
 COPY entrypoint.py /app/entrypoint.py
 
 # Make entrypoint executable
 RUN chmod +x /app/entrypoint.py
 
 # Set the entrypoint (exec ensures proper signal handling)
 ENTRYPOINT ["python3", "/app/entrypoint.py"]
