#!/usr/bin/env python3

export API_MODE='test'

python cli.py secure load-keys

python cli.py db check-db-connection

python cli.py db create-db

python cli.py db add-initial-data
