# --- BUILDER STAGE ---
FROM python:3.12 AS builder

WORKDIR /app

# Создание sources.list с зеркалом ftp.debian.org
RUN echo "deb http://ftp.debian.org/debian bookworm main" > /etc/apt/sources.list && \
    echo "deb http://ftp.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

RUN poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

# --- FINAL STAGE ---
FROM python:3.12-slim

WORKDIR /TraumaBot
ENV PYTHONPATH=/TraumaBot

# Создание sources.list с зеркалом ftp.debian.org
RUN echo "deb http://ftp.debian.org/debian bookworm main" > /etc/apt/sources.list && \
    echo "deb http://ftp.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 && \
    rm -rf /var/lib/apt/lists/*


# Copy the created virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
# Set environment variables for the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

COPY . .

COPY traefik-entrypoint.sh /traefik-entrypoint.sh
RUN chmod +x /traefik-entrypoint.sh