from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.config.database import get_db
from src.main import app
from src.models.activities import Activity
from src.models.rpl_files import RPLFile
from src.models.categories import Category


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

@pytest.fixture(name="category", autouse=False)
def category_fixture(session: Session):
    category = Category(
        id=1,
        course_id=1,
        name="Test Category",
        description="Some description",
        active=True,
        date_created=datetime.now(),
        last_updated=datetime.now(),
    )
    session.add(category)
    yield category

def test_get_activities(client: TestClient, activity: Activity):
    response = client.get(
        f"/api/v2/courses/{activity.course_id}/activities",
        headers={"Authorization": "bearer token"},
    )
    assert response.status_code == 200
    response_activity = response.json()[0]
    assert response_activity["id"] == activity.id
    assert response_activity["name"] == activity.name
    assert response_activity["description"] == activity.description
    assert response_activity["course_id"] == activity.course_id


def test_get_activities_empty(client: TestClient):
    response = client.get(
        "/api/v2/courses/1/activities", headers={"Authorization": "bearer token"}
    )
    assert response.status_code == 200
    assert response.json() == []


def test_get_activity(client: TestClient, activity: Activity):
    response = client.get(
        f"/api/v2/courses/{activity.course_id}/activities/{activity.id}",
        headers={"Authorization": "bearer token"},
    )
    assert response.status_code == 200
    response_activity = response.json()
    assert response_activity["id"] == activity.id
    assert response_activity["name"] == activity.name
    assert response_activity["description"] == activity.description
    assert response_activity["course_id"] == activity.course_id


def test_get_activity_not_found(client: TestClient):
    response = client.get(
        "/api/v2/courses/1/activities/1", headers={"Authorization": "bearer token"}
    )
    assert response.status_code == 404
    response_error = response.json()
    assert (
        response_error["detail"]
        == "The Activity with ID 1 does not exist in the Course 1"
    )


def test_delete_activity(client: TestClient, activity: Activity, session: Session):
    response = client.delete(
        f"/api/v2/courses/{activity.course_id}/activities/{activity.id}",
        headers={"Authorization": "bearer token"},
    )

    assert response.status_code == 204

    assert session.query(Activity).where(Activity.id == activity.id).first() == None


def test_delete_activity_not_found(client: TestClient):
    response = client.delete(
        "/api/v2/courses/1/activities/1",
        headers={"Authorization": "bearer token"},
    )

    assert response.status_code == 404


def test_create_activity(client: TestClient, category: Category, session: Session):
    files = [('startingFile', open('./tests/http/resources/files_metadata', 'rb')), ('startingFile', open('./tests/http/resources/main.py', 'rb'))]
    response = client.post(
        "/api/v2/courses/1/activities",
        data={
            "name": "Some test activity",
            "points": 1,
            "language": "python",
            "activityCategoryId": category.id,
            "description": "Some description"
        },
        files=files,
        headers={"Authorization": "bearer token"}
    )
    
    response_activity = response.json()

    db_activity = session.query(Activity).all()[0]
    assert response_activity["id"] == db_activity.id

    db_file = session.query(RPLFile).all()[0]
    assert response_activity["starting_files_id"] == db_file.id

def test_create_activity_not_found_category(client: TestClient, session: Session):
    files = [('startingFile', open('./tests/http/resources/files_metadata', 'rb')), ('startingFile', open('./tests/http/resources/main.py', 'rb'))]
    response = client.post(
        "/api/v2/courses/1/activities",
        data={
            "name": "Some test activity",
            "points": 1,
            "language": "python",
            "activityCategoryId": 1,
            "description": "Some description"
        },
        files=files,
        headers={"Authorization": "bearer token"}
    )
    
    assert response.status_code == 404
