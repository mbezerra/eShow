import pytest
from fastapi.testclient import TestClient

def test_create_artist_musical_style(client: TestClient):
    """Teste para criar uma associação artista-estilo musical"""
    artist_musical_style_data = {
        "artist_id": 1,
        "musical_style_id": 1
    }
    
    response = client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["artist_id"] == artist_musical_style_data["artist_id"]
    assert data["musical_style_id"] == artist_musical_style_data["musical_style_id"]
    assert "id" in data

def test_get_artist_musical_styles(client: TestClient):
    """Teste para listar associações artista-estilo musical"""
    # Este endpoint não existe, vamos testar um endpoint que existe
    response = client.get("/api/v1/artist-musical-styles/artist/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_artist_musical_style_by_id(client: TestClient):
    """Teste para obter associação artista-estilo musical por ID"""
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": 1,
        "musical_style_id": 2  # Usar um estilo diferente
    }
    
    create_response = client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data)
    assert create_response.status_code == 201
    
    # Agora buscar a associação criada usando o endpoint específico
    response = client.get(f"/api/v1/artist-musical-styles/1/2")
    assert response.status_code == 200
    
    data = response.json()
    assert data["artist_id"] == artist_musical_style_data["artist_id"]
    assert data["musical_style_id"] == artist_musical_style_data["musical_style_id"]

def test_get_artist_musical_styles_by_artist(client: TestClient):
    """Teste para obter estilos musicais de um artista específico"""
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": 1,
        "musical_style_id": 1
    }
    
    client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data)
    
    # Buscar estilos do artista
    response = client.get("/api/v1/artist-musical-styles/artist/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_artist_musical_styles_by_musical_style(client: TestClient):
    """Teste para obter artistas de um estilo musical específico"""
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": 1,
        "musical_style_id": 1
    }
    
    client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data)
    
    # Buscar artistas do estilo
    response = client.get("/api/v1/artist-musical-styles/musical-style/1")
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_delete_artist_musical_style(client: TestClient):
    """Teste para deletar associação artista-estilo musical"""
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": 1,
        "musical_style_id": 3  # Usar um estilo diferente
    }
    
    create_response = client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data)
    assert create_response.status_code == 201
    
    # Deletar a associação usando o endpoint específico
    response = client.delete(f"/api/v1/artist-musical-styles/1/3")
    assert response.status_code == 200
    
    # Verificar se a associação foi deletada
    get_response = client.get(f"/api/v1/artist-musical-styles/1/3")
    assert get_response.status_code == 404 