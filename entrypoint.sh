#!/usr/bin/env sh
set -e

# Wait for Postgres to be ready
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
  for i in $(seq 1 30); do
    if pg_isready -h "$POSTGRES_HOST" -p "${POSTGRES_PORT:-5432}" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; then
      echo "Postgres is ready"; break; fi
    echo "Postgres not ready yet, retry $i/30"; sleep 2;
  done
fi

# Apply database migrations
python shop_service/manage.py migrate --noinput

# Collect static files
python shop_service/manage.py collectstatic --noinput --clear

# Start Gunicorn
gunicorn shop_service.wsgi:application --bind 0.0.0.0:$PORT
