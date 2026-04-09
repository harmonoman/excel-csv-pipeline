FROM python:3.12-slim-bookworm
 
# Install uv from official image — pinned, cacheable, no curl required
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
 
# Upgrade all OS packages to patch known vulnerabilities, then install git
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*
 
# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
 
# Set working directory
WORKDIR /workspace/backend
 
# Copy dependency files explicitly — no glob, lock file must be committed and present
COPY backend/pyproject.toml backend/uv.lock ./
 
# Install all dependencies including dev — --frozen ensures exact lock file resolution
# Fails loudly if lock file is missing or out of date
RUN uv sync --frozen --dev
 
# Copy rest of backend source
COPY backend/ .
 
# Switch to non-root user
USER appuser
 
EXPOSE 8000
