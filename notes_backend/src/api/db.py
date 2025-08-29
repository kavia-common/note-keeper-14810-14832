"""
Database initialization and session management using SQLAlchemy.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.pool import StaticPool

from .settings import get_settings


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy models."""
    pass


_engine = None
_SessionLocal: sessionmaker[Session] | None = None


def _build_engine():
    settings = get_settings()
    url = settings.database_url

    # Special handling for SQLite in-memory or file to ensure proper pooling in single-process
    if url.startswith("sqlite"):
        engine = create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool if url.endswith(":memory:") else None,  # type: ignore[arg-type]
        )
    else:
        engine = create_engine(url)

    return engine


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency. Yields a SQLAlchemy session and ensures it is closed.

    Yields:
        Session: SQLAlchemy session.
    """
    if _SessionLocal is None:
        raise RuntimeError("Database session factory not initialized. Did you call init_db()?")

    db: Session = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Context manager for a transactional SQLAlchemy session.
    """
    if _SessionLocal is None:
        raise RuntimeError("Database session factory not initialized. Did you call init_db()?")

    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


# PUBLIC_INTERFACE
def init_db() -> None:
    """Initialize database engine, session factory, and create tables."""
    global _engine, _SessionLocal
    if _engine is None:
        _engine = _build_engine()

    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    # Import models and create tables
    from .models.note import Note  # noqa: F401

    Base.metadata.create_all(bind=_engine)


# PUBLIC_INTERFACE
def shutdown_db() -> None:
    """Dispose of the database engine."""
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None
