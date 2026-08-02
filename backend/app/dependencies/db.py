"""FastAPI database-session dependency."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Provide one database session for the lifetime of a request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()