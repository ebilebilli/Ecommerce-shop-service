# syntax=docker/dockerfile:1

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifest
COPY pyproject.toml ./

# Install Python dependencies declared in pyproject.toml
# Generate a temporary requirements.txt from pyproject dependencies and install
RUN python - <<'PY'
import tomllib, sys
with open('pyproject.toml','rb') as f:
    data = tomllib.load(f)
reqs = data.get('project', {}).get('dependencies', [])
open('requirements.txt','w', encoding='utf-8').write("\n".join(reqs))
print(f"Wrote {len(reqs)} dependencies to requirements.txt", file=sys.stderr)
PY
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Entrypoint script
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]


