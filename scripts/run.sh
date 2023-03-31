#!/usr/bin/env python3

# prestart the server
python prestart.py

# TODO: make run.sh more robust to allow pre-starting of dev, testing, and production environments.
alembic upgrade head

# start the server
python start.py
