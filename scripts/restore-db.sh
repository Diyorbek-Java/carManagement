#!/bin/bash

# Database Restore Script
# Usage: ./restore-db.sh /path/to/backup.sql.gz

# Check if backup file was provided
if [ -z "$1" ]; then
    echo "Error: No backup file specified"
    echo "Usage: $0 /path/to/backup.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

# Check if backup file exists
if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: Backup file '${BACKUP_FILE}' does not exist"
    exit 1
fi

# Warn user and confirm before proceeding
echo "WARNING: This will replace the current database with the contents of ${BACKUP_FILE}"
echo "Are you sure you want to proceed? (y/N)"
read -r confirmation

if [[ ! "${confirmation}" =~ ^[Yy]$ ]]; then
    echo "Restore cancelled"
    exit 0
fi

echo "Starting database restore at $(date)"

# Create a backup of the current database before restoring
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/opt/backups"
CURRENT_BACKUP="${BACKUP_DIR}/pre_restore_backup_${TIMESTAMP}.sql.gz"

mkdir -p ${BACKUP_DIR}

echo "Creating backup of current database state..."
docker-compose exec -T db pg_dump -U postgres -d demo | gzip > ${CURRENT_BACKUP}

if [ $? -ne 0 ]; then
    echo "Failed to create backup of current database. Proceed with caution."
    echo "Continue anyway? (y/N)"
    read -r proceed
    if [[ ! "${proceed}" =~ ^[Yy]$ ]]; then
        echo "Restore cancelled"
        exit 0
    fi
fi

# Restore the database
echo "Restoring database from ${BACKUP_FILE}..."
zcat ${BACKUP_FILE} | docker-compose exec -T db psql -U postgres -d demo

# Check if restore was successful
if [ $? -eq 0 ]; then
    echo "Database restore completed successfully at $(date)"
else
    echo "Database restore failed! at $(date)"
    echo "You can try to restore the previous state from: ${CURRENT_BACKUP}"
    exit 1
fi

echo "You may want to restart your application to ensure it's using the restored database:"
echo "docker-compose restart web"
