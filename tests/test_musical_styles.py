import pytest
from fastapi.testclient import TestClient

def test_create_musical_style(client: TestClient):
    """Teste para criar um estilo musical"""
    musical_style_data = {
        "estyle": "Jazz"
    }
    
    response = client.post("/api/v1/musical-styles/", json=musical_style_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["estyle"] == musical_style_data["estyle"]
    assert "id" in data

def test_get_musical_styles(client: TestClient):
    """Teste para listar estilos musicais"""
    response = client.get("/api/v1/musical-styles/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_musical_style_by_id(client: TestClient):
    """Teste para obter estilo musical por ID"""
    # Primeiro criar um estilo musical
    musical_style_data = {
        "estyle": "Rock"
    }
    
    create_response = client.post("/api/v1/musical-styles/", json=musical_style_data)
    musical_style_id = create_response.json()["id"]
    
    # Agora buscar o estilo criado
    response = client.get(f"/api/v1/musical-styles/{musical_style_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == musical_style_id
    assert data["estyle"] == musical_style_data["estyle"]

def test_update_musical_style(client: TestClient):
    """Teste para atualizar estilo musical"""
    # Primeiro criar um estilo musical
    musical_style_data = {
        "estyle": "Blues"
    }
    
    create_response = client.post("/api/v1/musical-styles/", json=musical_style_data)
    musical_style_id = create_response.json()["id"]
    
    # Atualizar o estilo
    update_data = {
        "estyle": "Blues Clássico"
    }
    
    response = client.put(f"/api/v1/musical-styles/{musical_style_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["estyle"] == update_data["estyle"]

def test_delete_musical_style(client: TestClient):
    """Teste para deletar estilo musical"""
    # Primeiro criar um estilo musical
    musical_style_data = {
        "estyle": "Temporário"
    }
    
    create_response = client.post("/api/v1/musical-styles/", json=musical_style_data)
    musical_style_id = create_response.json()["id"]
    
    # Deletar o estilo
    response = client.delete(f"/api/v1/musical-styles/{musical_style_id}")
    assert response.status_code == 204
    
    # Verificar se o estilo foi deletado
    get_response = client.get(f"/api/v1/musical-styles/{musical_style_id}")
    assert get_response.status_code == 404 