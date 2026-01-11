from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session
from typing import Generator
import os
from core.config import settings


# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session from the engine.
    This function is meant to be used as a FastAPI dependency.
    """
    with Session(engine) as session:
        yield session