#!/usr/bin/env bash
set -euo pipefail

# Navigate to project root
cd "$(dirname "$0")/.."

# Stop Docker containers
echo "Stopping PreLegal application..."
docker compose down

echo "✓ PreLegal stopped"
