#!/usr/bin/env bash
# Scrollrot backend build script for Render deployment
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
