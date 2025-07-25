import pytest
from fastapi.testclient import TestClient
import json

def test_create_space(client: TestClient):
    """Teste para criar um espaço"""
    space_data = {
        "profile_id": 2,  # Profile de espaço (ESPACO role)
        "space_type_id": 1,
        "acesso": "Público",
        "dias_apresentacao": ["sexta", "sábado"],
        "duracao_apresentacao": 3.0,
        "valor_hora": 150.0,
        "valor_couvert": 25.0,
        "requisitos_minimos": "Sistema de som profissional",
        "oferecimentos": "Palco, iluminação, som",
        "estrutura_apresentacao": "Palco com 50m²",
        "publico_estimado": "101-500",
        "fotos_ambiente": ["foto1.jpg", "foto2.jpg"]
    }
    
    response = client.post("/api/v1/spaces/", json=space_data)
    print(f"Create space response: {response.status_code} - {response.json()}")  # Debug
    assert response.status_code == 201
    
    data = response.json()
    assert data["profile_id"] == space_data["profile_id"]
    assert data["space_type_id"] == space_data["space_type_id"]
    assert data["acesso"] == space_data["acesso"]
    assert "id" in data

def test_get_spaces(client: TestClient):
    """Teste para listar espaços"""
    response = client.get("/api/v1/spaces/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_space_by_id(client: TestClient):
    """Teste para obter espaço por ID"""
    # Primeiro criar um espaço
    space_data = {
        "profile_id": 2,  # Profile de espaço (ESPACO role)
        "space_type_id": 1,
        "acesso": "Privado",
        "dias_apresentacao": ["domingo"],
        "duracao_apresentacao": 2.0,
        "valor_hora": 100.0,
        "valor_couvert": 15.0,
        "requisitos_minimos": "Sistema básico",
        "oferecimentos": "Palco simples",
        "estrutura_apresentacao": "Palco com 30m²",
        "publico_estimado": "51-100",
        "fotos_ambiente": ["foto3.jpg"]
    }
    
    create_response = client.post("/api/v1/spaces/", json=space_data)
    space_id = create_response.json()["id"]
    
    # Agora buscar o espaço criado
    response = client.get(f"/api/v1/spaces/{space_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == space_id
    assert data["profile_id"] == space_data["profile_id"]

def test_update_space(client: TestClient):
    """Teste para atualizar espaço"""
    # Primeiro criar um espaço
    space_data = {
        "profile_id": 2,  # Profile de espaço (ESPACO role)
        "space_type_id": 1,
        "acesso": "Público",
        "dias_apresentacao": ["quinta", "sexta"],
        "duracao_apresentacao": 4.0,
        "valor_hora": 200.0,
        "valor_couvert": 30.0,
        "requisitos_minimos": "Sistema avançado",
        "oferecimentos": "Palco completo",
        "estrutura_apresentacao": "Palco com 80m²",
        "publico_estimado": "501-1000",
        "fotos_ambiente": ["foto4.jpg", "foto5.jpg"]
    }
    
    create_response = client.post("/api/v1/spaces/", json=space_data)
    space_id = create_response.json()["id"]
    
    # Atualizar o espaço
    update_data = {
        "valor_hora": 250.0,
        "valor_couvert": 35.0,
        "requisitos_minimos": "Sistema premium"
    }
    
    response = client.put(f"/api/v1/spaces/{space_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["valor_hora"] == update_data["valor_hora"]
    assert data["valor_couvert"] == update_data["valor_couvert"]
    assert data["requisitos_minimos"] == update_data["requisitos_minimos"]

def test_delete_space(client: TestClient):
    """Teste para deletar espaço"""
    # Primeiro criar um espaço
    space_data = {
        "profile_id": 2,  # Profile de espaço (ESPACO role)
        "space_type_id": 1,
        "acesso": "Público",
        "dias_apresentacao": ["sábado"],
        "duracao_apresentacao": 1.5,
        "valor_hora": 80.0,
        "valor_couvert": 10.0,
        "requisitos_minimos": "Sistema básico",
        "oferecimentos": "Palco simples",
        "estrutura_apresentacao": "Palco com 20m²",
        "publico_estimado": "<50",
        "fotos_ambiente": ["foto6.jpg"]
    }
    
    create_response = client.post("/api/v1/spaces/", json=space_data)
    space_id = create_response.json()["id"]
    
    # Deletar o espaço
    response = client.delete(f"/api/v1/spaces/{space_id}")
    assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    # Verificar se o espaço foi deletado
    get_response = client.get(f"/api/v1/spaces/{space_id}")
    assert get_response.status_code == 404 