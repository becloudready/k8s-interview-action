# Use a lightweight Python base image
FROM python:3.11-alpine

# Install required dependencies
RUN apk add --no-cache curl bash kubectl

# Set working directory
WORKDIR /app

# Copy entrypoint script
COPY entrypoint.py /app/entrypoint.py

# Make entrypoint executable
RUN chmod +x /app/entrypoint.py

# Set the entrypoint (exec ensures proper signal handling)
ENTRYPOINT ["python3", "/app/entrypoint.py"]
