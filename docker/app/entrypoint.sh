#!/bin/bash
set -e

export PYTHONPATH=/app/src:$PYTHONPATH

python /app/src/manage.py migrate --noinput
python /app/src/manage.py collectstatic --noinput

exec "$@"