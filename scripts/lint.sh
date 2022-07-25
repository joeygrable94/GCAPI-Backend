#!/usr/bin/env bash

set -e
set -x

mypy app
black app
isort app
flake8 app
