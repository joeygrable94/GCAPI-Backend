#!/usr/bin/env bash

set -e
set -x

mypy tests
black --check tests
isort --check-only tests
flake8 tests
