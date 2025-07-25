import pytest
from fastapi.testclient import TestClient

def test_create_artist(client: TestClient):
    """Teste para criar um artista"""
    artist_data = {
        "profile_id": 1,  # Profile com role ARTISTA (já tem artista)
        "artist_type_id": 1,
        "dias_apresentacao": ["sexta", "sábado"],
        "raio_atuacao": 50.0,
        "duracao_apresentacao": 2.0,
        "valor_hora": 100.0,
        "valor_couvert": 20.0,
        "requisitos_minimos": "Sistema de som básico"
    }
    
    response = client.post("/api/v1/artists/", json=artist_data)
    # Espera-se erro pois já existe um artista para este profile
    assert response.status_code == 400
    assert "Já existe um artista cadastrado para este profile" in response.json()["detail"]

def test_get_artists(client: TestClient):
    """Teste para listar artistas"""
    response = client.get("/api/v1/artists/")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_artist_by_id(client: TestClient):
    """Teste para obter artista por ID"""
    # Usar um artista existente (ID 1 deve existir após a inicialização)
    artist_id = 1
    
    response = client.get(f"/api/v1/artists/{artist_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == artist_id
    assert "profile_id" in data
    assert "artist_type_id" in data

def test_update_artist(client: TestClient):
    """Teste para atualizar artista"""
    # Usar um artista existente (ID 1 deve existir após a inicialização)
    artist_id = 1
    
    # Atualizar o artista
    update_data = {
        "valor_hora": 150.0,
        "valor_couvert": 25.0,
        "requisitos_minimos": "Sistema de som profissional"
    }
    
    response = client.put(f"/api/v1/artists/{artist_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["valor_hora"] == update_data["valor_hora"]
    assert data["valor_couvert"] == update_data["valor_couvert"]
    assert data["requisitos_minimos"] == update_data["requisitos_minimos"]

def test_delete_artist(client: TestClient):
    """Teste para deletar artista"""
    # Usar um artista existente (ID 1 deve existir após a inicialização)
    artist_id = 1
    
    # Deletar o artista
    response = client.delete(f"/api/v1/artists/{artist_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o artista foi deletado
    get_response = client.get(f"/api/v1/artists/{artist_id}")
    assert get_response.status_code == 404 