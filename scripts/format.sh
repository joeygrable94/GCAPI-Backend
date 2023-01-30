#!/usr/bin/env bash

set -e
set -x

bash ./scripts/format-app.sh

bash ./scripts/format-tests.sh
