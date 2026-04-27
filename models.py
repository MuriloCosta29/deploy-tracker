# NOTE:  Defines the database tables as Python classes (Application, Deploy)

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy import func
from database import Base
# --------------------------------------------------------------------------------


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    created_at = Column(DateTime, server_default=func.now())


# --------------------------------------------------------------------------------


class Deploy(Base):
    __tablename__ = "deploys"
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    version = Column(String)
    status = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())


# --------------------------------------------------------------------------------


class HealthCheck(Base):
    __tablename__ = "health_checks"
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    status = Column(Boolean)
    response_time = Column(Float)
    http_code = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
