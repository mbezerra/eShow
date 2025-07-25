# Testes do eShow

Este diretório contém todos os testes automatizados para a API do eShow.

## Estrutura dos Testes

```
tests/
├── conftest.py                    # Configuração do pytest e fixtures
├── test_users.py                  # Testes para endpoints de usuários
├── test_auth.py                   # Testes para autenticação
├── test_roles.py                  # Testes para roles
├── test_profiles.py               # Testes para profiles
├── test_artist_types.py           # Testes para tipos de artistas
├── test_musical_styles.py         # Testes para estilos musicais
├── test_artists.py                # Testes para artistas
├── test_artist_musical_styles.py  # Testes para associações artista-estilo
├── test_space_types.py            # Testes para tipos de espaços
├── test_event_types.py            # Testes para tipos de eventos
├── test_festival_types.py         # Testes para tipos de festivais
├── test_spaces.py                 # Testes para espaços
├── test_space_event_types.py      # Testes para associações espaço-evento
├── test_space_festival_types.py   # Testes para associações espaço-festival
├── test_bookings.py               # Testes para bookings
├── test_reviews.py                # Testes para reviews
├── test_financials.py             # Testes para registros financeiros
├── test_interests.py              # Testes para interesses
└── test_location_search.py        # Testes para busca de localização
```

## Como Executar os Testes

### Executar todos os testes
```bash
./run_tests.sh
```

### Executar testes específicos
```bash
# Testes de usuários
pytest tests/test_users.py -v

# Testes de autenticação
pytest tests/test_auth.py -v

# Testes com cobertura
pytest tests/ -v --cov=app --cov-report=html
```

### Executar testes por categoria
```bash
# Apenas testes unitários
pytest tests/ -m unit

# Apenas testes de integração
pytest tests/ -m integration

# Excluir testes lentos
pytest tests/ -m "not slow"
```

## Cobertura de Testes

Cada arquivo de teste cobre as seguintes operações CRUD:

- **CREATE**: Teste de criação de recursos
- **READ**: Teste de listagem e busca por ID
- **UPDATE**: Teste de atualização de recursos
- **DELETE**: Teste de exclusão de recursos

### Endpoints Testados

1. **Users** (`/api/v1/users/`)
   - POST, GET, GET by ID, PUT, DELETE

2. **Auth** (`/api/v1/auth/`)
   - POST /register, POST /login

3. **Roles** (`/api/v1/roles/`)
   - POST, GET, GET by ID, PUT, DELETE

4. **Profiles** (`/api/v1/profiles/`)
   - POST, GET, GET by ID, PUT, DELETE

5. **Artist Types** (`/api/v1/artist-types/`)
   - POST, GET, GET by ID, PUT, DELETE

6. **Musical Styles** (`/api/v1/musical-styles/`)
   - POST, GET, GET by ID, PUT, DELETE

7. **Artists** (`/api/v1/artists/`)
   - POST, GET, GET by ID, PUT, DELETE

8. **Artist Musical Styles** (`/api/v1/artist-musical-styles/`)
   - POST, GET, GET by ID, GET by artist, GET by musical style, DELETE

9. **Space Types** (`/api/v1/space-types/`)
   - POST, GET, GET by ID, PUT, DELETE

10. **Event Types** (`/api/v1/event-types/`)
    - POST, GET, GET by ID, PUT, DELETE

11. **Festival Types** (`/api/v1/festival-types/`)
    - POST, GET, GET by ID, PUT, DELETE

12. **Spaces** (`/api/v1/spaces/`)
    - POST, GET, GET by ID, PUT, DELETE

13. **Space Event Types** (`/api/v1/space-event-types/`)
    - POST, GET, GET by ID, GET by space, GET by event type, DELETE

14. **Space Festival Types** (`/api/v1/space-festival-types/`)
    - POST, GET, GET by ID, GET by space, GET by festival type, DELETE

15. **Bookings** (`/api/v1/bookings/`)
    - POST, GET, GET by ID, PUT, DELETE, GET by space, GET by artist

16. **Reviews** (`/api/v1/reviews/`)
    - POST, GET, GET by ID, PUT, DELETE, GET by booking, GET by user

17. **Financials** (`/api/v1/financials/`)
    - POST, GET, GET by ID, PUT, DELETE, GET by booking, GET by status

18. **Interests** (`/api/v1/interests/`)
    - POST, GET, GET by ID, PUT, DELETE, GET by category

19. **Location Search** (`/api/v1/location-search/`)
    - GET by CEP, GET by city/state, GET by coordinates

## Configuração do Ambiente de Teste

O arquivo `conftest.py` configura:

- Banco de dados SQLite em memória para testes
- Fixtures para sessão do banco de dados
- Cliente de teste da API
- Override das dependências para usar banco de teste

## Dependências de Teste

- `pytest`: Framework de testes
- `pytest-cov`: Plugin para cobertura de código
- `fastapi[testing]`: Cliente de teste do FastAPI

## Relatórios

Após executar os testes com cobertura, você pode visualizar:

- **Relatório no terminal**: Mostra cobertura por arquivo
- **Relatório HTML**: Gerado em `htmlcov/index.html` com detalhes visuais

## Boas Práticas

1. **Isolamento**: Cada teste é independente e não depende de outros
2. **Limpeza**: O banco de dados é limpo após cada teste
3. **Dados de Teste**: Usar dados realistas mas fictícios
4. **Assertions**: Verificar tanto status code quanto conteúdo da resposta
5. **Documentação**: Cada teste tem docstring explicando seu propósito 