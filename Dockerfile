ARG BASE_IMAGE=python:3.10-slim-bookworm
FROM $BASE_IMAGE

# system update & package install
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    postgresql-client \
    build-essential \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
WORKDIR .

# pip & requirements
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Configration
EXPOSE 8000

# Execute
CMD ["python", "main.py"]
