#!/bin/sh

cd /app && python manage.py migrate
cd /app && python manage.py loaddata /preload_data/*
cd /app && uwsgi --ini uwsgi.ini