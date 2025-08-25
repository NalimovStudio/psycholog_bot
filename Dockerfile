FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry>=2.1.4

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Python
RUN poetry install --no-interaction --no-root

# Копируем весь код
COPY . .

# Делаем скрипт исполняемым
RUN chmod +x traefik-entrypoint.sh

# Создаем симлинки для обратной совместимости
RUN ln -sf /app /TraumaBot && \
    ln -sf /app /source

# Команда по умолчанию
CMD ["poetry", "run", "python", "-m", "source.main.bot"]