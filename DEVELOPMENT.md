# PreLegal Development Guide

## Prerequisites

- Docker and Docker Compose installed
- Node.js 20+ (for local frontend development)
- Python 3.12+ with uv (for local backend development)

## Quick Start

### Production/Docker Build

1. Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. Create `.env` file with the generated key:
```bash
cp .env.example .env
# Edit .env and add your SECRET_KEY
```

3. Start the application:
```bash
# On Mac/Linux
./scripts/start-mac.sh

# On Windows
./scripts/start-windows.ps1
```

4. Access at http://localhost:8000

## Local Development (Recommended)

For faster iteration with hot-reload, run frontend and backend separately:

### Backend Setup

1. Create `.env` file:
```bash
cp .env.example .env
# Edit and set SECRET_KEY to a random value
```

2. Install Python dependencies:
```bash
cd backend
uv sync
```

3. Run backend with auto-reload:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Copy dev environment config:
```bash
cd frontend
cp ../.env.local.example .env.local
```

2. Install Node dependencies:
```bash
npm ci
```

3. Run dev server:
```bash
npm run dev
```
Access frontend at http://localhost:3000

The frontend dev server will proxy API calls to http://localhost:8000 (set in `.env.local`).

## Testing

### Backend Tests

```bash
cd backend
uv run pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
# Output goes to: ../backend/app/static (for Docker) or .next (for development)
```

### Docker Build
```bash
docker compose build
```

## Environment Variables

See `.env.example` for all configuration options.

### Critical Settings

- **SECRET_KEY**: Must be a 32+ character random string for JWT signing. NEVER use the placeholder value.
- **DATABASE_URL**: Path to SQLite database file
- **OPENROUTER_API_KEY**: API key for OpenRouter (for future AI features)

## Troubleshooting

### "SECRET_KEY is not set"
The start script requires a valid SECRET_KEY in `.env`. Generate one:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Then add it to your `.env` file.

### Frontend can't reach API (404 on /api/templates)
Make sure you've set `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` in `frontend/.env.local` for local dev.

### Docker build fails
- Check that Docker is running: `docker ps`
- Clear Docker cache if needed: `docker compose down -v`
- Check logs: `docker compose logs`

### Port already in use
If port 8000 or 3000 is already in use:
- Modify the port in `docker-compose.yml` or `.env`
- Or stop the process using that port

## Architecture

- **Frontend**: Next.js 15 with static export, served by FastAPI in production
- **Backend**: FastAPI with SQLAlchemy ORM, SQLite database
- **Auth**: JWT tokens with 60-minute expiry
- **Database**: SQLite (file-based, resets on container restart)

See `CLAUDE.md` for full technical specifications.
