#!/bin/bash

echo "Stopping containers..."
docker-compose down

echo "Removing PostgreSQL volume..."
docker volume rm backend_postgres_data || echo "Volume does not exist, continuing..."

echo "Starting containers..."
docker-compose up -d

echo "Waiting for PostgreSQL to be ready..."
sleep 10

echo "Running migrations..."
docker-compose exec web python manage.py migrate

echo "Database reset complete!"
