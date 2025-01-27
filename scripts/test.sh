#!/usr/bin/env bash

set -e
set -x

export API_MODE='test'
export ENVIRONMENT="pytest"

pytest --cov-config=.coveragerc --cov=app --cov-report=term-missing --pythonwarnings=all tests "${@}"
