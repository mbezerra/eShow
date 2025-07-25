import pytest
from fastapi.testclient import TestClient

def test_create_artist_type(client: TestClient):
    """Teste para criar um tipo de artista"""
    artist_type_data = {
        "tipo": "Cantor(a) solo"
    }
    
    response = client.post("/api/v1/artist-types/", json=artist_type_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["tipo"] == artist_type_data["tipo"]
    assert "id" in data

def test_get_artist_types(client: TestClient):
    """Teste para listar tipos de artistas"""
    response = client.get("/api/v1/artist-types/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_artist_type_by_id(client: TestClient):
    """Teste para obter tipo de artista por ID"""
    # Primeiro criar um tipo de artista
    artist_type_data = {
        "tipo": "Banda"
    }
    
    create_response = client.post("/api/v1/artist-types/", json=artist_type_data)
    artist_type_id = create_response.json()["id"]
    
    # Agora buscar o tipo criado
    response = client.get(f"/api/v1/artist-types/{artist_type_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == artist_type_id
    assert data["tipo"] == artist_type_data["tipo"]

def test_update_artist_type(client: TestClient):
    """Teste para atualizar tipo de artista"""
    # Primeiro criar um tipo de artista
    artist_type_data = {
        "tipo": "Dupla"
    }
    
    create_response = client.post("/api/v1/artist-types/", json=artist_type_data)
    artist_type_id = create_response.json()["id"]
    
    # Atualizar o tipo
    update_data = {
        "tipo": "Trio"
    }
    
    response = client.put(f"/api/v1/artist-types/{artist_type_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["tipo"] == update_data["tipo"]

def test_delete_artist_type(client: TestClient):
    """Teste para deletar tipo de artista"""
    # Primeiro criar um tipo de artista
    artist_type_data = {
        "tipo": "Grupo"
    }
    
    create_response = client.post("/api/v1/artist-types/", json=artist_type_data)
    artist_type_id = create_response.json()["id"]
    
    # Deletar o tipo
    response = client.delete(f"/api/v1/artist-types/{artist_type_id}")
    assert response.status_code == 204
    
    # Verificar se o tipo foi deletado
    get_response = client.get(f"/api/v1/artist-types/{artist_type_id}")
    assert get_response.status_code == 404 