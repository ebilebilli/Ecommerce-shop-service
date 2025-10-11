# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev ca-certificates postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements.txt
COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

WORKDIR /app/shop_service

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

RUN mkdir -p /app/staticfiles /app/shop_service/media
RUN chmod -R 777 /app/staticfiles /app/shop_service/media

ENV PORT 8080
EXPOSE 8080

CMD ["gunicorn", "shop_service.wsgi:application", "--bind", "0.0.0.0:$PORT"]
