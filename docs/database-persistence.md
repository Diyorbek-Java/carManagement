# Database Persistence Strategy

This document outlines our strategy for ensuring database persistence and zero data loss during deployments.

## Overview

Our PostgreSQL database is configured to persist data across deployments and server restarts. This is achieved through:

1. Using named Docker volumes for database storage
2. Implementing pre-deployment backups
3. Using a deployment strategy that avoids downtime
4. Regular scheduled backups

## Docker Volume Configuration

The PostgreSQL data is stored in a Docker named volume (`postgres_data`) that persists independently of container lifecycles. This is configured in our `docker-compose.yml`:

```yaml
volumes:
  postgres_data:
```

And attached to the database container:

```yaml
services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
```

This ensures that even if the database container is stopped or removed, the data persists in the named volume.

## Pre-Deployment Backups

Before each deployment, a database backup is automatically created using the `backup-db.sh` script. This script:

1. Creates a timestamped database dump
2. Compresses the dump using gzip
3. Stores it in a designated backup directory
4. Implements a retention policy to manage disk space

## Zero-Downtime Deployment Strategy

Our CI/CD pipeline is designed to update services without impacting the database:

1. The database container is never restarted during deployment unless explicitly necessary
2. Only the application containers are updated and restarted
3. If database migrations need to be applied, they are tested thoroughly in the CI pipeline first

```bash
# Only update the web service, not the database
docker-compose up -d --no-deps web
```

## Scheduled Backups

In addition to pre-deployment backups, we implement scheduled backups using cron:

1. Daily backups at off-peak hours
2. Weekly comprehensive backups
3. Monthly backups retained for a longer period

## Backup Retention Policy

Our backup retention policy ensures efficient use of storage while maintaining adequate historical data:

- Daily backups: Retained for 7 days
- Weekly backups: Retained for 1 month
- Monthly backups: Retained for 6 months

## Backup Verification

To ensure the integrity of our backups, we periodically verify them by:

1. Restoring to a test environment
2. Running validation checks on the restored data
3. Documenting the verification process

## Disaster Recovery

In case of database corruption or data loss, follow the recovery steps in our disaster recovery documentation:

1. Stop the affected services
2. Restore the most recent backup
3. Verify data integrity
4. Restart services

## Monitoring

The database is monitored for:

- Disk usage
- Connection count
- Query performance
- Backup success/failure

Alerts are configured to notify the team of any issues.
