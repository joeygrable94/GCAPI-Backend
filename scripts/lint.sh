#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint-app.sh

bash ./scripts/lint-tests.sh
