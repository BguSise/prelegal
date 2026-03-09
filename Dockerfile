# Multi-stage build: frontend builder and backend runtime

# Stage 1: Build Next.js frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
COPY frontend/tsconfig.json ./
COPY frontend/next.config.js ./
COPY frontend/postcss.config.js ./
COPY frontend/tailwind.config.js ./
COPY frontend/app ./app/
COPY frontend/components ./components/
COPY frontend/lib ./lib/
COPY frontend/public ./public/

# Install dependencies and build
RUN npm ci && npm run build

# Stage 2: Python backend runtime
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip
RUN pip install --no-cache-dir uv

# Copy Python project files
COPY backend/pyproject.toml ./backend/

# Install Python dependencies (will generate uv.lock if not present)
WORKDIR /app/backend
RUN uv sync --no-dev

# Copy application code
COPY backend/app ./app

# Copy built frontend static files
COPY --from=frontend-builder /app/frontend/out ./static

# Copy templates
COPY templates /app/templates

# Create data directory for SQLite
RUN mkdir -p /app/data

WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
