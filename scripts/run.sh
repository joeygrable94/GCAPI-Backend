#!/usr/bin/env python3

# Check DB connection
python cli.py db check-db-connection

# Upgrade DB
echo "Running Backend DB Migrations..."
python -m alembic upgrade head

# Create initial data in DB
# python cli.py db add-initial-data

# start the server
fastapi run app/main.py --port 8888
# python start.py
