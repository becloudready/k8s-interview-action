FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install requests
COPY interview-deployment.yaml .

# Copy the interview script
COPY entrypoint.py .

# Create directory for ConfigMap mount
RUN mkdir -p /etc/app

CMD sh -c "kubectl apply -f interview-deployment.yaml && python ./entrypoint.py"

