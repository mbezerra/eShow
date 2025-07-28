import pytest
from fastapi.testclient import TestClient

def get_auth_token_and_data(client: TestClient):
    """Helper para obter token de autenticação e criar dados necessários"""
    import uuid
    
    # Criar usuário com email único
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "name": f"Test User {unique_id}",
        "email": f"test{unique_id}@example.com",
        "password": "testpass"
    }
    user_response = client.post("/api/v1/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Fazer login
    login_data = {
        "email": f"test{unique_id}@example.com",
        "password": "testpass"
    }
    response = client.post("/api/v1/auth/login", json=login_data)
    token_data = response.json()
    auth_token = f"Bearer {token_data['access_token']}"
    headers = {"Authorization": auth_token}
    
    # Criar profile (necessário para artist)
    profile_data = {
        "user_id": user_id,
        "role_id": 2,  # ARTISTA
        "full_name": "Test Artist Full Name",
        "artistic_name": "Test Artist",
        "bio": "Test bio for testing purposes",
        "cep": "01234-567",
        "logradouro": "Rua Teste",
        "numero": "123",
        "complemento": "Apto 1",
        "cidade": "São Paulo",
        "uf": "SP",
        "telefone_fixo": "11-1234-5678",
        "telefone_movel": "11-98765-4321",
        "whatsapp": "11-98765-4321",
        "latitude": -23.5505,
        "longitude": -46.6333
    }
    profile_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
    profile_id = profile_response.json()["id"]
    
    # Criar artista
    artist_data = {
        "profile_id": profile_id,
        "artist_type_id": 1,  # Campo obrigatório
        "name": f"Test Artist {unique_id}",
        "bio": "Test artist bio",
        "website": "https://testartist.com",
        "social_media": {"instagram": "@testartist"},
        "dias_apresentacao": ["segunda", "terça", "quarta"],  # Campo obrigatório
        "raio_atuacao": 50,  # Campo obrigatório
        "duracao_apresentacao": 120,  # Campo obrigatório
        "valor_hora": 100.0,  # Campo obrigatório
        "valor_couvert": 50.0,  # Campo obrigatório
        "requisitos_minimos": "Palco e som básico"  # Campo obrigatório
    }
    artist_response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
    artist_id = artist_response.json()["id"]
    
    # Criar estilo musical
    musical_style_data = {
        "style": f"Test Style {unique_id}"
    }
    musical_style_response = client.post("/api/v1/musical-styles/", json=musical_style_data, headers=headers)
    musical_style_id = musical_style_response.json()["id"]
    
    return auth_token, artist_id, musical_style_id

def get_auth_token(client: TestClient):
    """Helper para obter token de autenticação (mantido para compatibilidade)"""
    auth_token, _, _ = get_auth_token_and_data(client)
    return auth_token

def test_create_artist_musical_style(client: TestClient):
    """Teste para criar uma associação artista-estilo musical"""
    # Obter token de autenticação e dados necessários
    auth_token, artist_id, musical_style_id = get_auth_token_and_data(client)
    headers = {"Authorization": auth_token}
    
    artist_musical_style_data = {
        "artist_id": artist_id,
        "musical_style_id": musical_style_id
    }
    
    response = client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data, headers=headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["artist_id"] == artist_musical_style_data["artist_id"]
    assert data["musical_style_id"] == artist_musical_style_data["musical_style_id"]
    assert "id" in data

def test_get_artist_musical_styles(client: TestClient):
    """Teste para listar associações artista-estilo musical"""
    # Obter token de autenticação e dados necessários
    auth_token, artist_id, musical_style_id = get_auth_token_and_data(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": artist_id,
        "musical_style_id": musical_style_id
    }
    client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data, headers=headers)
    
    # Agora testar o endpoint de listagem
    response = client.get(f"/api/v1/artist-musical-styles/artist/{artist_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_artist_musical_style_by_id(client: TestClient):
    """Teste para obter associação artista-estilo musical por ID"""
    # Obter token de autenticação e dados necessários
    auth_token, artist_id, musical_style_id = get_auth_token_and_data(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": artist_id,
        "musical_style_id": musical_style_id
    }
    
    create_response = client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data, headers=headers)
    assert create_response.status_code == 201
    
    # Agora buscar a associação criada usando o endpoint específico
    response = client.get(f"/api/v1/artist-musical-styles/{artist_id}/{musical_style_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["artist_id"] == artist_musical_style_data["artist_id"]
    assert data["musical_style_id"] == artist_musical_style_data["musical_style_id"]

def test_get_artist_musical_styles_by_artist(client: TestClient):
    """Teste para obter estilos musicais de um artista específico"""
    # Obter token de autenticação e dados necessários
    auth_token, artist_id, musical_style_id = get_auth_token_and_data(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": artist_id,
        "musical_style_id": musical_style_id
    }
    
    client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data, headers=headers)
    
    # Buscar estilos do artista
    response = client.get(f"/api/v1/artist-musical-styles/artist/{artist_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_artist_musical_styles_by_musical_style(client: TestClient):
    """Teste para obter artistas de um estilo musical específico"""
    # Obter token de autenticação e dados necessários
    auth_token, artist_id, musical_style_id = get_auth_token_and_data(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": artist_id,
        "musical_style_id": musical_style_id
    }
    
    client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data, headers=headers)
    
    # Buscar artistas do estilo
    response = client.get(f"/api/v1/artist-musical-styles/musical-style/{musical_style_id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_delete_artist_musical_style(client: TestClient):
    """Teste para deletar associação artista-estilo musical"""
    # Obter token de autenticação e dados necessários
    auth_token, artist_id, musical_style_id = get_auth_token_and_data(client)
    headers = {"Authorization": auth_token}
    
    # Primeiro criar uma associação
    artist_musical_style_data = {
        "artist_id": artist_id,
        "musical_style_id": musical_style_id
    }
    
    create_response = client.post("/api/v1/artist-musical-styles/", json=artist_musical_style_data, headers=headers)
    assert create_response.status_code == 201
    
    # Deletar a associação usando o endpoint específico
    response = client.delete(f"/api/v1/artist-musical-styles/{artist_id}/{musical_style_id}", headers=headers)
    assert response.status_code == 200
    
    # Verificar se a associação foi deletada
    get_response = client.get(f"/api/v1/artist-musical-styles/{artist_id}/{musical_style_id}", headers=headers)
    assert get_response.status_code == 404 