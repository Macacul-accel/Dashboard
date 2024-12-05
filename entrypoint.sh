# Exit if command exists with a non-zero status
set -e

# Wait for the PostgreSQL db to be ready
until nc -z db 5432; do
    echo "Waiting for PgSQL..."
    sleep 2
done

# Initialize db
python backend/manage.py migrate

# fetch cards data
python backend/manage.py fetch_cards

# fetch images of the cards
python backend/manage.py fetch_images

# start the server
exec "$@"