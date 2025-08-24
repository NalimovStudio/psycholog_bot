# --- BUILDER STAGE ---
FROM python:3.12 as builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        # Add build-essential and libpq-dev here for compilation if needed by Python packages (like complile C-code)
        build-essential \
        libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/* \

RUN pip install "poetry==2.1.4"

# Copy only the Poetry configuration files first
# This allows Docker to cache this layer if pyproject.toml and poetry.lock don't change
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

# Export dependencies to a requirements.txt file
# --only main ensures only main dependencies are included (no dev)
# --without-hashes is often needed for compatibility with pip in Docker,
# though using hashes is more secure if you can manage it.
RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Create a virtual environment and install dependencies into it
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt


# --- FINAL STAGE ---
FROM python:3.12-slim

WORKDIR /TraumaBot
ENV PYTHONPATH=/TraumaBot

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    echo "nameserver 1.1.1.1" >> /etc/resolv.conf \

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        && rm -rf /var/lib/apt/lists/*

# Copy the created virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
# Set environment variables for the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

COPY . .

RUN ls -la /traefik-entrypoint.sh

RUN chmod +x traefik-entrypoint.sh