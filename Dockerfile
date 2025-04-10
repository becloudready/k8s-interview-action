FROM python:3.11-alpine
 
 # Install required dependencies
 RUN apk add --no-cache curl bash kubectl
 
 # Set working directory
 WORKDIR /app
 
 # Copy entrypoint script
 COPY troubleshoot_scenarios.py /app/troubleshoot_scenarios.py
 
 # Make entrypoint executable
 RUN chmod +x /app/troubleshoot_scenarios.py
 
 # Set the entrypoint (exec ensures proper signal handling)
 ENTRYPOINT ["python3", "/app/troubleshoot_scenarios.py"]

