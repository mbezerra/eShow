import pytest
from fastapi.testclient import TestClient

def test_create_artist(client: TestClient):
    """Teste para criar um artista"""
    artist_data = {
        "name": "João Silva",
        "bio": "Músico de jazz",
        "email": "joao@artist.com",
        "phone": "11999999999",
        "artist_type_id": 1,
        "is_active": True
    }
    
    response = client.post("/api/v1/artists/", json=artist_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == artist_data["name"]
    assert data["bio"] == artist_data["bio"]
    assert data["email"] == artist_data["email"]
    assert "id" in data

def test_get_artists(client: TestClient):
    """Teste para listar artistas"""
    response = client.get("/api/v1/artists/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_artist_by_id(client: TestClient):
    """Teste para obter artista por ID"""
    # Primeiro criar um artista
    artist_data = {
        "name": "Maria Santos",
        "bio": "Cantora de MPB",
        "email": "maria@artist.com",
        "phone": "11888888888",
        "artist_type_id": 1
    }
    
    create_response = client.post("/api/v1/artists/", json=artist_data)
    artist_id = create_response.json()["id"]
    
    # Agora buscar o artista criado
    response = client.get(f"/api/v1/artists/{artist_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == artist_id
    assert data["name"] == artist_data["name"]

def test_update_artist(client: TestClient):
    """Teste para atualizar artista"""
    # Primeiro criar um artista
    artist_data = {
        "name": "Pedro Costa",
        "bio": "Guitarrista",
        "email": "pedro@artist.com",
        "phone": "11777777777",
        "artist_type_id": 1
    }
    
    create_response = client.post("/api/v1/artists/", json=artist_data)
    artist_id = create_response.json()["id"]
    
    # Atualizar o artista
    update_data = {
        "name": "Pedro Silva Costa",
        "bio": "Guitarrista profissional"
    }
    
    response = client.put(f"/api/v1/artists/{artist_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["bio"] == update_data["bio"]

def test_delete_artist(client: TestClient):
    """Teste para deletar artista"""
    # Primeiro criar um artista
    artist_data = {
        "name": "Ana Oliveira",
        "bio": "Artista temporária",
        "email": "ana@artist.com",
        "phone": "11666666666",
        "artist_type_id": 1
    }
    
    create_response = client.post("/api/v1/artists/", json=artist_data)
    artist_id = create_response.json()["id"]
    
    # Deletar o artista
    response = client.delete(f"/api/v1/artists/{artist_id}")
    assert response.status_code == 204
    
    # Verificar se o artista foi deletado
    get_response = client.get(f"/api/v1/artists/{artist_id}")
    assert get_response.status_code == 404 