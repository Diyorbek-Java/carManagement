#!/bin/bash

echo "Testing database connection..."

# Execute database connection test
docker-compose exec web python -c "
import os
import psycopg2
import sys

try:
    # Get database connection parameters from environment
    dbname = os.environ.get('SQL_DATABASE')
    user = os.environ.get('SQL_USERNAME')
    password = os.environ.get('SQL_PASSWORD')
    host = os.environ.get('SQL_HOST')
    port = os.environ.get('SQL_PORT', '5432')
    
    # Print connection params (without password)
    print(f'Connecting to: postgresql://{user}@{host}:{port}/{dbname}')
    
    # Connect to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    # Create a cursor
    cur = conn.cursor()
    
    # Execute a simple test query
    cur.execute('SELECT version()')
    
    # Get the version
    version = cur.fetchone()
    
    # Print the result
    print('Database connection successful!')
    print(f'PostgreSQL version: {version[0]}')
    
    # Close the cursor and connection
    cur.close()
    conn.close()
    
    sys.exit(0)  # Success
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)  # Failure
"

# Check exit status
if [ $? -eq 0 ]; then
    echo "Database connection test successful!"
else
    echo "Database connection test failed!"
fi
