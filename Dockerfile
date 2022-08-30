FROM python:3.8

WORKDIR /code
COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY . /code
#
#RUN poetry run python manage.py migrate
#CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8121", "pug_project.wsgi"]