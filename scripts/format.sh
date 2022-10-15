#!/usr/bin/env bash

set -e
set -x

autoflake --remove-all-unused-imports --remove-unused-variables --exclude=__init__.py --in-place --recursive app
black app
isort app
