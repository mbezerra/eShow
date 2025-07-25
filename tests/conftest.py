import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.database import Base, get_database_session
from app.main import app
from app.core.auth import get_current_active_user

# Cria um arquivo temporário para o banco de dados SQLite
_db_fd, _db_path = tempfile.mkstemp()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{_db_path}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def mock_get_current_active_user():
    from app.schemas.user import UserResponse
    return UserResponse(
        id=1,
        name="Test User",
        email="test@example.com",
        is_active=True,
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00"
    )

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Importa todos os modelos para garantir criação das tabelas
    from infrastructure.database.models import (
        UserModel, RoleModel, ProfileModel, ArtistTypeModel, MusicalStyleModel,
        ArtistModel, ArtistMusicalStyleModel, SpaceModel, EventTypeModel,
        SpaceTypeModel, FestivalTypeModel, SpaceEventTypeModel, SpaceFestivalTypeModel,
        BookingModel, ReviewModel, FinancialModel, InterestModel, CepCoordinatesModel
    )
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    os.close(_db_fd)
    os.unlink(_db_path)

@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_database_session] = override_get_db
    app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer mock_token"}

@pytest.fixture
def mock_current_user():
    return mock_get_current_active_user() 