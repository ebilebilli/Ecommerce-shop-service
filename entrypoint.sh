#!/usr/bin/env sh
set -e

# Apply database migrations
python shop_service/manage.py migrate --noinput

# Collect static files (safe if none exist)
python shop_service/manage.py collectstatic --noinput --clear

# Start server
python shop_service/manage.py runserver 0.0.0.0:8000


