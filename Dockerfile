# === BUILDER STAGE ===
FROM python:3.12 as builder

# Set environment variables for Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    PATH="$POETRY_HOME/bin:/opt/venv/bin:$PATH"

# Install Poetry and its dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        # Add build-essential and libpq-dev here for compilation if needed by Python packages
        build-essential \
        libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Copy poetry.lock and pyproject.toml to leverage Docker cache
WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install project dependencies into the virtual environment
# Use --no-root to install only dependencies, not the project itself yet
RUN poetry install --no-root --only main

# Export runtime dependencies to requirements.txt (optional, but good for clarity)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

# === FINAL STAGE ===
FROM python:3.12-slim

# Set environment variables for the application
ENV VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Install runtime system dependencies
# Only install libpq5 for PostgreSQL runtime library
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy the created virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy your application code
WORKDIR /app
COPY . .

# Set the entry point or command to run your application
# For example, if you have a main.py:
# CMD ["python", "main.py"]
# Or if you use uvicorn/gunicorn:
# CMD ["uvicorn", "your_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Replace with your actual startup command