#!/bin/bash
set -e

# Применяем миграции
alembic upgrade head

# Запускаем сервер
uvicorn app.main:app --host 0.0.0.0 --port $PORT
