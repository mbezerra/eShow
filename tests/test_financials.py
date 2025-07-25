import pytest
from fastapi.testclient import TestClient
from datetime import datetime

def test_create_financial(client: TestClient):
    """Teste para criar um registro financeiro"""
    financial_data = {
        "booking_id": 1,
        "amount": 1500.00,
        "currency": "BRL",
        "payment_method": "credit_card",
        "status": "paid",
        "description": "Pagamento do show"
    }
    
    response = client.post("/api/v1/financials/", json=financial_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["booking_id"] == financial_data["booking_id"]
    assert data["amount"] == financial_data["amount"]
    assert data["currency"] == financial_data["currency"]
    assert data["status"] == financial_data["status"]
    assert "id" in data

def test_get_financials(client: TestClient):
    """Teste para listar registros financeiros"""
    response = client.get("/api/v1/financials/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_financial_by_id(client: TestClient):
    """Teste para obter registro financeiro por ID"""
    # Primeiro criar um registro financeiro
    financial_data = {
        "booking_id": 1,
        "amount": 2000.00,
        "currency": "BRL",
        "payment_method": "pix",
        "status": "pending",
        "description": "Pagamento pendente"
    }
    
    create_response = client.post("/api/v1/financials/", json=financial_data)
    financial_id = create_response.json()["id"]
    
    # Agora buscar o registro criado
    response = client.get(f"/api/v1/financials/{financial_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == financial_id
    assert data["booking_id"] == financial_data["booking_id"]

def test_update_financial(client: TestClient):
    """Teste para atualizar registro financeiro"""
    # Primeiro criar um registro financeiro
    financial_data = {
        "booking_id": 1,
        "amount": 1000.00,
        "currency": "BRL",
        "payment_method": "bank_transfer",
        "status": "pending",
        "description": "Transferência bancária"
    }
    
    create_response = client.post("/api/v1/financials/", json=financial_data)
    financial_id = create_response.json()["id"]
    
    # Atualizar o registro
    update_data = {
        "status": "paid",
        "description": "Transferência confirmada"
    }
    
    response = client.put(f"/api/v1/financials/{financial_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == update_data["status"]
    assert data["description"] == update_data["description"]

def test_delete_financial(client: TestClient):
    """Teste para deletar registro financeiro"""
    # Primeiro criar um registro financeiro
    financial_data = {
        "booking_id": 1,
        "amount": 500.00,
        "currency": "BRL",
        "payment_method": "cash",
        "status": "cancelled",
        "description": "Registro temporário"
    }
    
    create_response = client.post("/api/v1/financials/", json=financial_data)
    financial_id = create_response.json()["id"]
    
    # Deletar o registro
    response = client.delete(f"/api/v1/financials/{financial_id}")
    assert response.status_code == 204
    
    # Verificar se o registro foi deletado
    get_response = client.get(f"/api/v1/financials/{financial_id}")
    assert get_response.status_code == 404

def test_get_financials_by_booking(client: TestClient):
    """Teste para obter registros financeiros de um booking específico"""
    # Primeiro criar um registro financeiro
    financial_data = {
        "booking_id": 1,
        "amount": 3000.00,
        "currency": "BRL",
        "payment_method": "credit_card",
        "status": "paid",
        "description": "Teste por booking"
    }
    
    client.post("/api/v1/financials/", json=financial_data)
    
    # Buscar registros do booking
    response = client.get("/api/v1/financials/booking/1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)

def test_get_financials_by_status(client: TestClient):
    """Teste para obter registros financeiros por status"""
    # Primeiro criar um registro financeiro
    financial_data = {
        "booking_id": 1,
        "amount": 2500.00,
        "currency": "BRL",
        "payment_method": "pix",
        "status": "paid",
        "description": "Teste por status"
    }
    
    client.post("/api/v1/financials/", json=financial_data)
    
    # Buscar registros por status
    response = client.get("/api/v1/financials/status/paid")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list) 