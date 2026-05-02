# NOTE: Database configuration creates the engine, session factory, and Base class for models.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# ------------------------------------------------------

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

required_envs = {
    "POSTGRES_USER": POSTGRES_USER,
    "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
    "POSTGRES_DB": POSTGRES_DB,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
}

missing_envs = [name for name, value in required_envs.items() if value is None]

if missing_envs:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_envs)}"
    )


# ------------------------------------------------------

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

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
