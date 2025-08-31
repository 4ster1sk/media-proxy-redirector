#!/bin/sh
set -e
export WORKERS=${WORKERS:-5}
echo "Starting Uvicorn with $WORKERS workers..."
exec "$@"
