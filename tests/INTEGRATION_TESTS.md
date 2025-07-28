# Testes de Integração da API eShow

## Visão Geral

Este documento descreve a cobertura de testes de integração implementada para a API eShow, que utiliza arquitetura hexagonal e FastAPI.

## Estrutura dos Testes

### Arquivos de Teste

- `test_integration.py` - Testes de integração principais
- `test_integration_coverage.py` - Testes de cobertura específicos
- `conftest.py` - Configurações e fixtures compartilhadas

### Classes de Teste

#### TestAPIIntegration
Testes de integração abrangentes que cobrem:

1. **Endpoints Básicos**
   - Health check
   - Endpoint raiz
   - Documentação

2. **Autenticação**
   - Fluxo completo de login
   - Validação de tokens
   - Gerenciamento de sessão

3. **Gerenciamento de Usuários**
   - CRUD completo de usuários
   - Validação de dados
   - Tratamento de erros

4. **Gerenciamento de Perfis**
   - Criação e atualização de perfis
   - Relacionamentos com usuários e roles

5. **Gerenciamento de Artistas**
   - CRUD de artistas
   - Relacionamentos com perfis e tipos
   - Validação de dados específicos

6. **Gerenciamento de Espaços**
   - CRUD de espaços
   - Configurações de apresentação
   - Relacionamentos com perfis

7. **Gerenciamento de Reservas**
   - Criação de reservas
   - Atualização de status
   - Relacionamentos com artistas e espaços

8. **Gerenciamento de Avaliações**
   - CRUD de avaliações
   - Relacionamentos com reservas

9. **Gerenciamento Financeiro**
   - Registros financeiros
   - Tipos de transação
   - Status de pagamento

10. **Busca por Localização**
    - Busca por cidade
    - Busca por CEP
    - Busca por coordenadas

#### TestAPICoverage
Testes específicos de cobertura que garantem:

1. **Acessibilidade de Endpoints**
   - Todos os endpoints principais acessíveis
   - Respostas adequadas

2. **Validação de Dados**
   - Validação de emails
   - Validação de senhas
   - Dados obrigatórios

3. **Autenticação**
   - Credenciais inválidas
   - Tokens inválidos
   - Acesso sem autenticação

4. **Operações CRUD**
   - Create, Read, Update, Delete
   - Verificação de exclusão

5. **Relacionamentos**
   - Relacionamentos entre entidades
   - Integridade referencial

6. **Lógica de Negócio**
   - Fluxos de reserva
   - Atualização de status
   - Validações específicas

7. **Cenários de Erro**
   - Dados duplicados
   - Recursos inexistentes
   - Validações de entrada

8. **Tipos de Dados**
   - Preservação de tipos
   - Dados JSON complexos
   - Arrays e objetos

9. **Funcionalidades de Busca**
   - Busca por diferentes critérios
   - Filtros e paginação

10. **Operações Concorrentes**
    - Múltiplas operações simultâneas
    - IDs únicos

## Executando os Testes

### Script Principal
```bash
./run_integration_tests.sh
```

### Comandos Manuais

#### Executar todos os testes de integração
```bash
pytest tests/test_integration.py tests/test_integration_coverage.py -v
```

#### Executar com cobertura
```bash
pytest tests/test_integration.py tests/test_integration_coverage.py \
    --cov=app --cov=domain --cov=infrastructure \
    --cov-report=html:htmlcov/integration \
    --cov-report=term-missing
```

#### Executar testes específicos
```bash
# Teste de autenticação
pytest tests/test_integration.py::TestAPIIntegration::test_auth_integration_flow -v

# Teste de fluxo completo
pytest tests/test_integration.py::TestAPIIntegration::test_complete_workflow_integration -v

# Teste de cobertura de endpoints
pytest tests/test_integration_coverage.py::TestAPICoverage::test_all_endpoints_accessible -v
```

#### Executar com configuração específica
```bash
pytest -c pytest_integration.ini
```

## Cobertura de Testes

### Endpoints Testados

#### Autenticação
- `POST /api/v1/auth/login` - Login de usuário
- `GET /api/v1/auth/me` - Informações do usuário atual

#### Usuários
- `POST /api/v1/users/` - Criar usuário
- `GET /api/v1/users/` - Listar usuários
- `GET /api/v1/users/{id}` - Buscar usuário
- `PUT /api/v1/users/{id}` - Atualizar usuário
- `DELETE /api/v1/users/{id}` - Deletar usuário

#### Perfis
- `POST /api/v1/profiles/` - Criar perfil
- `GET /api/v1/profiles/` - Listar perfis
- `GET /api/v1/profiles/{id}` - Buscar perfil
- `PUT /api/v1/profiles/{id}` - Atualizar perfil

#### Artistas
- `POST /api/v1/artists/` - Criar artista
- `GET /api/v1/artists/` - Listar artistas
- `GET /api/v1/artists/{id}` - Buscar artista
- `PUT /api/v1/artists/{id}` - Atualizar artista

#### Espaços
- `POST /api/v1/spaces/` - Criar espaço
- `GET /api/v1/spaces/` - Listar espaços
- `GET /api/v1/spaces/{id}` - Buscar espaço
- `PUT /api/v1/spaces/{id}` - Atualizar espaço

#### Reservas
- `POST /api/v1/bookings/` - Criar reserva
- `GET /api/v1/bookings/` - Listar reservas
- `GET /api/v1/bookings/{id}` - Buscar reserva
- `PUT /api/v1/bookings/{id}` - Atualizar reserva

#### Avaliações
- `POST /api/v1/reviews/` - Criar avaliação
- `GET /api/v1/reviews/` - Listar avaliações
- `GET /api/v1/reviews/{id}` - Buscar avaliação
- `PUT /api/v1/reviews/{id}` - Atualizar avaliação

#### Financeiro
- `POST /api/v1/financials/` - Criar registro financeiro
- `GET /api/v1/financials/` - Listar registros financeiros
- `GET /api/v1/financials/{id}` - Buscar registro financeiro
- `PUT /api/v1/financials/{id}` - Atualizar registro financeiro

#### Busca por Localização
- `GET /api/v1/location-search/city/{city}` - Buscar por cidade
- `GET /api/v1/location-search/cep/{cep}` - Buscar por CEP
- `GET /api/v1/location-search/coordinates` - Buscar por coordenadas

### Cenários de Teste

#### Fluxos Completos
1. **Fluxo de Autenticação**
   - Criação de usuário
   - Login
   - Validação de token

2. **Fluxo de Reserva**
   - Criação de artista
   - Criação de espaço
   - Criação de reserva
   - Atualização de status
   - Criação de avaliação

3. **Fluxo Financeiro**
   - Criação de reserva
   - Registro de pagamento
   - Atualização de status

#### Validações
- Dados obrigatórios
- Formatos de email
- Tamanho de senhas
- Tipos de dados
- Relacionamentos

#### Tratamento de Erros
- Recursos inexistentes
- Dados inválidos
- Conflitos de dados
- Autenticação falhada

## Configuração do Ambiente

### Variáveis de Ambiente
```bash
export TESTING=True
export DATABASE_URL="sqlite:///./test_integration.db"
```

### Dependências
```bash
pip install pytest pytest-cov pytest-asyncio httpx
```

### Banco de Dados de Teste
- SQLite em memória para testes rápidos
- Dados de teste pré-populados
- Limpeza automática após testes

## Relatórios

### Cobertura de Código
- Relatório HTML: `htmlcov/integration/index.html`
- Relatório XML: `coverage.xml`
- Relatório de terminal com linhas não cobertas

### Métricas
- Cobertura mínima: 80%
- Testes de integração: 100% dos endpoints
- Testes de fluxo: Fluxos principais completos

## Manutenção

### Adicionando Novos Testes
1. Adicione o teste na classe apropriada
2. Use fixtures existentes quando possível
3. Documente o cenário de teste
4. Execute os testes para verificar

### Atualizando Testes
1. Verifique se as mudanças na API afetam os testes
2. Atualize dados de teste conforme necessário
3. Execute testes para garantir que ainda passam
4. Atualize documentação se necessário

### Troubleshooting

#### Problemas Comuns
1. **Banco de dados não inicializado**
   - Verifique se o `conftest.py` está correto
   - Execute `pytest --setup-show` para debug

2. **Fixtures não encontradas**
   - Verifique se o `conftest.py` está no diretório correto
   - Verifique se as fixtures estão definidas

3. **Testes falhando**
   - Verifique logs de erro
   - Execute testes individuais para isolar problemas
   - Verifique se dados de teste estão corretos

#### Debug
```bash
# Executar com debug
pytest -v -s --tb=long

# Executar teste específico com debug
pytest tests/test_integration.py::TestAPIIntegration::test_auth_integration_flow -v -s

# Ver setup/teardown
pytest --setup-show
```

## Contribuição

Para contribuir com os testes:

1. Siga o padrão de nomenclatura existente
2. Use fixtures compartilhadas
3. Documente novos cenários de teste
4. Mantenha a cobertura de código alta
5. Execute todos os testes antes de submeter

## Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Arquitetura Hexagonal](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) 