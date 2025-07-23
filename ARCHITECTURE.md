# Arquitetura Hexagonal - eShow API

## Visão Geral

Esta API foi construída seguindo os princípios da **Arquitetura Hexagonal** (também conhecida como Arquitetura de Portas e Adaptadores), que promove a separação de responsabilidades e facilita a manutenção e testabilidade do código.

## Estrutura da Arquitetura

### 1. Domínio (Core) - `domain/`

O domínio contém as regras de negócio e é independente de qualquer tecnologia externa.

#### Entidades (`domain/entities/`)
- **User**: Entidade que representa um usuário do sistema
- **Artist**: Entidade que representa um artista do sistema
- **Profile**: Entidade que representa um perfil de usuário
- **Role**: Entidade que representa um papel/função no sistema
- **ArtistType**: Entidade que representa um tipo de artista
- **MusicalStyle**: Entidade que representa um estilo musical
- **SpaceType**: Entidade que representa um tipo de espaço
- **EventType**: Entidade que representa um tipo de evento
- **FestivalType**: Entidade que representa um tipo de festival
- **Space**: Entidade que representa um espaço para apresentações

#### Repositórios (`domain/repositories/`)
- **UserRepository**: Interface para operações de usuários
- **ArtistRepository**: Interface para operações de artistas
- **ProfileRepository**: Interface para operações de perfis
- **RoleRepository**: Interface para operações de papéis
- **ArtistTypeRepository**: Interface para operações de tipos de artista
- **MusicalStyleRepository**: Interface para operações de estilos musicais
- **SpaceTypeRepository**: Interface para operações de tipos de espaço
- **EventTypeRepository**: Interface para operações de tipos de evento
- **FestivalTypeRepository**: Interface para operações de tipos de festival
- **SpaceRepository**: Interface para operações de espaços

### 2. Aplicação (`app/`)

A camada de aplicação contém os casos de uso e adaptadores de entrada.

#### API (`app/api/`)
- **Endpoints**: Controllers que expõem a API REST
- **Schemas**: Modelos Pydantic para validação de dados

#### Serviços (`app/application/services/`)
- **UserService**: Orquestra as operações de usuários
- **ArtistService**: Orquestra as operações de artistas
- **ProfileService**: Orquestra as operações de perfis
- **RoleService**: Orquestra as operações de papéis
- **ArtistTypeService**: Orquestra as operações de tipos de artista
- **MusicalStyleService**: Orquestra as operações de estilos musicais
- **SpaceTypeService**: Orquestra as operações de tipos de espaço
- **EventTypeService**: Orquestra as operações de tipos de evento
- **FestivalTypeService**: Orquestra as operações de tipos de festival
- **SpaceService**: Orquestra as operações de espaços

### 3. Infraestrutura (`infrastructure/`)

A camada de infraestrutura contém os adaptadores de saída.

#### Banco de Dados (`infrastructure/database/`)
- **Models**: Modelos SQLAlchemy para persistência
- **Database**: Configuração de conexão

#### Repositórios (`infrastructure/repositories/`)
- **UserRepositoryImpl**: Implementação concreta do repositório de usuários
- **ArtistRepositoryImpl**: Implementação concreta do repositório de artistas
- **ProfileRepositoryImpl**: Implementação concreta do repositório de perfis
- **RoleRepositoryImpl**: Implementação concreta do repositório de papéis
- **ArtistTypeRepositoryImpl**: Implementação concreta do repositório de tipos de artista
- **MusicalStyleRepositoryImpl**: Implementação concreta do repositório de estilos musicais
- **SpaceTypeRepositoryImpl**: Implementação concreta do repositório de tipos de espaço
- **EventTypeRepositoryImpl**: Implementação concreta do repositório de tipos de evento
- **FestivalTypeRepositoryImpl**: Implementação concreta do repositório de tipos de festival
- **SpaceRepositoryImpl**: Implementação concreta do repositório de espaços

## Fluxo de Dados

```
API Endpoint → Service → Repository Interface → Repository Implementation → Database
```

### Exemplo: Criar Usuário

1. **API Endpoint** (`app/api/endpoints/users.py`)
   - Recebe requisição HTTP
   - Valida dados com Pydantic
   - Chama o serviço

2. **Service** (`app/application/services/user_service.py`)
   - Contém regras de negócio
   - Cria entidade de domínio
   - Chama repositório

3. **Repository Interface** (`domain/repositories/user_repository.py`)
   - Define contrato abstrato

4. **Repository Implementation** (`infrastructure/repositories/user_repository_impl.py`)
   - Implementa persistência no banco
   - Retorna entidade de domínio

5. **Database** (`infrastructure/database/models/user_model.py`)
   - Modelo SQLAlchemy para persistência

## Benefícios da Arquitetura

### 1. Separação de Responsabilidades
- **Domínio**: Regras de negócio puras
- **Aplicação**: Casos de uso
- **Infraestrutura**: Detalhes técnicos

### 2. Testabilidade
- Cada camada pode ser testada independentemente
- Fácil mock de dependências
- Testes unitários isolados

### 3. Flexibilidade
- Troca de banco de dados sem afetar domínio
- Múltiplas interfaces (REST, GraphQL, CLI)
- Fácil adição de novos recursos

### 4. Manutenibilidade
- Código organizado e previsível
- Mudanças localizadas
- Documentação clara

## Injeção de Dependência

O projeto utiliza injeção de dependência para conectar as camadas:

```python
# app/application/dependencies.py
async def get_user_service():
    user_repository = await get_user_repository()
    return UserService(user_repository)
```

## Testes

### Estrutura de Testes
- **Unitários**: Testam cada camada isoladamente
- **Integração**: Testam fluxo completo
- **E2E**: Testam API completa

### Executar Testes
```bash
pytest tests/
```

## Migrações

O projeto usa Alembic para gerenciar migrações do banco:

```bash
# Criar migração
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrações
alembic upgrade head
```

## Funcionalidades Especiais

### Parâmetro `include_relations`

Implementado nos endpoints GET de Artists e Spaces para otimizar o carregamento de dados relacionados:

#### Como Funciona
- **Sem `include_relations`**: Retorna apenas a entidade principal com IDs dos relacionamentos
- **Com `include_relations=true`**: Retorna a entidade principal + dados completos dos relacionamentos

#### Implementação Técnica
1. **Repository Layer**: Usa SQLAlchemy `joinedload` para carregar relacionamentos
2. **Service Layer**: Passa o parâmetro para o repositório
3. **API Layer**: Expõe como query parameter opcional

#### Exemplo de Uso
```bash
# Sem relacionamentos
GET /api/v1/spaces/1

# Com relacionamentos
GET /api/v1/spaces/1?include_relations=true
```

#### Relacionamentos Incluídos
- **Artists**: profile, artist_type
- **Spaces**: profile, space_type, event_type, festival_type

#### Benefícios
- **Performance**: Evita N+1 queries
- **Flexibilidade**: Cliente decide quando carregar relacionamentos
- **Compatibilidade**: Mantém compatibilidade com versões anteriores

## Próximos Passos

1. Implementar autenticação JWT
2. Adicionar validações de negócio
3. Implementar cache Redis
4. Adicionar logs estruturados
5. Configurar CI/CD
6. Implementar documentação OpenAPI 