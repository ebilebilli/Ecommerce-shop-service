# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev ca-certificates postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy pyproject.toml
COPY pyproject.toml ./ 

# Generate requirements.txt from pyproject.toml (single-line for Cloud Build)
RUN python -c "import tomllib, sys; data=tomllib.load(open('pyproject.toml','rb')); reqs=data.get('project', {}).get('dependencies', []); open('requirements.txt','w',encoding='utf-8').write('\n'.join(reqs)); print(f'Wrote {len(reqs)} dependencies to requirements.txt', file=sys.stderr)"

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Change to Django project directory
WORKDIR /app/shop_service

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create static and media directories with proper permissions
RUN mkdir -p /app/staticfiles /app/shop_service/media
RUN chmod -R 777 /app/staticfiles /app/shop_service/media

# Expose port
ENV PORT 8080
EXPOSE 8080

# Start Django using Gunicorn
CMD ["gunicorn", "shop_service.wsgi:application", "--bind", "0.0.0.0:$PORT"]
