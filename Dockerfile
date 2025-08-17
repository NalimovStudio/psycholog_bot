FROM python:3.12-slim

WORKDIR /trauma_project

RUN pip install --no-cache-dir --retries=5 --default-timeout=25 poetry

COPY pyproject.toml poetry.lock README.md ./

# Добавляем --no-root
RUN poetry install --only main --no-interaction --no-ansi

COPY . .

# Используем poetry run для гарантии доступа к зависимостям
CMD ["poetry", "run", "python", "source/main/bot.py"]