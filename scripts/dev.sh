#!/bin/bash

echo "Starting development environment..."

# Check if docker-compose.local.yml exists and use it
if [ -f docker-compose.local.yml ]; then
  echo "Using docker-compose.local.yml for development..."
  docker-compose -f docker-compose.local.yml down
  docker-compose -f docker-compose.local.yml up -d --build
else
  echo "Using docker-compose.yml for development..."
  docker-compose down
  docker-compose up -d --build
fi

echo "Development environment is ready!"
echo "Access your application at http://localhost:8000"
