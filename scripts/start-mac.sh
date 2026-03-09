#!/usr/bin/env bash
set -euo pipefail

# Navigate to project root
cd "$(dirname "$0")/.."

# Ensure .env file exists
if [ ! -f .env ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
  echo ""
  echo "⚠️  IMPORTANT: Edit .env and set SECRET_KEY to a random 32+ character string"
  echo "   You can generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
  echo ""
  exit 1
fi

# Verify SECRET_KEY is set
if ! grep -q "^SECRET_KEY=[a-zA-Z0-9]" .env; then
  echo "✗ SECRET_KEY is not set in .env file"
  echo "   Please edit .env and set SECRET_KEY to a random 32+ character string"
  echo "   Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
  exit 1
fi

# Start Docker containers
echo "Starting PreLegal application..."
docker compose up -d --build

# Wait for application to be ready
sleep 3

# Check if container is running
if docker compose ps | grep -q "prelegal"; then
  echo "✓ PreLegal is running at http://localhost:8000"
else
  echo "✗ Failed to start PreLegal"
  docker compose logs
  exit 1
fi
