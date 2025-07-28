import pytest
import json
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

class TestAPICoverage:
    """Testes de cobertura para garantir que todos os endpoints estão funcionando"""
    
    def test_all_endpoints_accessible(self, client: TestClient):
        """Testa se todos os endpoints principais estão acessíveis"""
        endpoints = [
            "/health",
            "/",
            "/docs",
            "/api/v1/users/",
            "/api/v1/roles/",
            "/api/v1/profiles/",
            "/api/v1/artist-types/",
            "/api/v1/musical-styles/",
            "/api/v1/artists/",
            "/api/v1/artist-musical-styles/",
            "/api/v1/space-types/",
            "/api/v1/event-types/",
            "/api/v1/festival-types/",
            "/api/v1/spaces/",
            "/api/v1/space-event-types/",
            "/api/v1/space-festival-types/",
            "/api/v1/bookings/",
            "/api/v1/reviews/",
            "/api/v1/financials/",
            "/api/v1/interests/",
            "/api/v1/location-search/city/São Paulo",
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # Aceita 200 (sucesso) ou 404 (não encontrado) como respostas válidas
            assert response.status_code in [200, 404], f"Endpoint {endpoint} retornou {response.status_code}"
    
    def test_data_validation_coverage(self, client: TestClient):
        """Testa a validação de dados em diferentes endpoints"""
        
        # Teste de validação de email
        invalid_user_data = {
            "name": "Teste",
            "email": "email_invalido",
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=invalid_user_data)
        assert response.status_code == 422
        
        # Teste de validação de senha muito curta
        invalid_user_data = {
            "name": "Teste",
            "email": "teste@example.com",
            "password": "123"
        }
        response = client.post("/api/v1/users/", json=invalid_user_data)
        assert response.status_code == 422
        
        # Teste de validação de dados obrigatórios
        incomplete_user_data = {
            "name": "Teste"
            # Faltando email e password
        }
        response = client.post("/api/v1/users/", json=incomplete_user_data)
        assert response.status_code == 422
    
    def test_authentication_coverage(self, client: TestClient):
        """Testa diferentes cenários de autenticação"""
        
        # Teste de login com credenciais inválidas
        invalid_login_data = {
            "username": "usuario_inexistente@example.com",
            "password": "senha_errada"
        }
        response = client.post("/api/v1/auth/login", data=invalid_login_data)
        assert response.status_code == 401
        
        # Teste de acesso sem token
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        
        # Teste de acesso com token inválido
        headers = {"Authorization": "Bearer token_invalido"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_crud_operations_coverage(self, client: TestClient, db_session: Session):
        """Testa operações CRUD completas em diferentes entidades"""
        
        # Teste CRUD para usuários
        user_data = {
            "name": "Usuário CRUD",
            "email": "crud@example.com",
            "password": "senha123"
        }
        
        # Create
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        user = response.json()
        user_id = user["id"]
        
        # Read
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        
        # Update
        update_data = {"name": "Usuário Atualizado"}
        response = client.put(f"/api/v1/users/{user_id}", json=update_data)
        assert response.status_code == 200
        
        # Delete
        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 404
    
    def test_relationship_coverage(self, client: TestClient, db_session: Session):
        """Testa relacionamentos entre entidades"""
        
        # Criar usuário e perfil
        user_data = {
            "name": "Usuário Relacionamento",
            "email": "relacionamento@example.com",
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        user = response.json()
        
        profile_data = {
            "user_id": user["id"],
            "role_id": 1,
            "full_name": "Perfil Relacionamento",
            "artistic_name": "Artista",
            "bio": "Músico",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        response = client.post("/api/v1/profiles/", json=profile_data)
        assert response.status_code == 201
        profile = response.json()
        
        # Verificar se o relacionamento foi criado corretamente
        assert profile["user_id"] == user["id"]
        
        # Criar artista relacionado ao perfil
        artist_data = {
            "profile_id": profile["id"],
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        response = client.post("/api/v1/artists/", json=artist_data)
        assert response.status_code == 201
        artist = response.json()
        
        # Verificar relacionamento artista-perfil
        assert artist["profile_id"] == profile["id"]
    
    def test_business_logic_coverage(self, client: TestClient, db_session: Session):
        """Testa a lógica de negócio da aplicação"""
        
        # Teste de criação de reserva com dados válidos
        booking_data = {
            "artist_id": 1,
            "space_id": 1,
            "data": (datetime.now() + timedelta(days=30)).isoformat(),
            "horario": "20:00",
            "duracao": 2.0,
            "valor_total": 300.0,
            "status": "PENDENTE"
        }
        response = client.post("/api/v1/bookings/", json=booking_data)
        assert response.status_code == 201
        booking = response.json()
        
        # Verificar se a reserva foi criada com status correto
        assert booking["status"] == "PENDENTE"
        
        # Teste de atualização de status da reserva
        update_data = {"status": "CONFIRMADO"}
        response = client.put(f"/api/v1/bookings/{booking['id']}", json=update_data)
        assert response.status_code == 200
        updated_booking = response.json()
        assert updated_booking["status"] == "CONFIRMADO"
    
    def test_error_scenarios_coverage(self, client: TestClient):
        """Testa cenários de erro específicos"""
        
        # Teste de tentativa de criar usuário com email duplicado
        user_data = {
            "name": "Usuário Duplicado",
            "email": "test@example.com",  # Email já existe no banco de teste
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=user_data)
        # Pode retornar 400 (Bad Request) ou 422 (Unprocessable Entity)
        assert response.status_code in [400, 422]
        
        # Teste de tentativa de acessar recurso inexistente
        response = client.get("/api/v1/users/999999")
        assert response.status_code == 404
        
        # Teste de tentativa de atualizar recurso inexistente
        update_data = {"name": "Nome Atualizado"}
        response = client.put("/api/v1/users/999999", json=update_data)
        assert response.status_code == 404
        
        # Teste de tentativa de deletar recurso inexistente
        response = client.delete("/api/v1/users/999999")
        assert response.status_code == 404
    
    def test_data_types_coverage(self, client: TestClient, db_session: Session):
        """Testa diferentes tipos de dados"""
        
        # Teste com dados JSON complexos
        artist_data = {
            "profile_id": 1,
            "artist_type_id": 1,
            "dias_apresentacao": ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"],
            "raio_atuacao": 100.5,
            "duracao_apresentacao": 3.5,
            "valor_hora": 150.75,
            "valor_couvert": 25.50,
            "requisitos_minimos": "Sistema de som profissional com microfones"
        }
        response = client.post("/api/v1/artists/", json=artist_data)
        assert response.status_code == 201
        artist = response.json()
        
        # Verificar se os tipos de dados foram preservados
        assert isinstance(artist["raio_atuacao"], float)
        assert isinstance(artist["duracao_apresentacao"], float)
        assert isinstance(artist["valor_hora"], float)
        assert isinstance(artist["valor_couvert"], float)
        assert isinstance(artist["dias_apresentacao"], list)
    
    def test_search_functionality_coverage(self, client: TestClient):
        """Testa funcionalidades de busca"""
        
        # Teste de busca por cidade
        response = client.get("/api/v1/location-search/city/São Paulo")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        
        # Teste de busca por CEP
        response = client.get("/api/v1/location-search/cep/01234-567")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        
        # Teste de busca por coordenadas
        response = client.get("/api/v1/location-search/coordinates?lat=-23.5505&lng=-46.6333&radius=50")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
    
    def test_pagination_coverage(self, client: TestClient):
        """Testa funcionalidades de paginação"""
        
        # Teste com diferentes parâmetros de paginação
        pagination_tests = [
            {"skip": 0, "limit": 10},
            {"skip": 0, "limit": 5},
            {"skip": 10, "limit": 10},
            {"skip": 20, "limit": 5}
        ]
        
        for params in pagination_tests:
            response = client.get("/api/v1/users/", params=params)
            assert response.status_code == 200
            users = response.json()
            assert isinstance(users, list)
            assert len(users) <= params["limit"]
    
    def test_filtering_coverage(self, client: TestClient):
        """Testa funcionalidades de filtro"""
        
        # Teste de filtros em diferentes endpoints
        filter_tests = [
            ("/api/v1/artists/", {"artist_type_id": 1}),
            ("/api/v1/spaces/", {"space_type_id": 1}),
            ("/api/v1/bookings/", {"status": "PENDENTE"}),
            ("/api/v1/reviews/", {"rating": 5})
        ]
        
        for endpoint, filters in filter_tests:
            response = client.get(endpoint, params=filters)
            assert response.status_code == 200
            results = response.json()
            assert isinstance(results, list)
    
    def test_response_format_coverage(self, client: TestClient):
        """Testa o formato das respostas"""
        
        # Teste de resposta de criação
        user_data = {
            "name": "Usuário Formato",
            "email": "formato@example.com",
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        user = response.json()
        
        # Verificar campos obrigatórios na resposta
        required_fields = ["id", "name", "email", "is_active", "created_at", "updated_at"]
        for field in required_fields:
            assert field in user
        
        # Teste de resposta de listagem
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        
        if users:
            # Verificar se pelo menos um usuário tem os campos obrigatórios
            user = users[0]
            for field in required_fields:
                assert field in user
    
    def test_concurrent_operations_coverage(self, client: TestClient, db_session: Session):
        """Testa operações concorrentes"""
        
        # Criar múltiplos usuários rapidamente
        users_created = []
        for i in range(5):
            user_data = {
                "name": f"Usuário Concorrente {i}",
                "email": f"concorrente{i}@example.com",
                "password": "senha123"
            }
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 201
            users_created.append(response.json())
        
        # Verificar se todos foram criados
        assert len(users_created) == 5
        
        # Verificar se todos têm IDs únicos
        user_ids = [user["id"] for user in users_created]
        assert len(set(user_ids)) == 5
        
        # Limpar usuários criados
        for user in users_created:
            response = client.delete(f"/api/v1/users/{user['id']}")
            assert response.status_code == 204 