# syntax=docker/dockerfile:1.7

FROM python:3.13.13-slim-bookworm AS builder

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-dev \
    --no-install-project

COPY src ./src
COPY migrations ./migrations
COPY alembic.ini .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
    --frozen \
    --no-dev


FROM python:3.13.13-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

ARG VERSION=unknown
ARG COMMIT_SHA=unknown

LABEL org.opencontainers.image.title="nbstorage"
LABEL org.opencontainers.image.description="Менеджер паролей"
LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.revision=$COMMIT_SHA
LABEL org.opencontainers.image.source="https://github.com/Notikay/NBStorage"

RUN apt-get update \
    && apt-get install -y --no-install-recommends tini curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 10001 app \
    && useradd \
       --uid 10001 \
       --gid app \
       --create-home \
       --shell /usr/sbin/nologin \
       app

WORKDIR /app

COPY --from=builder --chown=app:app /app /app
COPY --from=builder --chown=app:app /app/migrations /migrations
COPY --from=builder --chown=app:app /app/alembic.ini /alembic.ini

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s \
            --timeout=5s \
            --start-period=20s \
            --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

ENTRYPOINT ["tini", "--"]

CMD ["uvicorn", "infrastructure.presentation.api.fastapi.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "./src"]