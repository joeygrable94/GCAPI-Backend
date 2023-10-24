#!/usr/bin/env python3

# Check the DB is connected.
python prestart.py

# Upgrade DB
echo "Running Backend DB Migrations..."
alembic upgrade head

sleep 5

# Create initial data in DB
python initial_data.py

# start the server
python start.py
