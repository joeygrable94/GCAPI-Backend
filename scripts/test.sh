#!/usr/bin/env bash

set -e
set -x

source .env

export API_MODE='test'
export ENVIRONMENT="pytest"

pytest --cov-config=.coveragerc --cov=app --cov-report=term-missing --asyncio-mode=auto --pythonwarnings=all tests "${@}"
