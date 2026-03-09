#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

# Navigate to project root
Set-Location (Split-Path $MyInvocation.MyCommand.Path)
Set-Location ..

# Stop Docker containers
Write-Output "Stopping PreLegal application..."
docker compose down

Write-Output "✓ PreLegal stopped"
