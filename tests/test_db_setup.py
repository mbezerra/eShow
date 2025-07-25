import pytest
from sqlalchemy import text
from infrastructure.database.database import Base, get_database_session
from infrastructure.database.models import (
    UserModel, RoleModel, ProfileModel, ArtistTypeModel, MusicalStyleModel,
    ArtistModel, ArtistMusicalStyleModel, SpaceModel, EventTypeModel,
    SpaceTypeModel, FestivalTypeModel, SpaceEventTypeModel, SpaceFestivalTypeModel,
    BookingModel, ReviewModel, FinancialModel, InterestModel, CepCoordinatesModel
)

def test_database_tables_creation():
    """Teste para verificar se as tabelas estão sendo criadas"""
    from tests.conftest import engine
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Verificar se as tabelas existem
    with engine.connect() as conn:
        # Verificar tabela users
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
        assert result.fetchone() is not None, "Tabela 'users' não foi criada"
        
        # Verificar outras tabelas importantes
        tables = ['roles', 'profiles', 'artist_types', 'musical_styles', 'artists']
        for table in tables:
            result = conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'"))
            assert result.fetchone() is not None, f"Tabela '{table}' não foi criada"
    
    # Limpar
    Base.metadata.drop_all(bind=engine) 