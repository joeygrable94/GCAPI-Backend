#!/usr/bin/env bash

set -e
set -x

pytest --cov-config=.coveragerc --cov=app --cov-report=term-missing --asyncio-mode=auto tests "${@}"
