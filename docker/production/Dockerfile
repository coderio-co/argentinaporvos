FROM python:3.7-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install gdal-bin postgresql-client -y \
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./docker/production/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY . /code/

EXPOSE 8000
