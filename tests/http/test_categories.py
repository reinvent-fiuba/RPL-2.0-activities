from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.config.database import get_db
from src.main import app
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


def test_get_categories(client: TestClient, category: Category):
    response = client.get(
        f"/api/v2/courses/{category.course_id}/categories",
        headers={"Authorization": "bearer token"},
    )
    assert response.status_code == 200
    response_category = response.json()[0]
    assert response_category["id"] == category.id
    assert response_category["name"] == category.name
    assert response_category["description"] == category.description
    assert response_category["course_id"] == category.course_id


def test_get_categories_empty(client: TestClient):
    response = client.get(
        "/api/v2/courses/1/categories", headers={"Authorization": "bearer token"}
    )
    assert response.status_code == 200
    assert response.json() == []


def test_get_category(client: TestClient, category: Category):
    response = client.get(
        f"/api/v2/courses/{category.course_id}/categories/{category.id}",
        headers={"Authorization": "bearer token"},
    )
    assert response.status_code == 200
    response_category = response.json()
    assert response_category["id"] == category.id
    assert response_category["name"] == category.name
    assert response_category["description"] == category.description
    assert response_category["course_id"] == category.course_id


def test_get_category_not_found(client: TestClient):
    response = client.get(
        "/api/v2/courses/1/categories/1", headers={"Authorization": "bearer token"}
    )
    assert response.status_code == 404
    response_error = response.json()
    assert (
        response_error["detail"]
        == "The Category with ID 1 does not exist in the Course 1"
    )
