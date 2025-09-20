#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py createsuperuser --noinput || true
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 project.wsgi:application
