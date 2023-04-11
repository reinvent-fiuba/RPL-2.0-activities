from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.config.database import get_db
from src.main import app
from src.models.activities import Activity


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        return session

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="activity", autouse=False)
def activity_fixture(session: Session):
    activity = Activity(
        id=1,
        course_id=1,
        activity_category_id=1,
        name="Test Activity",
        description="Some description",
        language="Python",
        is_io_tested=False,
        points=22,
        compilation_flags="",
        active=True,
        deleted=False,
        starting_files_id=1,
        date_created=datetime.now(),
        last_updated=datetime.now(),
    )
    session.add(activity)
    yield activity


def test_get_activities(client: TestClient, activity: Activity):
    response = client.get(f"/api/v2/courses/{activity.course_id}/activities")
    assert response.status_code == 200
    response_activity = response.json()[0]
    assert response_activity["id"] == activity.id
    assert response_activity["name"] == activity.name
    assert response_activity["description"] == activity.description
    assert response_activity["course_id"] == activity.course_id


def test_get_activities_empty(client: TestClient):
    response = client.get("/api/v2/courses/1/activities")
    assert response.status_code == 200
    assert response.json() == []


def test_get_activity(client: TestClient, activity: Activity):
    response = client.get(
        f"/api/v2/courses/{activity.course_id}/activities/{activity.id}"
    )
    assert response.status_code == 200
    response_activity = response.json()
    assert response_activity["id"] == activity.id
    assert response_activity["name"] == activity.name
    assert response_activity["description"] == activity.description
    assert response_activity["course_id"] == activity.course_id


def test_get_activity_not_found(client: TestClient):
    response = client.get("/api/v2/courses/1/activities/1")
    assert response.status_code == 404
    response_error = response.json()
    assert (
        response_error["detail"]
        == "The Activity with ID 1 does not exist in the Course 1"
    )
