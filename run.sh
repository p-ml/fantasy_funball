#!/bin/sh

# Terminate the script on first error.
set -e

# Export necessary env vars so they're accesible by cron job
echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}" >> /etc/environment
echo "ALLOWED_HOSTS=${ALLOWED_HOSTS}" >> /etc/environment
echo "DATABASE_URL=${DATABASE_URL}" >> /etc/environment
echo "CSRF_TRUSTED_ORIGINS=${CSRF_TRUSTED_ORIGINS}" >> /etc/environment
echo "SECRET_KEY=${SECRET_KEY}" >> /etc/environment
echo "DEBUG=${DEBUG}" >> /etc/environment
echo "GAME_RESUME=${GAME_RESUME}" >> /etc/environment
echo "PAPERTRAIL_API_TOKEN=${PAPERTRAIL_API_TOKEN}" >> /etc/environment

echo "PYTHONPATH=/app" >> /etc/environment

# Load cron configuration.
crontab /app/etc/crontab

# Start cron as a daemon.
cron

# Run the main app.
gunicorn --bind :8000 --workers 2 core.wsgi:application
