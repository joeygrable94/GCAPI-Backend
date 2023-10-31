#!/usr/bin/env python3

# Check the DB is connected.
python cli.py db check-connection

# Upgrade DB
echo "Running Backend DB Migrations..."
alembic upgrade head

sleep 5

# Create initial data in DB
python cli.py db add-initial-data

# start the server
python start.py
