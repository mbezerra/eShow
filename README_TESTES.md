# 🎵 eShow - Guia Completo de Testes

## 🚀 Início Rápido

### Executar Todos os Testes
```bash
./run_all_tests.sh
```

### Executar Apenas Testes de Integração
```bash
./run_integration_tests.sh
```

### Executar Apenas Testes de Performance
```bash
./run_performance_tests.sh
```

## 📋 Visão Geral

A API eShow possui uma cobertura abrangente de testes que inclui:

- ✅ **Testes Unitários** - Testes individuais de cada componente
- ✅ **Testes de Integração** - Fluxos completos da API
- ✅ **Testes de Performance** - Métricas de tempo e throughput
- ✅ **Cobertura de Código** - Relatórios detalhados de cobertura

## 🏗️ Estrutura de Testes

```
tests/
├── conftest.py                    # Configurações e fixtures compartilhadas
├── test_integration.py            # Testes de integração principais
├── test_integration_coverage.py   # Testes de cobertura específicos
├── test_performance.py            # Testes de performance
├── INTEGRATION_TESTS.md           # Documentação detalhada
└── [outros testes unitários]      # Testes unitários existentes

scripts/
├── run_all_tests.sh              # Suite completa de testes
├── run_integration_tests.sh      # Apenas testes de integração
└── run_performance_tests.sh      # Apenas testes de performance

config/
├── pytest_integration.ini        # Configuração específica para integração
└── pytest.ini                    # Configuração geral do pytest
```

## 🎯 Tipos de Testes

### 1. Testes Unitários
Testam componentes individuais isoladamente.

```bash
# Executar todos os testes unitários
pytest tests/ -k "not integration and not performance"

# Executar teste específico
pytest tests/test_users.py::test_create_user -v
```

### 2. Testes de Integração
Testam fluxos completos da API, incluindo banco de dados.

```bash
# Executar todos os testes de integração
pytest tests/test_integration.py tests/test_integration_coverage.py

# Executar teste específico
pytest tests/test_integration.py::TestAPIIntegration::test_auth_integration_flow -v
```

### 3. Testes de Performance
Testam métricas de tempo, throughput e uso de recursos.

```bash
# Executar todos os testes de performance
pytest tests/test_performance.py

# Executar teste específico
pytest tests/test_performance.py::TestAPIPerformance::test_endpoint_response_time -v
```

## 📊 Relatórios e Cobertura

### Relatórios HTML
- `reports/unit_tests_report.html` - Testes unitários
- `reports/integration_tests_report.html` - Testes de integração
- `reports/performance_tests_report.html` - Testes de performance

### Cobertura de Código
- `htmlcov/unit/index.html` - Cobertura unitária
- `htmlcov/integration/index.html` - Cobertura de integração
- `htmlcov/consolidated/index.html` - Cobertura consolidada

### Visualizar Relatórios
```bash
# Abrir relatório de cobertura consolidado
open htmlcov/consolidated/index.html

# Abrir relatório de testes de integração
open reports/integration_tests_report.html
```

## 🔧 Configuração

### Dependências
```bash
pip install pytest pytest-cov pytest-asyncio httpx psutil pytest-html
```

### Variáveis de Ambiente
```bash
export TESTING=True
export DATABASE_URL="sqlite:///./test.db"
```

### Banco de Dados de Teste
- SQLite em memória para testes rápidos
- Dados de teste pré-populados automaticamente
- Limpeza automática após cada teste

## 🎪 Cenários de Teste

### Fluxos Completos Testados

#### 1. Fluxo de Autenticação
```
Criar usuário → Fazer login → Validar token → Acessar recursos protegidos
```

#### 2. Fluxo de Reserva
```
Criar artista → Criar espaço → Criar reserva → Atualizar status → Criar avaliação
```

#### 3. Fluxo Financeiro
```
Criar reserva → Registrar pagamento → Atualizar status financeiro
```

### Validações Testadas
- ✅ Dados obrigatórios
- ✅ Formatos de email
- ✅ Tamanho de senhas
- ✅ Tipos de dados
- ✅ Relacionamentos entre entidades

### Tratamento de Erros
- ✅ Recursos inexistentes (404)
- ✅ Dados inválidos (422)
- ✅ Conflitos de dados (400)
- ✅ Autenticação falhada (401)

## ⚡ Métricas de Performance

### Tempo de Resposta
- **Máximo**: 1.0s por endpoint
- **Médio**: < 0.5s por operação
- **Fluxo complexo**: < 3.0s total

### Throughput
- **Mínimo**: 50 req/s
- **Objetivo**: 100+ req/s

### Operações em Lote
- **Criação de usuários**: < 0.5s por usuário
- **Consultas com filtro**: < 0.3s
- **Paginação**: < 0.5s

## 🛠️ Comandos Úteis

### Execução de Testes
```bash
# Suite completa
./run_all_tests.sh

# Apenas integração
./run_integration_tests.sh

# Apenas performance
./run_performance_tests.sh

# Teste específico
pytest tests/test_integration.py::TestAPIIntegration::test_auth_integration_flow -v

# Com cobertura
pytest tests/ --cov=app --cov=domain --cov=infrastructure --cov-report=html
```

### Debug e Troubleshooting
```bash
# Executar com debug
pytest -v -s --tb=long

# Ver setup/teardown
pytest --setup-show

# Executar com logs detalhados
pytest -v --log-cli-level=DEBUG
```

### Limpeza
```bash
# Limpar cache do pytest
pytest --cache-clear

# Limpar relatórios
rm -rf reports/ htmlcov/ coverage.xml
```

## 📈 Monitoramento

### Cobertura Mínima
- **Código**: 80%
- **Endpoints**: 100%
- **Fluxos**: 100%

### Alertas de Qualidade
- Testes falhando
- Cobertura abaixo do mínimo
- Performance degradada
- Tempo de resposta alto

## 🔍 Exemplos de Testes

### Teste de Endpoint
```python
def test_create_user(client: TestClient):
    user_data = {
        "name": "Usuário Teste",
        "email": "teste@example.com",
        "password": "senha123"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    user = response.json()
    assert user["email"] == user_data["email"]
```

### Teste de Fluxo Completo
```python
def test_complete_workflow(client: TestClient):
    # 1. Criar usuário
    user = create_user(client)
    
    # 2. Criar perfil
    profile = create_profile(client, user["id"])
    
    # 3. Criar artista
    artist = create_artist(client, profile["id"])
    
    # 4. Criar espaço
    space = create_space(client, profile["id"])
    
    # 5. Criar reserva
    booking = create_booking(client, artist["id"], space["id"])
    
    # Verificar relacionamentos
    assert booking["artist_id"] == artist["id"]
    assert booking["space_id"] == space["id"]
```

### Teste de Performance
```python
def test_endpoint_response_time(client: TestClient):
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()
    
    response_time = end_time - start_time
    assert response_time < 1.0  # Máximo 1 segundo
    assert response.status_code == 200
```

## 🚨 Troubleshooting

### Problemas Comuns

#### 1. Banco de dados não inicializado
```bash
# Verificar se o conftest.py está correto
pytest --setup-show
```

#### 2. Fixtures não encontradas
```bash
# Verificar se o conftest.py está no diretório correto
ls -la tests/conftest.py
```

#### 3. Testes falhando
```bash
# Executar com debug
pytest -v -s --tb=long

# Executar teste específico
pytest tests/test_integration.py::TestAPIIntegration::test_health_check -v -s
```

#### 4. Dependências faltando
```bash
# Instalar dependências
pip install pytest pytest-cov pytest-asyncio httpx psutil pytest-html
```

### Logs e Debug
```bash
# Executar com logs detalhados
pytest -v --log-cli-level=DEBUG

# Ver configuração do pytest
pytest --collect-only

# Executar com coverage detalhado
pytest --cov=app --cov-report=term-missing
```

## 📚 Documentação Adicional

- [Documentação de Testes de Integração](tests/INTEGRATION_TESTS.md)
- [Resumo da Cobertura de Testes](TEST_COVERAGE_SUMMARY.md)
- [Arquitetura da API](ARCHITECTURE.md)
- [Estratégia de Banco de Dados](DATABASE_STRATEGY.md)

## 🤝 Contribuição

### Adicionando Novos Testes
1. Siga o padrão de nomenclatura existente
2. Use fixtures compartilhadas quando possível
3. Documente o cenário de teste
4. Execute todos os testes antes de submeter

### Padrões de Qualidade
- Nomenclatura consistente
- Documentação em português
- Organização clara
- Reutilização de código

---

**Status**: ✅ Implementado e Funcional  
**Última Atualização**: $(date)  
**Versão**: 1.0.0

🎵 **eShow - Conectando Artistas e Espaços através da Tecnologia** 