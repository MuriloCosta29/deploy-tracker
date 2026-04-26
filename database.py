# NOTE: Database configuration creates the engine, session factory, and Base class for models.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(
    "postgresql+psycopg2://deploy_tracker:password@db/deploy_tracker"
)  # hostname always `localhost`. | In Docker Compose, the hostname will change to the container name.

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
