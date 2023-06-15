FROM python:3.10-slim

# set work directory
WORKDIR /src

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/src

# install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-cache --no-interaction

# copy project
COPY . .

RUN chmod a+x /src/docker_commands/gunicorn.sh
RUN chmod a+x /src/docker_commands/celery.sh

