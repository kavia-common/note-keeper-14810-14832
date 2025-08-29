"""
FastAPI application entrypoint for the Notes backend.

This module initializes the FastAPI app, configures CORS, database connections,
and includes the API routers for managing notes.

Environment variables (loaded from .env if present):
- DATABASE_URL: Database connection string (default: sqlite:///./notes.db)
- CORS_ALLOW_ORIGINS: Comma-separated list of origins to allow (default: *)

Swagger/OpenAPI:
- Exposes comprehensive API documentation at /docs and JSON at /openapi.json
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .settings import get_settings
from .db import init_db, shutdown_db
from .routers.notes import router as notes_router


def _get_cors_origins(raw: str | None) -> list[str]:
    if not raw or raw.strip() == "" or raw.strip() == "*":
        return ["*"]
    # split by comma and strip spaces
    return [o.strip() for o in raw.split(",") if o.strip()]


def _create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Notes Backend API",
        description="A simple Notes application API with CRUD operations for notes.",
        version="1.0.0",
        openapi_tags=[
            {"name": "Health", "description": "Service status endpoints"},
            {"name": "Notes", "description": "CRUD operations for notes"},
        ],
    )

    # Configure CORS
    allow_origins = _get_cors_origins(settings.cors_allow_origins)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Lifespan events
    @app.on_event("startup")
    async def on_startup() -> None:
        # Initialize DB (create tables if not exists)
        init_db()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        shutdown_db()

    # Health endpoint
    @app.get(
        "/",
        summary="Health Check",
        tags=["Health"],
        response_model=dict,
        responses={200: {"description": "Service is healthy"}},
    )
    # PUBLIC_INTERFACE
    def health_check() -> dict:
        """
        Health check endpoint.

        Returns:
            dict: Simple JSON indicating the service is healthy.
        """
        return {"message": "Healthy"}

    # Include routers
    app.include_router(notes_router, prefix="/api/v1")

    # Custom exception handlers could be added here if needed
    @app.exception_handler(ValueError)
    async def value_error_handler(_, exc: ValueError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    return app


app = _create_app()
