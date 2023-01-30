#!/usr/bin/env bash

set -e
set -x

mypy app
black --check app
isort --check-only app
flake8 app
