FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir drf-spectacular==0.27.2

# Copy project
COPY . .

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media

# Make scripts executable
RUN if [ -d "/app/scripts" ]; then chmod +x /app/scripts/*.sh; fi

EXPOSE 8000

# Simple startup command to run migrations and start the server
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 configs.wsgi:application
