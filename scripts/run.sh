#!/usr/bin/env python3

# TODO: make run.sh more robust to allow pre-starting of dev, testing, and production environments.
alembic upgrade head

# prestart the server
python prestart.py

# start the server
python start.py
