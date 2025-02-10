#!/usr/bin/env bash

cd mail_sender
python3 manage.py migrate
gunicorn --bind 0.0.0.0:8000 --reload mail_sender.wsgi:application --timeout 600 --log-level debug
