FROM python:3.7

RUN apt-get update -y
RUN apt-get install -y python-pip
RUN pip install poetry

COPY ./app/pyproject.toml /app/pyproject.toml
COPY ./app/poetry.lock /app/poetry.lock

WORKDIR /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# CMD ["python", "/app/init.py"]