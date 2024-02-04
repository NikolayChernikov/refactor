FROM python:3.10

WORKDIR /migrations

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

COPY /migrations ./migrations
COPY /scripts ./scripts
COPY /app ./app