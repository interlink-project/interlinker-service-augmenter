#! /usr/bin/env bash
HOST=${HOST:-0.0.0.0}
PORT=${PORT}
LOG_LEVEL=${LOG_LEVEL:-info}

# Let the DB start
python /app/app/pre_start.py

# Create initial data in DB
python /app/app/initial_data.py

# Start Uvicorn with live reload IF DEVELOPMENT
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "app.main:app"