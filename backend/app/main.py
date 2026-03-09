from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_tables
from app.routers import auth, templates, documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: create database tables
    create_db_tables()
    yield
    # Shutdown: nothing to do


# Create FastAPI app instance
app = FastAPI(
    title="PreLegal API",
    description="Legal document generation platform API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(templates.router, prefix="/api")
app.include_router(documents.router, prefix="/api")

# Mount static files (must be last to avoid shadowing API routes)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
