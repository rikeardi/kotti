#!/bin/bash

cd /code/kotti

python manage.py makemigrations --noinput
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py runserver 0.0.0.0:8000