#!/usr/bin/env bash

set -x

mypy app
black app
isort app
flake8 app
