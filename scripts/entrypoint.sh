#!/bin/bash

set -e

# Function to check if Postgres is ready
postgres_ready() {
  nc -z ${SQL_HOST} ${SQL_PORT}
}

# Wait for PostgreSQL to be ready
until postgres_ready; do
  echo "Waiting for PostgreSQL at ${SQL_HOST}:${SQL_PORT}..."
  sleep 2
done
echo "PostgreSQL is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the command passed to docker run
exec "$@"
