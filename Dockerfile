FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/src"

RUN pip install poetry

WORKDIR $PYSETUP_PATH

RUN mkdir input
RUN mkdir output

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev