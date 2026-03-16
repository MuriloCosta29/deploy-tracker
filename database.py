from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(
    "postgresql+psycopg2://deploy_tracker:password@localhost/deploy_tracker"
)  # hostname always `localhost`. | In Docker Compose, the hostname will change to the container name.

# ------------------------------------------------------


class Base(DeclarativeBase):
    pass


# -----------------------------------------------------


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
