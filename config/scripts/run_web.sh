#!/bin/sh

cd /app && python manage.py migrate
cd /app && python manage.py loaddata /preload_data/*

cd /app && python manage.py collectstatic --no-input
