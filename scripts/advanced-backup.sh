#!/bin/bash
# Advanced Database Backup Script with error handling and notifications

# Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_TYPE=${1:-daily}  # daily, weekly, monthly or manual
BACKUP_DIR="/opt/backups"
LOG_FILE="/var/log/db-backups.log"
ERROR_LOG="/var/log/db-backup-errors.log"

# Retention periods (in days)
DAILY_RETENTION=7
WEEKLY_RETENTION=30
MONTHLY_RETENTION=180

# Create subdirectories based on backup type
BACKUP_SUBDIR="${BACKUP_DIR}/${BACKUP_TYPE}"
mkdir -p ${BACKUP_SUBDIR}

# Get database information from environment or .env file
if [ -f .env ]; then
    source .env
fi

DB_NAME=${SQL_DATABASE:-carmanagement}
DB_USER=${SQL_USERNAME:-postgres}
DB_PASS=${SQL_PASSWORD:-postgres}
DB_HOST=${SQL_HOST:-db}
DB_PORT=${SQL_PORT:-5432}

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a ${LOG_FILE}
}

# Function to log errors
log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a ${ERROR_LOG}
    # Add notification mechanism here if needed
    # Example: send email or Slack notification
}

# Function to cleanup old backups
cleanup_old_backups() {
    local retention_days=$1
    local backup_subdir=$2
    
    log "Cleaning up backups older than ${retention_days} days in ${backup_subdir}..."
    find ${backup_subdir} -name "backup_*.sql.gz" -mtime +${retention_days} -delete
}

# Create backup filename
BACKUP_FILE="${BACKUP_SUBDIR}/backup_${DB_NAME}_${TIMESTAMP}.sql.gz"

# Create the backup (using docker-compose if running in container)
log "Starting ${BACKUP_TYPE} backup of database ${DB_NAME}..."

if [ -x "$(command -v docker-compose)" ] && [ "$(docker-compose ps -q db)" != "" ]; then
    # Using docker-compose
    log "Using docker-compose to create backup..."
    docker-compose exec -T db pg_dump -U ${DB_USER} -d ${DB_NAME} --clean --if-exists | gzip > ${BACKUP_FILE}
    BACKUP_RESULT=$?
else
    # Using direct connection
    log "Using direct connection to create backup..."
    PGPASSWORD=${DB_PASS} pg_dump -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} --clean --if-exists | gzip > ${BACKUP_FILE}
    BACKUP_RESULT=$?
fi

# Check if backup was successful
if [ ${BACKUP_RESULT} -eq 0 ]; then
    log "Backup completed successfully: ${BACKUP_FILE}"
    log "Backup size: $(du -h ${BACKUP_FILE} | cut -f1)"
else
    log_error "Backup failed with error code ${BACKUP_RESULT}"
    exit 1
fi

# Cleanup old backups based on backup type
case ${BACKUP_TYPE} in
    daily)
        cleanup_old_backups ${DAILY_RETENTION} ${BACKUP_SUBDIR}
        ;;
    weekly)
        cleanup_old_backups ${WEEKLY_RETENTION} ${BACKUP_SUBDIR}
        ;;
    monthly)
        cleanup_old_backups ${MONTHLY_RETENTION} ${BACKUP_SUBDIR}
        ;;
    manual)
        log "Manual backup completed, no automatic cleanup."
        ;;
    *)
        log "Unknown backup type: ${BACKUP_TYPE}, no cleanup performed."
        ;;
esac

log "Backup process completed."
