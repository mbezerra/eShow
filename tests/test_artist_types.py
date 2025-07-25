import pytest
from fastapi.testclient import TestClient

def test_create_artist_type(client: TestClient):
    """Teste para criar um tipo de artista"""
    artist_type_data = {
        "tipo": "Dupla"
    }
    
    response = client.post("/api/v1/artist-types/", json=artist_type_data)
    print(f"Create artist type response: {response.status_code} - {response.json()}")  # Debug
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
    # Usar um tipo existente (ID 1 deve existir após a inicialização)
    artist_type_id = 1
    
    # Buscar o tipo
    response = client.get(f"/api/v1/artist-types/{artist_type_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == artist_type_id
    assert "tipo" in data

def test_update_artist_type(client: TestClient):
    """Teste para atualizar tipo de artista"""
    # Usar um tipo existente (ID 1 deve existir após a inicialização)
    artist_type_id = 1
    
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
    # Primeiro criar um tipo de artista temporário
    artist_type_data = {
        "tipo": "Banda"
    }
    
    create_response = client.post("/api/v1/artist-types/", json=artist_type_data)
    artist_type_id = create_response.json()["id"]
    
    # Deletar o tipo
    response = client.delete(f"/api/v1/artist-types/{artist_type_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o tipo foi deletado
    get_response = client.get(f"/api/v1/artist-types/{artist_type_id}")
    assert get_response.status_code == 404 