#!/bin/sh
set -e

echo "[entrypoint] applico le migration..."
python -m arena.cli migrate

echo "[entrypoint] avvio l'API..."
exec uvicorn arena.main:app --host 0.0.0.0 --port 8000
