# NOTE: Database configuration creates the engine, session factory, and Base class for models.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# ------------------------------------------------------

DB_HOST = os.getenv("DB_HOST", "db")

# ------------------------------------------------------
engine = create_engine(
    f"postgresql+psycopg2://deploy_tracker:password@{DB_HOST}/deploy_tracker"
)  # DB_HOST defaults to "db" for Docker Compose, override with env variable for other environments.
# ------------------------------------------------------


class Base(DeclarativeBase):
    pass


# -----------------------------------------------------


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -----------------------------------------------------


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
