"""
Guide:
1. This Dockerfile uses multi-stage builds to optimize the final image size.
2. The `uv` builder stage handles dependency installation and caching.
3. The final stage copies only the required files, creating a lightweight image.

Steps to build and run:
1. Build the Docker image:
   docker build -t my-news-service .

2. Run the Docker container:
   docker run -p 8000:8000 my-news-service
"""

FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.10-slim-bookworm
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "/app/run.py"]
