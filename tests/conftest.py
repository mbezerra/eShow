import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.database import Base, get_database_session
from app.main import app
from app.core.auth import get_current_active_user
from datetime import datetime, timedelta

# Usar banco de dados SQLite em arquivo temporário para testes
import tempfile
_db_fd, _db_path = tempfile.mkstemp(suffix='.db')
os.close(_db_fd)
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

@pytest.fixture(scope="session")
def setup_database():
    """Fixture para configurar o banco de dados de teste"""
    # Importa todos os modelos para garantir criação das tabelas
    from infrastructure.database.models import (
        UserModel, RoleModel, ProfileModel, ArtistTypeModel, MusicalStyleModel,
        ArtistModel, ArtistMusicalStyleModel, SpaceModel, EventTypeModel,
        SpaceTypeModel, FestivalTypeModel, SpaceEventTypeModel, SpaceFestivalTypeModel,
        BookingModel, ReviewModel, FinancialModel, InterestModel, CepCoordinatesModel
    )
    
    # Garantir que todas as tabelas sejam criadas
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Todas as tabelas foram criadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise
    
    # Popular banco de teste com dados básicos
    session = TestingSessionLocal()
    try:
        # Criar roles básicos
        from domain.entities.role import RoleType
        admin_role = RoleModel(role=RoleType.ADMIN)
        artista_role = RoleModel(role=RoleType.ARTISTA)
        espaco_role = RoleModel(role=RoleType.ESPACO)
        session.add_all([admin_role, artista_role, espaco_role])
        session.commit()
        
        # Criar usuário de teste
        from app.core.security import get_password_hash
        test_user = UserModel(
            name="Test User",
            email="test@example.com",
            password=get_password_hash("testpass"),
            is_active=True
        )
        session.add(test_user)
        session.commit()
        
        # Criar profiles básicos
        profile_artista = ProfileModel(
            user_id=test_user.id,
            role_id=artista_role.id,
            full_name="Artista Teste",
            artistic_name="Artista",
            bio="Músico profissional com experiência em diversos estilos",
            cep="01234-567",
            logradouro="Rua das Flores",
            numero="123",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11999999999"
        )
        profile_espaco = ProfileModel(
            user_id=test_user.id,
            role_id=espaco_role.id,
            full_name="Espaço Teste",
            artistic_name="Espaço",
            bio="Local para eventos e apresentações musicais",
            cep="01234-568",
            logradouro="Avenida Principal",
            numero="456",
            cidade="São Paulo",
            uf="SP",
            telefone_movel="11888888888"
        )
        session.add_all([profile_artista, profile_espaco])
        session.commit()
        
        # Criar artist type básico
        from domain.entities.artist_type import ArtistTypeEnum
        artist_type = ArtistTypeModel(tipo=ArtistTypeEnum.CANTOR_SOLO)
        session.add(artist_type)
        session.commit()
        
        # Criar artista básico
        import json
        artist = ArtistModel(
            profile_id=profile_artista.id,
            artist_type_id=artist_type.id,
            dias_apresentacao=json.dumps(["sexta", "sábado"]),
            raio_atuacao=50.0,
            duracao_apresentacao=2.0,
            valor_hora=100.0,
            valor_couvert=20.0,
            requisitos_minimos="Sistema de som básico"
        )
        session.add(artist)
        session.commit()
        
        # Criar estilos musicais básicos
        musical_style1 = MusicalStyleModel(estyle="Jazz")
        musical_style2 = MusicalStyleModel(estyle="Rock")
        musical_style3 = MusicalStyleModel(estyle="Blues")
        session.add_all([musical_style1, musical_style2, musical_style3])
        session.commit()
        
        # Criar space type básico
        from infrastructure.database.models.space_type_model import SpaceTypeModel
        space_type = SpaceTypeModel(tipo="Teatro")
        session.add(space_type)
        session.commit()
        
        # Criar space básico
        from infrastructure.database.models.space_model import SpaceModel
        from domain.entities.space import AcessoEnum, PublicoEstimadoEnum
        space = SpaceModel(
            profile_id=profile_espaco.id,
            space_type_id=space_type.id,
            acesso=AcessoEnum.PUBLICO,
            dias_apresentacao=json.dumps(["sexta", "sábado"]),
            duracao_apresentacao=3.0,
            valor_hora=150.0,
            valor_couvert=25.0,
            requisitos_minimos="Sistema de som profissional",
            oferecimentos="Palco, iluminação, som",
            estrutura_apresentacao="Palco com 50m²",
            publico_estimado=PublicoEstimadoEnum.CEM_A_QUINHENTOS,
            fotos_ambiente=json.dumps(["foto1.jpg", "foto2.jpg"])
        )
        session.add(space)
        session.commit()
        
        # Criar event type básico
        from infrastructure.database.models.event_type_model import EventTypeModel
        event_type = EventTypeModel(type="Show")
        session.add(event_type)
        session.commit()
        
        # Criar festival type básico
        from infrastructure.database.models.festival_type_model import FestivalTypeModel
        festival_type = FestivalTypeModel(type="Festival de Jazz")
        session.add(festival_type)
        session.commit()
        
        # Criar space event type básico
        from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
        from domain.entities.space_event_type import StatusEventType
        space_event_type = SpaceEventTypeModel(
            space_id=space.id,
            event_type_id=event_type.id,
            tema="Show de Jazz",
            descricao="Apresentação de jazz com músicos locais",
            status=StatusEventType.CONTRATANDO,
            data=datetime.now() + timedelta(days=7),
            horario="20:00"
        )
        session.add(space_event_type)
        session.commit()
        
    except Exception as e:
        print(f"Erro ao popular banco de teste: {e}")
        session.rollback()
        raise
    finally:
        session.close()
    
    yield
    
    # Cleanup após todos os testes
    Base.metadata.drop_all(bind=engine)
    os.unlink(_db_path)

@pytest.fixture(scope="function")
def db_session():
    """Fixture para criar uma sessão de banco de dados para cada teste"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(setup_database, db_session):
    """Fixture para criar um cliente de teste com banco de dados configurado"""
    # Garantir que as tabelas existam
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Erro ao criar tabelas no client fixture: {e}")
        raise
    
    app.dependency_overrides[get_database_session] = override_get_db
    # Não usar mock para get_current_active_user nos testes de integração
    # app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer mock_token"}

@pytest.fixture
def mock_current_user():
    return mock_get_current_active_user() 