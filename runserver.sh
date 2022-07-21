#!/bin/bash

cd /code/kotti/docs

sphinx-apidoc -o . ..
make html

cd /code/kotti

python manage.py makemigrations --noinput
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput

python manage.py runserver 0.0.0.0:8000
#gunicorn kotti.wsgi:application --bind 0.0.0.0:8000 --workers 4