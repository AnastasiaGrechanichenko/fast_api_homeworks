#!/bin/sh
set -e

echo "Применяем миграции alembic"
alembic upgrade head

echo "Заполняем базу начальными данными"
python seed.py

echo "Запускаем uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
