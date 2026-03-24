# ============================================================
# main.py - FastAPI application entry point
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import user, task

# ─────────────────────────────────────────
# Create all tables in the database on startup
# (In production, use Alembic migrations instead)
# ─────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ─────────────────────────────────────────
# Initialize FastAPI app
# ─────────────────────────────────────────
app = FastAPI(
    title="To-Do",
    description="A complete To-Do API with FastAPI, PostgreSQL, JWT Auth",
    version="1.0.0",
    docs_url="/docs",       # Swagger UI at /docs
    redoc_url="/redoc"      # ReDoc UI at /redoc
)

# ─────────────────────────────────────────
# CORS Middleware (allow all origins for dev)
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# Register Routers
# ─────────────────────────────────────────
app.include_router(user.router)     # /register, /login, /me
app.include_router(task.router)     # /tasks, /tasks/{id}


# ─────────────────────────────────────────
# Root endpoint — health check
# ─────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "message": "To-Do API is running!",
        "docs": "/docs",
        "version": "1.0.0"
    }