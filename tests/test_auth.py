import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    """Teste para registrar um novo usuário"""
    user_data = {
        "name": "Teste Auth",
        "email": "auth@example.com",
        "password": "senha123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_login_user(client: TestClient):
    """Teste para login de usuário"""
    # Primeiro registrar um usuário
    user_data = {
        "name": "Login Test",
        "email": "login@example.com",
        "password": "senha123"
    }
    
    client.post("/api/v1/auth/register", json=user_data)
    
    # Fazer login
    login_data = {
        "email": "login@example.com",
        "password": "senha123"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    """Teste para login com credenciais inválidas"""
    login_data = {
        "email": "inexistente@example.com",
        "password": "senhaerrada"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401 