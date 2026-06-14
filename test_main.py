import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# The app modules validate these variables during import. The tests do not use
# Postgres or Redis, but the placeholders keep imports deterministic.
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")

from database import Base
from metrics import HEALTH_CHECK_UP
from models import Application, HealthCheck
from routes import applications as applications_routes
from routes import health_checks as health_checks_routes


@pytest.fixture()
def client(monkeypatch):
    # Use a single in-memory SQLite database connection for the whole test app.
    # StaticPool is required so every request sees the same tables and rows.
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    deleted_cache_keys = []
    written_cache_keys = []

    # Replace the production database dependency with the test session.
    def override_get_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def fake_set_cache(key, data):
        written_cache_keys.append((key, len(data)))

    def fake_delete_cache(key):
        deleted_cache_keys.append(key)

    # Avoid Redis during tests while still asserting cache side effects.
    monkeypatch.setattr(applications_routes, "get_cache", lambda key: None)
    monkeypatch.setattr(applications_routes, "set_cache", fake_set_cache)
    monkeypatch.setattr(applications_routes, "delete_cache", fake_delete_cache)
    monkeypatch.setattr(health_checks_routes, "get_cache", lambda key: None)
    monkeypatch.setattr(health_checks_routes, "set_cache", fake_set_cache)

    # Build a minimal app with only the routers under test. Importing main.py
    # would initialize the production engine and metrics app.
    app = FastAPI()
    app.include_router(applications_routes.router)
    app.include_router(health_checks_routes.router)
    app.dependency_overrides[applications_routes.get_session] = override_get_session
    app.dependency_overrides[health_checks_routes.get_session] = override_get_session
    app.state.SessionLocal = TestingSessionLocal
    app.state.deleted_cache_keys = deleted_cache_keys
    app.state.written_cache_keys = written_cache_keys

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


def test_application_crud_flow(client):
    # Start from an empty database and confirm the list endpoint writes cache.
    response = client.get("/applications")
    assert response.status_code == 200
    assert response.json() == []
    assert ("applications_all", 0) in client.app.state.written_cache_keys

    # Create an application and verify the response plus cache invalidation.
    response = client.post(
        "/applications",
        json={"name": "Deploy Tracker", "url": "https://deploy-tracker.test"},
    )
    assert response.status_code == 200
    created_application = response.json()
    assert created_application["name"] == "Deploy Tracker"
    assert created_application["url"] == "https://deploy-tracker.test"
    assert isinstance(created_application["id"], int)
    assert "applications_all" in client.app.state.deleted_cache_keys

    application_id = created_application["id"]

    # Read, update, list, and delete the same application to cover the full flow.
    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200
    assert response.json()["id"] == application_id

    response = client.get("/applications")
    assert response.status_code == 200
    assert [application["id"] for application in response.json()] == [application_id]

    response = client.patch(
        f"/applications/{application_id}",
        json={"name": "Deploy Tracker API", "url": "https://api.deploy-tracker.test"},
    )
    assert response.status_code == 200
    updated_application = response.json()
    assert updated_application["id"] == application_id
    assert updated_application["name"] == "Deploy Tracker API"
    assert updated_application["url"] == "https://api.deploy-tracker.test"

    response = client.delete(f"/applications/{application_id}")
    assert response.status_code == 200
    assert response.json()["id"] == application_id

    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200
    assert response.json() is None


def test_health_check_history_flow_sets_metric_from_latest_check(client):
    # Seed the database directly so the health check endpoint can read history.
    session = client.app.state.SessionLocal()
    try:
        application = Application(name="API", url="https://api.test")
        session.add(application)
        session.commit()
        session.refresh(application)

        session.add_all(
            [
                HealthCheck(
                    application_id=application.id,
                    status=True,
                    response_time=0.12,
                    http_code=200,
                ),
                HealthCheck(
                    application_id=application.id,
                    status=False,
                    response_time=0,
                    http_code=500,
                ),
            ]
        )
        session.commit()
        application_id = application.id
    finally:
        session.close()

    response = client.get(f"/applications/{application_id}/healthchecks")

    # The endpoint should return all checks and cache the application history.
    assert response.status_code == 200
    health_checks = response.json()
    assert len(health_checks) == 2
    assert health_checks[0]["status"] is True
    assert health_checks[1]["status"] is False
    assert health_checks[1]["http_code"] == 500
    assert (
        f"healthchecks_app_{application_id}",
        2,
    ) in client.app.state.written_cache_keys

    # The metric should reflect the latest check, which is down in this fixture.
    health_check_up = next(
        sample
        for sample in HEALTH_CHECK_UP.collect()[0].samples
        if sample.name == "health_check_up"
        and sample.labels["application_id"] == str(application_id)
    )
    assert health_check_up.value == 0


def test_health_check_history_returns_empty_list_without_checks(client):
    # Unknown applications have no health check rows, so the API returns [].
    response = client.get("/applications/999/healthchecks")

    assert response.status_code == 200
    assert response.json() == []
    assert ("healthchecks_app_999", 0) in client.app.state.written_cache_keys
