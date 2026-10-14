FROM ghcr.io/openinvento/openinvento:latest

COPY run.py /run.py

# The wrapper exports Supervisor options, then execs the upstream entrypoint.
ENTRYPOINT ["python3", "/run.py"]
