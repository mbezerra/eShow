import pytest
from fastapi.testclient import TestClient

def test_create_role(client: TestClient):
    """Teste para criar um role"""
    # Testar criação de um role que não existe
    role_data = {
        "name": "TestRole"
    }
    
    response = client.post("/api/v1/roles/", json=role_data)
    print(f"Create role response: {response.status_code} - {response.json()}")  # Debug
    # Deve falhar porque "TestRole" não é um RoleType válido
    assert response.status_code == 400
    assert "não é válido" in response.json()["detail"]

def test_get_roles(client: TestClient):
    """Teste para listar roles"""
    response = client.get("/api/v1/roles/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_role_by_id(client: TestClient):
    """Teste para obter role por ID"""
    # Usar um role existente (ID 1 deve existir após a inicialização)
    role_id = 1
    
    # Buscar o role
    response = client.get(f"/api/v1/roles/{role_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == role_id
    assert "name" in data

def test_update_role(client: TestClient):
    """Teste para atualizar role"""
    # Usar um role existente (ID 2 deve existir após a inicialização)
    role_id = 2
    
    # Atualizar o role
    update_data = {
        "name": "Artista"
    }
    
    response = client.put(f"/api/v1/roles/{role_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]

def test_delete_role(client: TestClient):
    """Teste para deletar role"""
    # Tentar deletar um role que está sendo usado (ID 2 = ESPACO)
    role_id = 2
    
    # Tentar deletar o role
    try:
        response = client.delete(f"/api/v1/roles/{role_id}")
        # Se não ocorrer exceção, deve retornar erro devido à integridade referencial
        assert response.status_code in (400, 409, 500)
    except Exception as e:
        # Se ocorrer uma exceção de integridade, o teste também é considerado sucesso
        assert "IntegrityError" in str(e) or "NOT NULL constraint failed" in str(e) 