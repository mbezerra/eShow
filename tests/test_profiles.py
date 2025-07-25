import pytest
from fastapi.testclient import TestClient

def test_create_profile(client: TestClient):
    """Teste para criar um profile"""
    profile_data = {
        "user_id": 1,
        "bio": "Músico apaixonado por jazz",
        "phone": "11999999999",
        "address": "Rua das Flores, 123",
        "city": "São Paulo",
        "state": "SP",
        "cep": "01234-567"
    }
    
    response = client.post("/api/v1/profiles/", json=profile_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["bio"] == profile_data["bio"]
    assert data["phone"] == profile_data["phone"]
    assert "id" in data

def test_get_profiles(client: TestClient):
    """Teste para listar profiles"""
    response = client.get("/api/v1/profiles/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_profile_by_id(client: TestClient):
    """Teste para obter profile por ID"""
    # Primeiro criar um profile
    profile_data = {
        "user_id": 1,
        "bio": "Produtor musical",
        "phone": "11888888888"
    }
    
    create_response = client.post("/api/v1/profiles/", json=profile_data)
    profile_id = create_response.json()["id"]
    
    # Agora buscar o profile criado
    response = client.get(f"/api/v1/profiles/{profile_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == profile_id
    assert data["bio"] == profile_data["bio"]

def test_update_profile(client: TestClient):
    """Teste para atualizar profile"""
    # Primeiro criar um profile
    profile_data = {
        "user_id": 1,
        "bio": "Músico iniciante",
        "phone": "11777777777"
    }
    
    create_response = client.post("/api/v1/profiles/", json=profile_data)
    profile_id = create_response.json()["id"]
    
    # Atualizar o profile
    update_data = {
        "bio": "Músico profissional",
        "phone": "11666666666"
    }
    
    response = client.put(f"/api/v1/profiles/{profile_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["bio"] == update_data["bio"]
    assert data["phone"] == update_data["phone"]

def test_delete_profile(client: TestClient):
    """Teste para deletar profile"""
    # Primeiro criar um profile
    profile_data = {
        "user_id": 1,
        "bio": "Profile temporário",
        "phone": "11555555555"
    }
    
    create_response = client.post("/api/v1/profiles/", json=profile_data)
    profile_id = create_response.json()["id"]
    
    # Deletar o profile
    response = client.delete(f"/api/v1/profiles/{profile_id}")
    assert response.status_code == 204
    
    # Verificar se o profile foi deletado
    get_response = client.get(f"/api/v1/profiles/{profile_id}")
    assert get_response.status_code == 404 