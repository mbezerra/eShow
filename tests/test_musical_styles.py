import pytest
from fastapi.testclient import TestClient

def test_create_musical_style(client: TestClient):
    """Teste para criar um estilo musical"""
    musical_style_data = {
        "style": "Funk"
    }
    
    response = client.post("/api/v1/musical-styles/", json=musical_style_data)
    print(f"Create musical style response: {response.status_code} - {response.json()}")  # Debug
    assert response.status_code == 201
    
    data = response.json()
    assert data["style"] == musical_style_data["style"]
    assert "id" in data

def test_get_musical_styles(client: TestClient):
    """Teste para listar estilos musicais"""
    response = client.get("/api/v1/musical-styles/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_musical_style_by_id(client: TestClient):
    """Teste para obter estilo musical por ID"""
    # Usar um estilo existente (ID 1 deve existir após a inicialização)
    musical_style_id = 1
    
    # Buscar o estilo
    response = client.get(f"/api/v1/musical-styles/{musical_style_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == musical_style_id
    assert "style" in data

def test_update_musical_style(client: TestClient):
    """Teste para atualizar estilo musical"""
    # Usar um estilo existente (ID 1 deve existir após a inicialização)
    musical_style_id = 1
    
    # Atualizar o estilo
    update_data = {
        "style": "Jazz Moderno"
    }
    
    response = client.put(f"/api/v1/musical-styles/{musical_style_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["style"] == update_data["style"]

def test_delete_musical_style(client: TestClient):
    """Teste para deletar estilo musical"""
    # Usar um estilo existente (ID 2 deve existir após a inicialização)
    musical_style_id = 2
    
    # Deletar o estilo
    response = client.delete(f"/api/v1/musical-styles/{musical_style_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o estilo foi deletado
    get_response = client.get(f"/api/v1/musical-styles/{musical_style_id}")
    assert get_response.status_code == 404 