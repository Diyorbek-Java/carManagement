.PHONY: dev build stop clean test migrate backup

# Development environment
dev:
	docker-compose -f docker-compose.local.yml up

# Start in detached mode
dev-d:
	docker-compose -f docker-compose.local.yml up -d

# Build containers
build:
	docker-compose -f docker-compose.local.yml build

# Stop all containers
stop:
	docker-compose -f docker-compose.local.yml down

# Clean volumes and containers
clean:
	docker-compose -f docker-compose.local.yml down -v

# Run tests
test:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py test

# Create migrations
makemigrations:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py makemigrations

# Apply migrations
migrate:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py migrate

# Create database backup
backup:
	docker-compose -f docker-compose.local.yml exec db pg_dump -U $(SQL_USERNAME) -d $(SQL_DATABASE) | gzip > ./backups/backup_$(shell date +%Y%m%d_%H%M%S).sql.gz

# Shell into the backend container
shell:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py shell

# Create a superuser
createsuperuser:
	docker-compose -f docker-compose.local.yml run --rm web python manage.py createsuperuser

# Show logs
logs:
	docker-compose -f docker-compose.local.yml logs -f
