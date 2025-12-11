# ---------- base image ----------
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    # don’t create venv inside image (keeps everything in system site-packages)
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# ---------- install system deps ----------
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl vim \
    && rm -rf /var/lib/apt/lists/*

# ---------- install Poetry ----------
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# ---------- copy only dependency files first (for layer caching) ----------
COPY pyproject.toml poetry.lock* ./

# ---------- install project deps ----------
RUN poetry install --no-interaction --no-ansi \
    # make sure gunicorn + uvicorn are present
    && pip install --no-cache-dir gunicorn uvicorn

# ---------- copy source ----------
COPY . /app

# ---------- runtime ----------
EXPOSE 8000
EXPOSE 5680

# Use Gunicorn to manage workers, Uvicorn as ASGI worker
CMD ["gunicorn",  "-k", "uvicorn.workers.UvicornWorker", "-w", "4",  "-b", "0.0.0.0:8000", "--timeout", "30", "main:app"]