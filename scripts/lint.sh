#!/usr/bin/env bash

set -x

mypy app
black app --check
isort app --recursive --check-only app
flake8 app
