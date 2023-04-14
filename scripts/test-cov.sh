#!/usr/bin/env bash

set -e
set -x

export APP_MODE='test'

bash scripts/test.sh --cov-report=xml --cov-report=html "${@}"
