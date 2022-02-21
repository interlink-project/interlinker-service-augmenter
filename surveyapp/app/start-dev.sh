#! /usr/bin/env bash
HOST=${HOST_SURVEY:-0.0.0.0}
PORT=${PORT_SURVEY}
LOG_LEVEL=${LOG_LEVEL_SURVEY:-info}

# Let the DB start
python /app/app/pre_start.py

# Create initial data in DB
python /app/app/initial_data.py

# Start Uvicorn with live reload IF DEVELOPMENT
exec uvicorn --reload --host $HOST_SURVEY --port $PORT_SURVEY --log-level $LOG_LEVEL_SURVEY "app.main:app"