#!/bin/bash

echo "Starting local development environment..."

# Use local environment file
cp .env.local .env

# Start the containers
docker-compose down
docker-compose up -d

echo "Local development environment is ready!"
echo "Access your application at http://localhost:8000"
