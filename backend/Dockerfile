# Build Stage
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .

RUN pip install --upgrade pip && pip wheel --wheel-dir /build/wheels -r requirements.txt


# Runtime Stage
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TRANSFORMERS_CACHE=/app/model_cache HF_HOME=/app/model_cache

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 libopenblas0 && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" --uid 1001 appuser

USER appuser

WORKDIR /app

COPY --from=builder /build/wheels /wheels

RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY --chown=appuser:appuser app ./app

RUN mkdir -p /app/model_cache

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]