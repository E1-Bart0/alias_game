FROM python:3.9
WORKDIR /app

COPY ./.requirements /.requirements
COPY ./preload_data /preload_data

RUN pip install --no-cache-dir -r /.requirements/common.txt


COPY ./alias /app
COPY ./uwsgi.ini /app

COPY ./scripts /app