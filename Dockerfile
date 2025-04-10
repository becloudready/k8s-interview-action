FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install requests
COPY interview-deployment.yaml .

# Copy the interview script
COPY entrypoint.py .

# Create directory for ConfigMap mount
RUN mkdir -p /etc/app

# Create a script to apply the deployment and run the troubleshooting script
RUN echo '#!/bin/sh\nkubectl apply -f interview-deployment.yaml && python ./entrypoint.py' > /start.sh && chmod +x /start.sh

# Set default command to run the script
CMD ["/start.sh"]

