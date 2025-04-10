FROM python:3.9-slim


# Copy action files
COPY deployment.yaml /action/deployment.yaml
COPY configmap.yaml /action/configmap.yaml
COPY troubleshoot.py /action/troubleshoot.py
COPY entrypoint.sh /action/entrypoint.sh

ENTRYPOINT ["/bin/bash", "/action/entrypoint.sh"]

