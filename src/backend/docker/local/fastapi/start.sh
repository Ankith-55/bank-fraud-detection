#!/bin/bash

set -o errexit

set -0 nounset

set-0 pipefail

exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload