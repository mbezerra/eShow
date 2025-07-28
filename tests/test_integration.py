import pytest
import json
import uuid
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

class TestAPIIntegration:
    """Testes de integração para a API completa"""
    
    def get_auth_token_and_user(self, client: TestClient):
        """Helper para obter token de autenticação e criar usuário"""
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
        
        return auth_token, user_id
    
    def test_health_check(self, client: TestClient):
        """Testa o endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["architecture"] == "hexagonal"
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self, client: TestClient):
        """Testa o endpoint raiz"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Bem-vindo à eShow API" in data["message"]
    
    def test_docs_endpoint(self, client: TestClient):
        """Testa se a documentação está acessível"""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_auth_integration_flow(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de autenticação"""
        # 1. Criar usuário
        user_data = {
            "name": "Usuário Teste",
            "email": "usuario.teste@example.com",
            "password": "senha123"
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201, f"Erro ao criar usuário: {response.text}"
        user = response.json()
        assert user["email"] == user_data["email"]
        
        # 2. Fazer login
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200, f"Erro no login: {response.text}"
        token_data = response.json()
        assert "access_token" in token_data
        assert "token_type" in token_data
        
        # 3. Verificar token
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200
        user_info = response.json()
        assert user_info["email"] == user_data["email"]
    
    def test_user_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de usuários"""
        # 1. Criar usuário
        user_data = {
            "name": "Usuário Gerenciamento",
            "email": "gerenciamento@example.com",
            "password": "senha123"
        }
        
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        user = response.json()
        user_id = user["id"]
        
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 2. Buscar usuário por ID
        response = client.get(f"/api/v1/users/{user_id}", headers=headers)
        assert response.status_code == 200
        fetched_user = response.json()
        assert fetched_user["email"] == user_data["email"]
        
        # 3. Atualizar usuário
        update_data = {"name": "Usuário Atualizado"}
        response = client.put(f"/api/v1/users/{user_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "Usuário Atualizado"
        
        # 4. Listar usuários
        response = client.get("/api/v1/users/", headers=headers)
        assert response.status_code == 200
        users = response.json()
        assert len(users) > 0
        
        # 5. Deletar usuário
        response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
        assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    def test_role_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de roles"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Listar roles existentes
        response = client.get("/api/v1/roles/", headers=headers)
        assert response.status_code == 200
        roles = response.json()
        assert len(roles) > 0
        
        # 2. Buscar role específico
        if roles:
            role_id = roles[0]["id"]
            response = client.get(f"/api/v1/roles/{role_id}", headers=headers)
            assert response.status_code == 200
            role = response.json()
            assert role["id"] == role_id
    
    def test_profile_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de perfis"""
        # Obter token de autenticação e criar usuário
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar perfil
        profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Perfil Teste",
            "artistic_name": "Artista Teste",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        
        response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
        assert response.status_code == 201
        profile = response.json()
        profile_id = profile["id"]
        
        # 2. Buscar perfil
        response = client.get(f"/api/v1/profiles/{profile_id}", headers=headers)
        assert response.status_code == 200
        fetched_profile = response.json()
        assert fetched_profile["full_name"] == profile_data["full_name"]
        
        # 3. Atualizar perfil
        update_data = {"bio": "Músico profissional atualizado"}
        response = client.put(f"/api/v1/profiles/{profile_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_profile = response.json()
        assert updated_profile["bio"] == "Músico profissional atualizado"
        
        # 4. Listar perfis
        response = client.get("/api/v1/profiles/", headers=headers)
        assert response.status_code == 200
        profiles = response.json()
        assert len(profiles) > 0
    
    def test_artist_type_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de tipos de artista"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Listar tipos de artista
        response = client.get("/api/v1/artist-types/", headers=headers)
        assert response.status_code == 200
        artist_types = response.json()
        assert len(artist_types) > 0
        
        # 2. Buscar tipo específico
        if artist_types:
            type_id = artist_types[0]["id"]
            response = client.get(f"/api/v1/artist-types/{type_id}", headers=headers)
            assert response.status_code == 200
            artist_type = response.json()
            assert artist_type["id"] == type_id
    
    def test_musical_style_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de estilos musicais"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar estilo musical
        style_data = {"style": "Samba"}
        
        response = client.post("/api/v1/musical-styles/", json=style_data, headers=headers)
        assert response.status_code == 201
        style = response.json()
        style_id = style["id"]
        
        # 2. Buscar estilo
        response = client.get(f"/api/v1/musical-styles/{style_id}", headers=headers)
        assert response.status_code == 200
        fetched_style = response.json()
        assert fetched_style["style"] == "Samba"
        
        # 3. Atualizar estilo
        update_data = {"style": "Samba Rock"}
        response = client.put(f"/api/v1/musical-styles/{style_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_style = response.json()
        assert updated_style["style"] == "Samba Rock"
        
        # 4. Listar estilos
        response = client.get("/api/v1/musical-styles/", headers=headers)
        assert response.status_code == 200
        styles = response.json()
        assert len(styles) > 0
        
        # 5. Deletar estilo
        response = client.delete(f"/api/v1/musical-styles/{style_id}", headers=headers)
        assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    def test_artist_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de artistas"""
        # Obter token de autenticação e criar profile
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar profile primeiro
        profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Teste",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        profile_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
        profile_id = profile_response.json()["id"]
        
        # 1. Criar artista
        artist_data = {
            "profile_id": profile_id,
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        
        response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert response.status_code == 201
        artist = response.json()
        artist_id = artist["id"]
        
        # 2. Buscar artista
        response = client.get(f"/api/v1/artists/{artist_id}", headers=headers)
        assert response.status_code == 200
        fetched_artist = response.json()
        assert fetched_artist["valor_hora"] == 100.0
        
        # 3. Atualizar artista
        update_data = {"valor_hora": 120.0}
        response = client.put(f"/api/v1/artists/{artist_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_artist = response.json()
        assert updated_artist["valor_hora"] == 120.0
        
        # 4. Listar artistas
        response = client.get("/api/v1/artists/", headers=headers)
        assert response.status_code == 200
        artists = response.json()
        assert len(artists) > 0
    
    def test_space_type_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de tipos de espaço"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar tipo de espaço
        space_type_data = {"tipo": "Bar"}
        
        response = client.post("/api/v1/space-types/", json=space_type_data, headers=headers)
        assert response.status_code == 201
        space_type = response.json()
        space_type_id = space_type["id"]
        
        # 2. Buscar tipo de espaço
        response = client.get(f"/api/v1/space-types/{space_type_id}", headers=headers)
        assert response.status_code == 200
        fetched_space_type = response.json()
        assert fetched_space_type["tipo"] == "Bar"
        
        # 3. Atualizar tipo de espaço
        update_data = {"tipo": "Bar Musical"}
        response = client.put(f"/api/v1/space-types/{space_type_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_space_type = response.json()
        assert updated_space_type["tipo"] == "Bar Musical"
        
        # 4. Listar tipos de espaço
        response = client.get("/api/v1/space-types/", headers=headers)
        assert response.status_code == 200
        space_types = response.json()
        assert len(space_types) > 0
        
        # 5. Deletar tipo de espaço
        response = client.delete(f"/api/v1/space-types/{space_type_id}", headers=headers)
        assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    def test_space_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de espaços"""
        # Obter token de autenticação e criar profile
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar profile primeiro
        profile_data = {
            "user_id": user_id,
            "role_id": 3,  # ESPACO
            "full_name": "Espaço Teste",
            "artistic_name": "Espaço",
            "bio": "Espaço para eventos",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        profile_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
        assert profile_response.status_code == 201, f"Erro ao criar profile: {profile_response.text}"
        profile_id = profile_response.json()["id"]
        
        # 1. Criar espaço
        space_data = {
            "profile_id": profile_id,
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
        
        response = client.post("/api/v1/spaces/", json=space_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar espaço: {response.text}"
        space = response.json()
        space_id = space["id"]
        
        # 2. Buscar espaço
        response = client.get(f"/api/v1/spaces/{space_id}", headers=headers)
        assert response.status_code == 200
        fetched_space = response.json()
        assert fetched_space["valor_hora"] == 150.0
        
        # 3. Atualizar espaço
        update_data = {"valor_hora": 180.0}
        response = client.put(f"/api/v1/spaces/{space_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_space = response.json()
        assert updated_space["valor_hora"] == 180.0
        
        # 4. Listar espaços
        response = client.get("/api/v1/spaces/", headers=headers)
        assert response.status_code == 200
        spaces = response.json()
        assert len(spaces) > 0
    
    def test_event_type_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de tipos de evento"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar tipo de evento com nome único
        unique_id = str(uuid.uuid4())[:8]
        event_type_data = {"type": f"Festival Único {unique_id}"}
        
        response = client.post("/api/v1/event-types/", json=event_type_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar event type: {response.text}"
        event_type = response.json()
        event_type_id = event_type["id"]
        
        # 2. Buscar tipo de evento
        response = client.get(f"/api/v1/event-types/{event_type_id}", headers=headers)
        assert response.status_code == 200
        fetched_event_type = response.json()
        assert fetched_event_type["type"] == f"Festival Único {unique_id}"
        
        # 3. Atualizar tipo de evento
        update_data = {"type": "Festival de Música"}
        response = client.put(f"/api/v1/event-types/{event_type_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_event_type = response.json()
        assert updated_event_type["type"] == "Festival de Música"
        
        # 4. Listar tipos de evento
        response = client.get("/api/v1/event-types/", headers=headers)
        assert response.status_code == 200
        event_types = response.json()
        assert len(event_types) > 0
        
        # 5. Deletar tipo de evento
        response = client.delete(f"/api/v1/event-types/{event_type_id}", headers=headers)
        assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    def test_festival_type_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de tipos de festival"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar tipo de festival com nome único
        unique_id = str(uuid.uuid4())[:8]
        festival_type_data = {"type": f"Festival de Jazz {unique_id}"}
        
        response = client.post("/api/v1/festival-types/", json=festival_type_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar festival type: {response.text}"
        festival_type = response.json()
        festival_type_id = festival_type["id"]
        
        # 2. Buscar tipo de festival
        response = client.get(f"/api/v1/festival-types/{festival_type_id}", headers=headers)
        assert response.status_code == 200
        fetched_festival_type = response.json()
        assert fetched_festival_type["type"] == f"Festival de Jazz {unique_id}"
        
        # 3. Atualizar tipo de festival
        update_data = {"type": "Festival Internacional de Jazz"}
        response = client.put(f"/api/v1/festival-types/{festival_type_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_festival_type = response.json()
        assert updated_festival_type["type"] == "Festival Internacional de Jazz"
        
        # 4. Listar tipos de festival
        response = client.get("/api/v1/festival-types/", headers=headers)
        assert response.status_code == 200
        festival_types = response.json()
        assert len(festival_types) > 0
        
        # 5. Deletar tipo de festival
        response = client.delete(f"/api/v1/festival-types/{festival_type_id}", headers=headers)
        assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    def test_booking_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de reservas"""
        # Obter token de autenticação e criar dados necessários
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar profile do artista
        artist_profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Booking",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        artist_profile_response = client.post("/api/v1/profiles/", json=artist_profile_data, headers=headers)
        assert artist_profile_response.status_code == 201, f"Erro ao criar profile do artista: {artist_profile_response.text}"
        artist_profile_id = artist_profile_response.json()["id"]
        
        # Criar artista
        artist_data = {
            "profile_id": artist_profile_id,
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        artist_response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert artist_response.status_code == 201, f"Erro ao criar artista: {artist_response.text}"
        artist_id = artist_response.json()["id"]
        
        # Criar profile do espaço
        space_profile_data = {
            "user_id": user_id,
            "role_id": 3,  # ESPACO
            "full_name": "Espaço Booking",
            "artistic_name": "Espaço",
            "bio": "Espaço para eventos",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        space_profile_response = client.post("/api/v1/profiles/", json=space_profile_data, headers=headers)
        assert space_profile_response.status_code == 201, f"Erro ao criar profile do espaço: {space_profile_response.text}"
        space_profile_id = space_profile_response.json()["id"]
        
        # Criar espaço
        space_data = {
            "profile_id": space_profile_id,
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
        space_response = client.post("/api/v1/spaces/", json=space_data, headers=headers)
        assert space_response.status_code == 201, f"Erro ao criar espaço: {space_response.text}"
        space_id = space_response.json()["id"]
        
        # 1. Criar reserva (artista agendando espaço)
        data_inicio = datetime.now() + timedelta(days=30)
        data_fim = data_inicio + timedelta(hours=2)
        booking_data = {
            "profile_id": artist_profile_id,
            "space_id": space_id,  # Artista agendando espaço
            "data_inicio": data_inicio.isoformat(),
            "horario_inicio": "20:00",
            "data_fim": data_fim.isoformat(),
            "horario_fim": "22:00"
        }
        
        response = client.post("/api/v1/bookings/", json=booking_data, headers=headers)
        assert response.status_code == 201
        booking = response.json()
        booking_id = booking["id"]
        
        # 2. Buscar reserva
        response = client.get(f"/api/v1/bookings/{booking_id}", headers=headers)
        assert response.status_code == 200
        fetched_booking = response.json()
        assert fetched_booking["profile_id"] == artist_profile_id
        
        # 3. Atualizar reserva
        update_data = {"horario_inicio": "21:00", "horario_fim": "23:00"}
        response = client.put(f"/api/v1/bookings/{booking_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_booking = response.json()
        assert updated_booking["horario_inicio"] == "21:00"
        
        # 4. Listar reservas
        response = client.get("/api/v1/bookings/", headers=headers)
        assert response.status_code == 200
        bookings = response.json()
        assert len(bookings) > 0
    
    def test_review_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de avaliações"""
        # Obter token de autenticação e criar booking
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar booking primeiro (simplificado)
        # Criar profile do artista
        artist_profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Review",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        artist_profile_response = client.post("/api/v1/profiles/", json=artist_profile_data, headers=headers)
        assert artist_profile_response.status_code == 201, f"Erro ao criar profile do artista: {artist_profile_response.text}"
        artist_profile_id = artist_profile_response.json()["id"]
        
        # Criar artista
        artist_data = {
            "profile_id": artist_profile_id,
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        artist_response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert artist_response.status_code == 201, f"Erro ao criar artista: {artist_response.text}"
        artist_id = artist_response.json()["id"]
        
        # Criar profile do espaço
        space_profile_data = {
            "user_id": user_id,
            "role_id": 3,  # ESPACO
            "full_name": "Espaço Review",
            "artistic_name": "Espaço",
            "bio": "Espaço para eventos",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        space_profile_response = client.post("/api/v1/profiles/", json=space_profile_data, headers=headers)
        assert space_profile_response.status_code == 201, f"Erro ao criar profile do espaço: {space_profile_response.text}"
        space_profile_id = space_profile_response.json()["id"]
        
        # Criar espaço
        space_data = {
            "profile_id": space_profile_id,
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
        space_response = client.post("/api/v1/spaces/", json=space_data, headers=headers)
        assert space_response.status_code == 201, f"Erro ao criar espaço: {space_response.text}"
        space_id = space_response.json()["id"]
        
        # Criar booking (artista agendando espaço)
        data_inicio = datetime.now() + timedelta(days=30)
        data_fim = data_inicio + timedelta(hours=2)
        booking_data = {
            "profile_id": artist_profile_id,
            "space_id": space_id,  # Artista agendando espaço
            "data_inicio": data_inicio.isoformat(),
            "horario_inicio": "20:00",
            "data_fim": data_fim.isoformat(),
            "horario_fim": "22:00"
        }
        booking_response = client.post("/api/v1/bookings/", json=booking_data, headers=headers)
        assert booking_response.status_code == 201, f"Erro ao criar booking: {booking_response.text}"
        booking_id = booking_response.json()["id"]
        
        # 1. Criar avaliação
        review_data = {
            "profile_id": artist_profile_id,
            "space_event_type_id": 1,  # Usar um space event type existente
            "data_hora": datetime.now().isoformat(),
            "nota": 5,
            "depoimento": "Excelente apresentação! O espaço é muito bem estruturado e a acústica é perfeita."
        }
        
        response = client.post("/api/v1/reviews/", json=review_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar review: {response.text}"
        review = response.json()
        review_id = review["id"]
        
        # 2. Buscar avaliação
        response = client.get(f"/api/v1/reviews/{review_id}", headers=headers)
        assert response.status_code == 200
        fetched_review = response.json()
        assert fetched_review["nota"] == 5
        
        # 3. Atualizar avaliação
        update_data = {"nota": 4, "depoimento": "Muito boa apresentação!"}
        response = client.put(f"/api/v1/reviews/{review_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_review = response.json()
        assert updated_review["nota"] == 4
        
        # 4. Listar avaliações
        response = client.get("/api/v1/reviews/", headers=headers)
        assert response.status_code == 200
        reviews = response.json()
        assert len(reviews) > 0
    
    def test_financial_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento financeiro"""
        # Obter token de autenticação e criar booking
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar profile primeiro
        profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Financial",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        profile_response = client.post("/api/v1/profiles/", json=profile_data, headers=headers)
        assert profile_response.status_code == 201, f"Erro ao criar profile: {profile_response.text}"
        profile_id = profile_response.json()["id"]
        
        # Criar booking simples para o teste (artista agendando espaço)
        data_inicio = datetime.now() + timedelta(days=30)
        data_fim = data_inicio + timedelta(hours=2)
        booking_data = {
            "profile_id": profile_id,
            "space_id": 1,   # Artista agendando espaço
            "data_inicio": data_inicio.isoformat(),
            "horario_inicio": "20:00",
            "data_fim": data_fim.isoformat(),
            "horario_fim": "22:00"
        }
        booking_response = client.post("/api/v1/bookings/", json=booking_data, headers=headers)
        assert booking_response.status_code == 201, f"Erro ao criar booking: {booking_response.text}"
        booking_id = booking_response.json()["id"]
        
        # 1. Criar registro financeiro
        financial_data = {
            "profile_id": profile_id,
            "banco": "001",
            "agencia": "1234",
            "conta": "12345678",
            "tipo_conta": "Corrente",
            "cpf_cnpj": "12345678901",
            "tipo_chave_pix": "CPF",
            "chave_pix": "12345678901",
            "preferencia": "PIX"
        }
        
        response = client.post("/api/v1/financials/", json=financial_data, headers=headers)
        assert response.status_code == 201
        financial = response.json()
        financial_id = financial["id"]
        
        # 2. Buscar registro financeiro
        response = client.get(f"/api/v1/financials/{financial_id}", headers=headers)
        assert response.status_code == 200
        fetched_financial = response.json()
        assert fetched_financial["profile_id"] == profile_id
        
        # 3. Atualizar registro financeiro
        update_data = {"banco": "002"}
        response = client.put(f"/api/v1/financials/{financial_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_financial = response.json()
        assert updated_financial["banco"] == "002"
        
        # 4. Listar registros financeiros
        response = client.get("/api/v1/financials/", headers=headers)
        assert response.status_code == 200
        financials = response.json()
        assert len(financials) > 0
    
    def test_interest_management_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de gerenciamento de interesses"""
        # Obter token de autenticação e criar dados necessários
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar profile do artista
        artist_profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Interest",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        artist_profile_response = client.post("/api/v1/profiles/", json=artist_profile_data, headers=headers)
        assert artist_profile_response.status_code == 201, f"Erro ao criar profile do artista: {artist_profile_response.text}"
        artist_profile_id = artist_profile_response.json()["id"]
        
        # Criar artista
        artist_data = {
            "profile_id": artist_profile_id,
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        artist_response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert artist_response.status_code == 201, f"Erro ao criar artista: {artist_response.text}"
        artist_id = artist_response.json()["id"]
        
        # Criar profile do espaço
        space_profile_data = {
            "user_id": user_id,
            "role_id": 3,  # ESPACO
            "full_name": "Espaço Interest",
            "artistic_name": "Espaço",
            "bio": "Espaço para eventos",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        space_profile_response = client.post("/api/v1/profiles/", json=space_profile_data, headers=headers)
        assert space_profile_response.status_code == 201, f"Erro ao criar profile do espaço: {space_profile_response.text}"
        space_profile_id = space_profile_response.json()["id"]
        
        # Criar espaço
        space_data = {
            "profile_id": space_profile_id,
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
        space_response = client.post("/api/v1/spaces/", json=space_data, headers=headers)
        assert space_response.status_code == 201, f"Erro ao criar espaço: {space_response.text}"
        space_id = space_response.json()["id"]
        
        # 1. Criar interesse
        interest_data = {
            "profile_id_interessado": artist_profile_id,
            "profile_id_interesse": space_profile_id,
            "data_inicial": (datetime.now() + timedelta(days=30)).date().isoformat(),
            "horario_inicial": "20:00",
            "duracao_apresentacao": 2.0,
            "valor_hora_ofertado": 100.0,
            "valor_couvert_ofertado": 20.0,
            "mensagem": "Gostaria de fazer uma apresentação no seu espaço. Tenho experiência com jazz e blues."
        }
        
        response = client.post("/api/v1/interests/", json=interest_data, headers=headers)
        assert response.status_code == 201
        interest = response.json()
        interest_id = interest["id"]
        
        # 2. Buscar interesse
        response = client.get(f"/api/v1/interests/{interest_id}", headers=headers)
        assert response.status_code == 200
        fetched_interest = response.json()
        assert fetched_interest["status"] == "AGUARDANDO_CONFIRMACAO"
        
        # 3. Atualizar interesse
        update_data = {"status": "ACEITO"}
        response = client.put(f"/api/v1/interests/{interest_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_interest = response.json()
        assert updated_interest["status"] == "ACEITO"
        
        # 4. Listar interesses
        response = client.get("/api/v1/interests/", headers=headers)
        assert response.status_code == 200
        interests = response.json()
        assert len(interests) > 0
    
    def test_location_search_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de busca por localização"""
        # 1. Buscar por cidade
        response = client.get("/api/v1/location-search/city/São Paulo/state/SP")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, dict)
        
        # 2. Buscar por CEP
        response = client.get("/api/v1/location-search/cep/01234-567")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, dict)
        
        # 3. Buscar por coordenadas
        response = client.get("/api/v1/location-search/coordinates?lat=-23.5505&lng=-46.6333")
        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, dict)
    
    def test_artist_musical_style_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de relacionamento artista-estilo musical"""
        # Obter token de autenticação e criar dados necessários
        auth_token, user_id = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Criar profile do artista
        artist_profile_data = {
            "user_id": user_id,
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Musical Style",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        artist_profile_response = client.post("/api/v1/profiles/", json=artist_profile_data, headers=headers)
        assert artist_profile_response.status_code == 201, f"Erro ao criar profile do artista: {artist_profile_response.text}"
        artist_profile_id = artist_profile_response.json()["id"]
        
        # Criar artista
        artist_data = {
            "profile_id": artist_profile_id,
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        artist_response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert artist_response.status_code == 201, f"Erro ao criar artista: {artist_response.text}"
        artist_id = artist_response.json()["id"]
        
        # Criar estilo musical com nome único
        unique_id = str(uuid.uuid4())[:8]
        musical_style_data = {"style": f"Jazz {unique_id}"}
        musical_style_response = client.post("/api/v1/musical-styles/", json=musical_style_data, headers=headers)
        assert musical_style_response.status_code == 201, f"Erro ao criar musical style: {musical_style_response.text}"
        musical_style_id = musical_style_response.json()["id"]
        
        # 1. Criar relacionamento
        relationship_data = {
            "artist_id": artist_id,
            "musical_style_id": musical_style_id
        }
        
        response = client.post("/api/v1/artist-musical-styles/", json=relationship_data, headers=headers)
        assert response.status_code == 201
        relationship = response.json()
        relationship_id = relationship["id"]
        
        # 2. Buscar relacionamento
        response = client.get(f"/api/v1/artist-musical-styles/{artist_id}/{musical_style_id}", headers=headers)
        assert response.status_code == 200
        fetched_relationship = response.json()
        assert fetched_relationship["artist_id"] == artist_id
        
        # 3. Listar relacionamentos do artista
        response = client.get(f"/api/v1/artist-musical-styles/artist/{artist_id}", headers=headers)
        assert response.status_code == 200
        relationships = response.json()
        assert len(relationships["items"]) > 0
        
        # 4. Deletar relacionamento
        response = client.delete(f"/api/v1/artist-musical-styles/{artist_id}/{musical_style_id}", headers=headers)
        assert response.status_code == 200  # O endpoint retorna 200, não 204
    
    def test_space_event_type_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de relacionamento espaço-tipo de evento"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar relacionamento
        relationship_data = {
            "space_id": 1,
            "event_type_id": 1,
            "tema": "Show de Jazz",
            "descricao": "Apresentação de jazz com músicos locais",
            "status": "CONTRATANDO",
            "data": (datetime.now() + timedelta(days=7)).isoformat(),
            "horario": "20:00"
        }
        
        response = client.post("/api/v1/space-event-types/", json=relationship_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar space event type: {response.text}"
        relationship = response.json()
        relationship_id = relationship["id"]
        
        # 2. Buscar relacionamento
        response = client.get(f"/api/v1/space-event-types/{relationship_id}", headers=headers)
        assert response.status_code == 200
        fetched_relationship = response.json()
        assert fetched_relationship["tema"] == "Show de Jazz"
        
        # 3. Atualizar relacionamento
        update_data = {"status": "FECHADO"}
        response = client.put(f"/api/v1/space-event-types/{relationship_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_relationship = response.json()
        assert updated_relationship["status"] == "FECHADO"
        
        # 4. Listar relacionamentos
        response = client.get("/api/v1/space-event-types/", headers=headers)
        assert response.status_code == 200
        relationships = response.json()
        assert len(relationships) > 0
    
    def test_space_festival_type_integration(self, client: TestClient, db_session: Session):
        """Testa o fluxo completo de relacionamento espaço-tipo de festival"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar relacionamento
        relationship_data = {
            "space_id": 1,
            "festival_type_id": 1,
            "tema": "Festival de Jazz",
            "descricao": "Festival anual de jazz",
            "status": "CONTRATANDO",
            "data": (datetime.now() + timedelta(days=30)).isoformat(),
            "horario": "18:00"
        }
        
        response = client.post("/api/v1/space-festival-types/", json=relationship_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar space festival type: {response.text}"
        relationship = response.json()
        relationship_id = relationship["id"]
        
        # 2. Buscar relacionamento
        response = client.get(f"/api/v1/space-festival-types/{relationship_id}", headers=headers)
        assert response.status_code == 200
        fetched_relationship = response.json()
        assert fetched_relationship["tema"] == "Festival de Jazz"
        
        # 3. Atualizar relacionamento
        update_data = {"status": "FECHADO"}
        response = client.put(f"/api/v1/space-festival-types/{relationship_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_relationship = response.json()
        assert updated_relationship["status"] == "FECHADO"
        
        # 4. Listar relacionamentos
        response = client.get("/api/v1/space-festival-types/", headers=headers)
        assert response.status_code == 200
        relationships = response.json()
        assert len(relationships) > 0
    
    def test_error_handling_integration(self, client: TestClient):
        """Testa o tratamento de erros da API"""
        # 1. Tentar acessar recurso inexistente (sem autenticação)
        response = client.get("/api/v1/users/999999")
        assert response.status_code == 403  # Forbidden (não autenticado)
        
        # 2. Tentar criar usuário com dados inválidos
        invalid_user_data = {
            "name": "",  # Nome vazio
            "email": "email_invalido",  # Email inválido
            "password": "123"  # Senha muito curta
        }
        response = client.post("/api/v1/users/", json=invalid_user_data)
        assert response.status_code == 422
        
        # 3. Tentar acessar endpoint inexistente
        response = client.get("/api/v1/endpoint-inexistente/")
        assert response.status_code == 404
    
    def test_pagination_integration(self, client: TestClient, db_session: Session):
        """Testa a paginação dos endpoints"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Testar paginação em diferentes endpoints
        endpoints = [
            "/api/v1/users/",
            "/api/v1/artists/",
            "/api/v1/spaces/",
            "/api/v1/bookings/",
            "/api/v1/reviews/"
        ]
        
        for endpoint in endpoints:
            # Testar com parâmetros de paginação
            response = client.get(f"{endpoint}?skip=0&limit=10", headers=headers)
            assert response.status_code == 200, f"Erro no endpoint {endpoint}: {response.text}"
            data = response.json()
            # Verificar se é lista direta ou estrutura com items
            if isinstance(data, dict) and "items" in data:
                assert isinstance(data["items"], list)
            else:
                assert isinstance(data, list)
            
            # Testar com limite diferente
            response = client.get(f"{endpoint}?skip=0&limit=5", headers=headers)
            assert response.status_code == 200, f"Erro no endpoint {endpoint}: {response.text}"
            data = response.json()
            # Verificar se é lista direta ou estrutura com items
            if isinstance(data, dict) and "items" in data:
                assert isinstance(data["items"], list)
            else:
                assert isinstance(data, list)
    
    def test_filtering_integration(self, client: TestClient, db_session: Session):
        """Testa os filtros dos endpoints"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # Testar filtros em artistas
        response = client.get("/api/v1/artists/?artist_type_id=1", headers=headers)
        assert response.status_code == 200, f"Erro no filtro de artistas: {response.text}"
        artists = response.json()
        # Verificar se é lista direta ou estrutura com items
        if isinstance(artists, dict) and "items" in artists:
            assert isinstance(artists["items"], list)
        else:
            assert isinstance(artists, list)
        
        # Testar filtros em espaços
        response = client.get("/api/v1/spaces/?space_type_id=1", headers=headers)
        assert response.status_code == 200, f"Erro no filtro de espaços: {response.text}"
        spaces = response.json()
        # Verificar se é lista direta ou estrutura com items
        if isinstance(spaces, dict) and "items" in spaces:
            assert isinstance(spaces["items"], list)
        else:
            assert isinstance(spaces, list)
        
        # Testar filtros em reservas
        response = client.get("/api/v1/bookings/?status=PENDENTE", headers=headers)
        assert response.status_code == 200, f"Erro no filtro de reservas: {response.text}"
        bookings = response.json()
        # Verificar se é lista direta ou estrutura com items
        if isinstance(bookings, dict) and "items" in bookings:
            assert isinstance(bookings["items"], list)
        else:
            assert isinstance(bookings, list)
    
    def test_complete_workflow_integration(self, client: TestClient, db_session: Session):
        """Testa um fluxo completo de trabalho da aplicação"""
        # Obter token de autenticação
        auth_token, _ = self.get_auth_token_and_user(client)
        headers = {"Authorization": auth_token}
        
        # 1. Criar usuário artista
        artist_user_data = {
            "name": "Artista Completo",
            "email": "artista.completo@example.com",
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=artist_user_data)
        assert response.status_code == 201, f"Erro ao criar usuário artista: {response.text}"
        artist_user = response.json()
        
        # 2. Criar perfil do artista
        artist_profile_data = {
            "user_id": artist_user["id"],
            "role_id": 2,  # ARTISTA
            "full_name": "Artista Completo",
            "artistic_name": "Artista",
            "bio": "Músico profissional",
            "cep": "01234-567",
            "logradouro": "Rua das Flores",
            "numero": "123",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11999999999"
        }
        response = client.post("/api/v1/profiles/", json=artist_profile_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar profile: {response.text}"
        artist_profile = response.json()
        
        # 3. Criar artista
        artist_data = {
            "profile_id": artist_profile["id"],
            "artist_type_id": 1,
            "dias_apresentacao": ["sexta", "sábado"],
            "raio_atuacao": 50.0,
            "duracao_apresentacao": 2.0,
            "valor_hora": 100.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Sistema de som básico"
        }
        response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar artista: {response.text}"
        artist = response.json()
        
        # 4. Criar usuário espaço
        space_user_data = {
            "name": "Espaço Completo",
            "email": "espaco.completo@example.com",
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=space_user_data)
        assert response.status_code == 201
        space_user = response.json()
        
        # 5. Criar perfil do espaço
        space_profile_data = {
            "user_id": space_user["id"],
            "role_id": 3,  # ESPACO
            "full_name": "Espaço Completo",
            "artistic_name": "Espaço",
            "bio": "Local para eventos",
            "cep": "01234-568",
            "logradouro": "Avenida Principal",
            "numero": "456",
            "cidade": "São Paulo",
            "uf": "SP",
            "telefone_movel": "11888888888"
        }
        response = client.post("/api/v1/profiles/", json=space_profile_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar profile do espaço: {response.text}"
        space_profile = response.json()
        
        # 6. Criar espaço
        space_data = {
            "profile_id": space_profile["id"],
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
        response = client.post("/api/v1/spaces/", json=space_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar espaço: {response.text}"
        space = response.json()
        
        # 7. Verificar se todos os dados foram criados corretamente
        assert artist["profile_id"] == artist_profile["id"]
        assert space["profile_id"] == space_profile["id"]
        
        print(f"Fluxo básico testado com sucesso:")
        print(f"- Usuário artista: {artist_user['id']}")
        print(f"- Usuário espaço: {space_user['id']}")
        print(f"- Artista: {artist['id']}")
        print(f"- Espaço: {space['id']}") 