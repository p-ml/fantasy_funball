#!/bin/sh

# Terminate the script on first error.
set -e

# Create directory for log.
mkdir -p /app/var/log

# Load cron configuration.
crontab /app/etc/crontab
# Start cron as a daemon.
cron

# Run your main app.
gunicorn --bind :8000 --workers 2 core.wsgi:application
