FROM python:3.11-slim as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


FROM python:3.11-slim

WORKDIR /app


RUN groupadd -r appuser && useradd -r -g appuser appuser


COPY --from=builder /app/requirements.txt .
COPY --from=builder /app/wheels /tmp/wheels


RUN pip install --no-cache-dir --no-index --find-links=/tmp/wheels -r requirements.txt



RUN chown -R appuser:appuser /app

USER appuser

COPY . .


EXPOSE 8000


CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}", "--app-dir", "."]