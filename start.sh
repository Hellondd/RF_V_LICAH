#!/bin/bash

# Если переменная RUN_LOAD_REGIONS = true, то выполняем скрипт
if [ "$RUN_LOAD_REGIONS" = "true" ]; then
    echo "Running load_regions_from_geojson.py..."
    python scripts/load_regions_from_geojson.py
fi

# Запускаем основное приложение
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT
