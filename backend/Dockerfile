FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/ /app/
COPY deploy/api-entrypoint.sh /usr/local/bin/api-entrypoint
RUN pip install --no-cache-dir ".[worker]" \
    && chmod +x /usr/local/bin/api-entrypoint

EXPOSE 8000

CMD ["api-entrypoint"]
