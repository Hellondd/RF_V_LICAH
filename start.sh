#!/bin/bash

# Если переменная RUN_LOAD_REGIONS = true, то выполняем скрипт

echo "Running load_regions_from_geojson.py..."
python scripts/load_regions_from_geojson.py

echo "Running seed_regions.py"
python scripts/seed_regions.py
# Запускаем основное приложение
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT
