#!/bin/bash

echo "Deploying the application..."

# Stop existing containers
docker-compose down

# Build and start containers
docker-compose up -d --build

echo "Waiting for PostgreSQL to be ready..."
sleep 15

# Run migrations
docker-compose exec web python manage.py migrate

# Create a superuser (optional - uncomment if needed)
# docker-compose exec web python manage.py createsuperuser --noinput

echo "Deployment complete!"
echo "Access your application at http://localhost:8000"
