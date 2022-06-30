#!/bin/bash

cd /code/kotti

python manage.py makemigrations --noinput
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput

gunicorn kotti.wsgi:application --bind 0.0.0.0:8000 --workers 4