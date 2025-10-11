#!/bin/bash

# Create .env file for local development
cat > .env << 'EOF'
# Django Configuration
SECRET_KEY=django-insecure-local-dev-key-change-in-production
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,shop-service-814454543179.europe-west1.run.app

# Database Configuration (Local Development)
POSTGRES_DB=shop_service
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Cloud Run Configuration (for production deployment)
# RUNNING_ON_CLOUDRUN=false
# CLOUD_SQL_CONNECTION_NAME=PROJECT_ID:europe-west1:shop-sql

# Web Port
WEB_PORT=8000
EOF

echo ".env file created successfully!"
echo "Default values:"
echo "- Database: shop_service"
echo "- User: postgres"
echo "- Password: postgres123"
echo "- Host: db (Docker service name)"
echo "- Port: 5432"
echo ""
echo "You can now run: docker-compose up --build"
