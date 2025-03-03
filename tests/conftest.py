import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from urlnk.app import app
from urlnk.database import Base, get_db

# Use a single "shared cache" in-memory DB for all connections
TEST_DATABASE_URL = "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # So all calls reuse the exact same DB connection
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_database():
    """
    Create all tables before each test, and drop them after each test.
    Ensures each test has a fresh, empty DB.
    """
    os.environ["APP_ENV"] = "test"
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Override the dependency before any test
app.dependency_overrides[get_db] = override_get_db  # type: ignore


@pytest.fixture
def client():
    # Now the app and your fixture share the same engine + single connection
    return TestClient(app)
