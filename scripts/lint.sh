#!/usr/bin/env bash

set -x

mypy app
black --check app
isort --check-only app
flake8 app
