#!/bin/bash

# Automated Database Backup Script
# This script can be run before deployments or on a schedule
# It backs up the PostgreSQL database to ensure zero data loss

# Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/opt/backups"
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql.gz"
BACKUP_RETENTION_DAYS=30  # How many days to keep backups

# Ensure backup directory exists
mkdir -p ${BACKUP_DIR}

echo "Starting database backup at $(date)"

# Use docker-compose to backup the database directly from the container
# This ensures we're backing up the exact data in use
docker-compose exec -T db pg_dump -U postgres -d demo | gzip > ${BACKUP_FILE}

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup successful: ${BACKUP_FILE}"
    echo "Backup size: $(du -h ${BACKUP_FILE} | cut -f1)"
else
    echo "Backup failed!"
    exit 1
fi

# Clean up old backups
echo "Removing backups older than ${BACKUP_RETENTION_DAYS} days..."
find ${BACKUP_DIR} -name "db_backup_*.sql.gz" -mtime +${BACKUP_RETENTION_DAYS} -delete

echo "Backup process completed at $(date)"
