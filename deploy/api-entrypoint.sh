#!/bin/sh
set -e

echo "[entrypoint] applico le migration..."
python -m sportlogic.cli migrate

echo "[entrypoint] avvio l'API..."
exec uvicorn sportlogic.main:app --host 0.0.0.0 --port 8000
