FROM python:3.12-slim

# тут создается папка с проектом (на самом высоком уровне), которая уже пихает в себя все остальные файлы
WORKDIR /trauma_project

ENV PYTHONPATH=/trauma_project

# Устанавливаем Poetry с отключением виртуального окружения
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости (без текущего проекта)
RUN poetry install --only main --no-root --no-interaction --no-ansi

# Копируем весь код
COPY . .