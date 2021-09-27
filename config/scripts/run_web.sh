#!/bin/bash

cd /app && python manage.py migrate
cd /app && python manage.py loaddata /preload_data/*

cd /app && python manage.py collectstatic --no-input

if [[ "$ENV" == "dev" ]]
then
  python manage.py runserver "$APP_HOST:$APP_PORT"
else
  poetry run uwsgi --ini uwsgi.ini
fi
