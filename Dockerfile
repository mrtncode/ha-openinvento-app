FROM ghcr.io/openinvento/openinvento:latest

COPY run.py /run.py

# Preserve the upstream image's CMD and run it with values from Supervisor options.
ENTRYPOINT ["python3", "/run.py"]
