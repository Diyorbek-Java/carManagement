# Django Backend CI/CD with Zero Database Downtime

This repository contains a Django DRF (Django Rest Framework) backend with a comprehensive CI/CD pipeline designed for zero database downtime deployments.

## Features

- **CI/CD Pipeline**: Automated testing, building, and deployment through GitHub Actions
- **Zero Database Downtime**: Database persistence across deployments
- **Docker Containerization**: Application runs in isolated containers
- **Nginx Reverse Proxy**: Properly configured for API endpoints
- **Automated Migrations**: Database migrations run automatically after deployment
- **Scheduled Backups**: Regular database backups are automated

## Setup and Deployment

### Prerequisites

- Docker and Docker Compose installed on the production server
- Git access to the repository
- SSH access to the production server

### First-Time Deployment

The application will be automatically deployed when changes are pushed to the main branch. For the first deployment:

1. Ensure all GitHub secrets are set up:
   - `PRODUCTION_HOST`: SSH host for your server
   - `PRODUCTION_USERNAME`: SSH username for your server
   - `PRODUCTION_SSH_KEY`: SSH private key for deployment
   - `SECRET_KEY`: Django secret key
   - `SQL_DATABASE`: PostgreSQL database name
   - `SQL_USERNAME`: PostgreSQL username
   - `SQL_PASSWORD`: PostgreSQL password
   - `SQL_HOST`: PostgreSQL host (set to "db" for Docker deployment)
   - `SQL_PORT`: PostgreSQL port (default: 5432)
   - `EMAIL_HOST_USER`: SMTP email username
   - `EMAIL_HOST_PASSWORD`: SMTP email password

2. Push to the main branch to trigger the deployment:
   ```bash
   git push origin main
   ```

3. After deployment, set up automatic backups on the server:
   ```bash
   ssh [your-server]
   cd /opt/backend
   chmod +x scripts/*.sh
   sudo scripts/setup-cron.sh
   ```

### Development

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-directory]
   ```

2. For local development, you can use the provided script:
   ```bash
   ./scripts/dev_local.sh
   ```
   
   This will copy the `.env.local` file to `.env` and start the application with local settings.

3. Alternatively, you can run with docker-compose directly:
   ```bash
   docker-compose -f docker-compose.local.yml up -d
   ```

4. Access the API at http://localhost:8000/api/

## Database Management

### Zero Downtime Strategy

The CI/CD pipeline is designed to never restart or rebuild the database container during deployments. Instead:

1. Only the web and nginx containers are updated
2. The database data is stored in a persistent Docker volume
3. Migrations are automatically applied after each deployment

### Backup and Restore

Backups are automatically scheduled with the following frequency:
- Daily: Every day at 1:00 AM
- Weekly: Every Sunday at 2:00 AM
- Monthly: 1st day of each month at 3:00 AM

To manually create a backup:
```bash
ssh [your-server]
cd /opt/backend
./scripts/backup-db.sh
```

To restore from a backup:
```bash
ssh [your-server]
cd /opt/backend
./scripts/restore-db.sh /path/to/backup.sql.gz
```

## API Documentation

- Swagger UI: http://your-server/swagger/
- ReDoc: http://your-server/redoc/

## Architecture

- **Web**: Django REST Framework application
- **Database**: PostgreSQL
- **Proxy**: Nginx
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Troubleshooting

### Database Connection Issues

If the web container can't connect to the database:

1. Check environment variables:
   ```bash
   docker-compose exec web env | grep SQL
   ```

2. Verify the database is running:
   ```bash
   docker-compose ps db
   ```

3. Check database logs:
   ```bash
   docker-compose logs db
   ```

### Container Issues

To restart just the web container without affecting the database:
```bash
docker-compose up -d --no-deps web
```

To view application logs:
```bash
docker-compose logs -f web
```
