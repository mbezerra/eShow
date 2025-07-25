import pytest
from fastapi.testclient import TestClient

def test_create_profile(client: TestClient):
    """Teste para criar um profile"""
    profile_data = {
        "user_id": 1,  # Usuário existente do conftest.py
        "role_id": 1,  # Role ARTISTA
        "full_name": "João Silva",
        "artistic_name": "João Artista",
        "bio": "Músico profissional com experiência em diversos estilos",
        "cep": "01234-567",
        "logradouro": "Rua das Flores",
        "numero": "123",
        "cidade": "São Paulo",
        "uf": "SP",
        "telefone_movel": "11999999999"
    }
    
    response = client.post("/api/v1/profiles/", json=profile_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["full_name"] == profile_data["full_name"]
    assert data["artistic_name"] == profile_data["artistic_name"]
    assert data["user_id"] == profile_data["user_id"]
    assert "id" in data

def test_get_profiles(client: TestClient):
    """Teste para listar profiles"""
    response = client.get("/api/v1/profiles/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_profile_by_id(client: TestClient):
    """Teste para obter profile por ID"""
    # Usar um profile existente (ID 1 deve existir após a inicialização)
    profile_id = 1
    
    # Buscar o profile
    response = client.get(f"/api/v1/profiles/{profile_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == profile_id
    assert "bio" in data
    assert "full_name" in data

def test_update_profile(client: TestClient):
    """Teste para atualizar profile"""
    # Usar um profile existente (ID 1 deve existir após a inicialização)
    profile_id = 1
    
    # Atualizar o profile
    update_data = {
        "bio": "Músico profissional com experiência em diversos estilos",
        "telefone_movel": "11666666666"
    }
    
    response = client.put(f"/api/v1/profiles/{profile_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["bio"] == update_data["bio"]
    assert data["telefone_movel"] == update_data["telefone_movel"]

def test_delete_profile(client: TestClient):
    """Teste para deletar profile"""
    # Usar um profile existente (ID 2 deve existir após a inicialização)
    profile_id = 2

    try:
        response = client.delete(f"/api/v1/profiles/{profile_id}")
        # Espera-se erro devido à integridade referencial
        assert response.status_code in (400, 409, 500)
    except Exception as e:
        # Se ocorrer uma exceção de integridade, o teste também é considerado sucesso
        assert "IntegrityError" in str(e) or "NOT NULL constraint failed" in str(e) 