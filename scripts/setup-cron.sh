#!/bin/bash

# This script sets up automated backups via cron
# Run this once on your production server

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root"
  exit 1
fi

CRON_FILE="/etc/cron.d/db-backups"
BACKUP_SCRIPT="/opt/backend/scripts/backup-db.sh"

# Make sure backup script is executable
chmod +x ${BACKUP_SCRIPT}

# Create cron job file
cat > ${CRON_FILE} << EOF
# Automated Database Backups
# Daily backup at 1:00 AM
0 1 * * * root ${BACKUP_SCRIPT} > /var/log/db-backup.log 2>&1

# Weekly backup on Sunday at 2:00 AM
0 2 * * 0 root ${BACKUP_SCRIPT} weekly > /var/log/db-backup-weekly.log 2>&1

# Monthly backup on the 1st of each month at 3:00 AM
0 3 1 * * root ${BACKUP_SCRIPT} monthly > /var/log/db-backup-monthly.log 2>&1
EOF

# Set proper permissions
chmod 644 ${CRON_FILE}

echo "Cron jobs for database backups have been set up."
echo "Daily backups will run at 1:00 AM"
echo "Weekly backups will run on Sundays at 2:00 AM"
echo "Monthly backups will run on the 1st of each month at 3:00 AM"
echo "Logs will be written to /var/log/db-backup*.log"
