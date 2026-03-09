#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

# Navigate to project root
Set-Location (Split-Path $MyInvocation.MyCommand.Path)
Set-Location ..

# Ensure .env file exists
if (-not (Test-Path .env)) {
  Write-Output "Creating .env from .env.example..."
  Copy-Item .env.example .env
  Write-Output ""
  Write-Output "⚠️  IMPORTANT: Edit .env and set SECRET_KEY to a random 32+ character string"
  Write-Output "   You can generate one with: python -c `"import secrets; print(secrets.token_hex(32))`""
  Write-Output ""
  exit 1
}

# Verify SECRET_KEY is set
$envContent = Get-Content .env
if (-not ($envContent -match "^SECRET_KEY=[a-zA-Z0-9]+")) {
  Write-Output "✗ SECRET_KEY is not set in .env file"
  Write-Output "   Please edit .env and set SECRET_KEY to a random 32+ character string"
  Write-Output "   Generate one with: python -c `"import secrets; print(secrets.token_hex(32))`""
  exit 1
}

# Start Docker containers
Write-Output "Starting PreLegal application..."
docker compose up -d --build

# Wait for application to be ready
Start-Sleep -Seconds 3

# Check if container is running
$containers = docker compose ps
if ($containers -match "prelegal") {
  Write-Output "✓ PreLegal is running at http://localhost:8000"
} else {
  Write-Output "✗ Failed to start PreLegal"
  docker compose logs
  exit 1
}
