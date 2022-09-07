FROM python:3.8

WORKDIR /code
COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY . /code
