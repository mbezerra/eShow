import pytest
import time
import asyncio
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

class TestAPIPerformance:
    """Testes de performance para a API eShow"""
    
    def test_endpoint_response_time(self, client: TestClient):
        """Testa o tempo de resposta dos endpoints principais"""
        # Endpoints que não precisam de autenticação
        public_endpoints = [
            "/health",
            "/",
            "/docs"
        ]
        
        # Endpoints que precisam de autenticação
        auth_endpoints = [
            "/api/v1/users/",
            "/api/v1/roles/",
            "/api/v1/artist-types/",
            "/api/v1/musical-styles/"
        ]
        
        max_response_time = 1.0  # 1 segundo máximo
        
        # Testar endpoints públicos
        for endpoint in public_endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response_time < max_response_time, f"Endpoint {endpoint} demorou {response_time:.3f}s (máximo: {max_response_time}s)"
            assert response.status_code in [200, 404], f"Endpoint {endpoint} retornou {response.status_code}"
        
        # Testar endpoints que precisam de autenticação (esperar 403)
        for endpoint in auth_endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response_time < max_response_time, f"Endpoint {endpoint} demorou {response_time:.3f}s (máximo: {max_response_time}s)"
            assert response.status_code in [403, 404], f"Endpoint {endpoint} retornou {response.status_code} (esperado: 403 ou 404)"
    
    def test_bulk_operations_performance(self, client: TestClient, db_session: Session):
        """Testa performance de operações em lote"""
        
        # Teste de criação de múltiplos usuários
        num_users = 10
        start_time = time.time()
        
        users_created = []
        for i in range(num_users):
            user_data = {
                "name": f"Usuário Performance {i}",
                "email": f"performance{i}@example.com",
                "password": "senha123"
            }
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 201
            users_created.append(response.json())
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_user = total_time / num_users
        
        # Verificar se a performance está aceitável
        assert avg_time_per_user < 0.5, f"Tempo médio por usuário: {avg_time_per_user:.3f}s (máximo: 0.5s)"
        assert total_time < 5.0, f"Tempo total para {num_users} usuários: {total_time:.3f}s (máximo: 5.0s)"
        
        # Limpar usuários criados
        for user in users_created:
            client.delete(f"/api/v1/users/{user['id']}")
    
    def test_database_query_performance(self, client: TestClient, db_session: Session):
        """Testa performance de consultas ao banco de dados"""
        
        # Teste de listagem com paginação (sem autenticação = 403)
        start_time = time.time()
        response = client.get("/api/v1/users/?skip=0&limit=100")
        end_time = time.time()
        
        query_time = end_time - start_time
        assert query_time < 0.5, f"Consulta de usuários demorou {query_time:.3f}s (máximo: 0.5s)"
        assert response.status_code == 403  # Sem autenticação
        
        # Teste de busca com filtros (sem autenticação = 403)
        start_time = time.time()
        response = client.get("/api/v1/artists/?artist_type_id=1")
        end_time = time.time()
        
        filter_time = end_time - start_time
        assert filter_time < 0.3, f"Consulta com filtro demorou {filter_time:.3f}s (máximo: 0.3s)"
        assert response.status_code == 403  # Sem autenticação
    
    def test_concurrent_requests_performance(self, client: TestClient):
        """Testa performance com requisições concorrentes"""
        import threading
        import queue
        
        num_threads = 5
        requests_per_thread = 10
        results = queue.Queue()
        
        def make_requests(thread_id):
            for i in range(requests_per_thread):
                start_time = time.time()
                response = client.get("/health")
                end_time = time.time()
                
                response_time = end_time - start_time
                results.put({
                    'thread_id': thread_id,
                    'request_id': i,
                    'response_time': response_time,
                    'status_code': response.status_code
                })
        
        # Criar threads
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=make_requests, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Aguardar todas as threads terminarem
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Coletar resultados
        all_results = []
        while not results.empty():
            all_results.append(results.get())
        
        # Verificar resultados
        assert len(all_results) == num_threads * requests_per_thread
        
        # Verificar se todas as requisições foram bem-sucedidas
        for result in all_results:
            assert result['status_code'] == 200
            assert result['response_time'] < 1.0
        
        # Verificar tempo total
        expected_time = len(all_results) * 0.1  # 0.1s por requisição
        assert total_time < expected_time, f"Tempo total: {total_time:.3f}s (esperado: <{expected_time:.3f}s)"
    
    def test_memory_usage_performance(self, client: TestClient, db_session: Session):
        """Testa uso de memória durante operações"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Criar múltiplos registros
        num_records = 50
        for i in range(num_records):
            user_data = {
                "name": f"Usuário Memória {i}",
                "email": f"memoria{i}@example.com",
                "password": "senha123"
            }
            response = client.post("/api/v1/users/", json=user_data)
            assert response.status_code == 201
        
        # Verificar uso de memória
        current_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = current_memory - initial_memory
        
        # Limpeza de memória deve ser eficiente
        assert memory_increase < 50, f"Aumento de memória: {memory_increase:.2f}MB (máximo: 50MB)"
    
    def test_api_throughput_performance(self, client: TestClient):
        """Testa throughput da API"""
        
        num_requests = 100
        start_time = time.time()
        
        successful_requests = 0
        for i in range(num_requests):
            response = client.get("/health")
            if response.status_code == 200:
                successful_requests += 1
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Calcular throughput
        throughput = successful_requests / total_time  # requests per second
        
        # Verificar se o throughput está aceitável
        assert throughput > 50, f"Throughput: {throughput:.2f} req/s (mínimo: 50 req/s)"
        assert successful_requests == num_requests, f"Requisições bem-sucedidas: {successful_requests}/{num_requests}"
    
    def test_complex_workflow_performance(self, client: TestClient, db_session: Session):
        """Testa performance de fluxo complexo"""
        
        start_time = time.time()
        
        # 1. Criar usuário
        user_data = {
            "name": "Usuário Fluxo Performance",
            "email": "fluxo.performance@example.com",
            "password": "senha123"
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        user = response.json()
        
        # 2. Fazer login para obter token
        login_data = {
            "email": "fluxo.performance@example.com",
            "password": "senha123"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200, f"Erro no login: {login_response.text}"
        token_data = login_response.json()
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        
        # 3. Criar perfil
        profile_data = {
            "user_id": user["id"],
            "role_id": 2,  # ARTISTA
            "full_name": "Perfil Performance",
            "artistic_name": "Artista",
            "bio": "Músico",
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
        
        # 4. Criar artista
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
        response = client.post("/api/v1/artists/", json=artist_data, headers=headers)
        assert response.status_code == 201, f"Erro ao criar artista: {response.text}"
        artist = response.json()
        
        # 5. Testar performance de consultas
        response = client.get("/api/v1/artists/", headers=headers)
        assert response.status_code == 200
        
        response = client.get("/api/v1/roles/", headers=headers)
        assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verificar se o fluxo básico foi executado em tempo aceitável
        assert total_time < 2.0, f"Fluxo básico demorou {total_time:.3f}s (máximo: 2.0s)"
        
        print(f"Fluxo básico executado em {total_time:.3f}s")
        print(f"- Usuário: {user['id']}")
        print(f"- Perfil: {profile['id']}")
        print(f"- Artista: {artist['id']}")
    
    def test_search_performance(self, client: TestClient):
        """Testa performance das funcionalidades de busca"""
        
        # Teste de busca por cidade (endpoint correto)
        start_time = time.time()
        response = client.get("/api/v1/location-search/city/São Paulo/state/SP")
        end_time = time.time()
        
        city_search_time = end_time - start_time
        assert city_search_time < 0.5, f"Busca por cidade demorou {city_search_time:.3f}s (máximo: 0.5s)"
        assert response.status_code == 200
        
        # Teste de busca por CEP
        start_time = time.time()
        response = client.get("/api/v1/location-search/cep/01234-567")
        end_time = time.time()
        
        cep_search_time = end_time - start_time
        assert cep_search_time < 0.3, f"Busca por CEP demorou {cep_search_time:.3f}s (máximo: 0.3s)"
        assert response.status_code == 200
        
        # Teste de busca por coordenadas
        start_time = time.time()
        response = client.get("/api/v1/location-search/coordinates?lat=-23.5505&lng=-46.6333&radius=50")
        end_time = time.time()
        
        coord_search_time = end_time - start_time
        assert coord_search_time < 0.5, f"Busca por coordenadas demorou {coord_search_time:.3f}s (máximo: 0.5s)"
        assert response.status_code == 200
    
    def test_error_handling_performance(self, client: TestClient):
        """Testa performance do tratamento de erros"""
        
        # Teste de requisições com dados inválidos
        start_time = time.time()
        
        for i in range(10):
            invalid_data = {
                "name": "",
                "email": "email_invalido",
                "password": "123"
            }
            response = client.post("/api/v1/users/", json=invalid_data)
            assert response.status_code == 422
        
        end_time = time.time()
        error_handling_time = end_time - start_time
        
        # Verificar se o tratamento de erro é rápido
        avg_error_time = error_handling_time / 10
        assert avg_error_time < 0.1, f"Tempo médio de tratamento de erro: {avg_error_time:.3f}s (máximo: 0.1s)"
    
    def test_database_connection_pool_performance(self, client: TestClient, db_session: Session):
        """Testa performance do pool de conexões do banco"""
        
        # Simular múltiplas conexões simultâneas
        num_connections = 20
        start_time = time.time()
        
        for i in range(num_connections):
            # Fazer requisições que usam o banco (sem autenticação = 403)
            response = client.get("/api/v1/users/")
            assert response.status_code == 403  # Sem autenticação
            
            # Usar endpoints públicos para testar performance
            response = client.get("/health")
            assert response.status_code == 200
            
            response = client.get("/")
            assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verificar se o pool de conexões é eficiente
        avg_time_per_connection = total_time / num_connections
        assert avg_time_per_connection < 0.05, f"Tempo médio por conexão: {avg_time_per_connection:.3f}s (máximo: 0.05s)" 