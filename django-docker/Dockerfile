FROM python:3.14-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /bin/

RUN useradd --system --no-create-home app

WORKDIR /app

ENV UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --no-editable

COPY --chown=app:app . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable --compile-bytecode \
    && DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput

USER app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn ready_app.wsgi:application --bind 0.0.0.0:8000"]
