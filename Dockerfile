FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install requests

# Copy the interview deployment yaml and entrypoint script
COPY interview-deployment.yaml .
COPY entrypoint.py .

# Create directory for ConfigMap mount
RUN mkdir -p /etc/app

# Set the default command to run the entrypoint.py
CMD ["python", "entrypoint.py"]

