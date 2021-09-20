#!/bin/bash

python manage.py collectstatic --no-input

exec gunicorn blackjack_django.wsgi:application -b 0.0.0.0 --reload
