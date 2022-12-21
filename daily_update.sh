#!/bin/sh
echo "Running daily_update.sh"
/usr/local/bin/python /app/fantasy_funball/scheduler/update_database.py
