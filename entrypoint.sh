#!/bin/bash

# Wait for the PostgreSQL db to be ready
echo "waiting for PG db..."
until pg_isready -h $DB_HOST -p $DB_PORT; do
    >&2 echo "PG is unavailable..."
    sleep 2
done
>&2 echo "PG is up - continuing"

# Initialize db
echo "migrations applied"
python backend/manage.py migrate || { echo "Migration failed"; exit 1; }

# fetch cards data
echo "fetch cards.."
python backend/manage.py fetch_cards || { echo "fetch cards failed"; exit 1; }

# fetch images of the cards
echo "fetch images..."
python backend/manage.py fetch_images || { echo "fetch images failed"; exit 1; }

# start the server
echo "starting django server"
exec "$@"