#!/bin/bash

export DJANGO_SETTINGS_MODULE=settings.settings

python manage.py migrate

python manage.py loaddata fixtures/db.json

exec python manage.py runserver 0.0.0.0:8000