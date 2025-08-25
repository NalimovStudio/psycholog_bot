# --- BUILDER STAGE ---
FROM python:3.12 AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry>=2.1.4

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

# Copy the created virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
# Set environment variables for the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

COPY . .

COPY traefik-entrypoint.sh /traefik-entrypoint.sh
RUN chmod +x /traefik-entrypoint.sh