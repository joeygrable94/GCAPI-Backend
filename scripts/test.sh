#!/usr/bin/env bash

set -e
set -x

export APP_MODE='test'

pytest --cov-config=.coveragerc --cov=app --cov-report=term-missing --asyncio-mode=auto tests "${@}"
