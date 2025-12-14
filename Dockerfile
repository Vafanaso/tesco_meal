# -------------------------
# Builder stage
# -------------------------
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install deps + project (uv-managed venv)
RUN uv sync --locked

# Copy source
COPY src ./src

# -------------------------
# Runtime stage
# -------------------------
FROM python:3.12-slim

# Copy uv binary
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /usr/local/bin/uvx /usr/local/bin/uvx

# Copy uv environment + app
COPY --from=builder /root/.cache/uv /root/.cache/uv
COPY --from=builder /app /app

WORKDIR /app

ENV PATH="/root/.cache/uv/bin:/usr/local/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "python", "-m", "src.main"]
