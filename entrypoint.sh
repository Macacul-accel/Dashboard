#!/bin/bash

# Wait for the PostgreSQL db to be ready
echo "waiting for PG db..."
until pg_isready -h $DB_HOST -p $DB_PORT; do
    >&2 echo "PG is unavailable..."
    sleep 2
done
>&2 echo "PG is up - continuing"

cd backend

# Initialize db
echo "migrations applied"
python manage.py migrate || { echo "Migration failed"; exit 1; }

# Collect static files
echo "collecting static files..."
python manage.py collectstatic --noinput || { echo "collectstatic failed"; exit 1; }

# start the server
echo "starting django server"
exec "$@"