import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from infrastructure.database.database import Base, get_database_session
from app.main import app

def test_simple_database_connection():
    """Teste simples para verificar conexão com banco de dados"""
    from tests.conftest import engine, TestingSessionLocal
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    
    # Verificar se as tabelas existem
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]
        print(f"Tabelas criadas: {tables}")
        
        # Verificar se a tabela users existe
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users'"))
        users_table = result.fetchone()
        assert users_table is not None, "Tabela 'users' não foi criada"
    
    # Limpar
    Base.metadata.drop_all(bind=engine)

def test_simple_client(client):
    """Teste simples para verificar se o cliente funciona"""
    # Teste simples de health check
    response = client.get("/docs")
    assert response.status_code == 200 