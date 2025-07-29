### **Arquitetura Implementada**

O endpoint festival_types implementa uma **arquitetura similar ao event_types** para gerenciamento de tipos de festivais, seguindo os princípios da **Clean Architecture**:

1. **Camada de Apresentação**: FastAPI com endpoints CRUD básicos e validação Pydantic
2. **Camada de Aplicação**: FestivalTypeService com lógica de negócio focada em unicidade
3. **Camada de Domínio**: Entidade FestivalType simples e interface de repositório
4. **Camada de Infraestrutura**: Implementação de repositório com SQLAlchemy

### **Características Principais**

- **Simplicidade**: Estrutura direta para gerenciamento de tipos de festivais
- **Unicidade**: Garantia de que cada tipo de festival seja único
- **Paginação**: Suporte a listagem paginada com skip e limit
- **Validação**: Verificações de existência e unicidade em operações
- **CRUD Completo**: Todas as operações básicas implementadas

### **Endpoints Disponíveis**

1. **POST /festival_types/** - Criar novo tipo de festival
2. **GET /festival_types/** - Listar todos os tipos de festival (com paginação)
3. **GET /festival_types/{id}** - Buscar tipo de festival por ID
4. **PUT /festival_types/{id}** - Atualizar tipo de festival
5. **DELETE /festival_types/{id}** - Deletar tipo de festival

### **Regras de Negócio**

- **Unicidade**: O campo `type` deve ser único na tabela
- **Existência**: Verificação de existência antes de operações de atualização/exclusão
- **Validação de Entrada**: Campo `type` obrigatório (validação básica)
- **Integridade**: Verificação de unicidade na atualização (permitindo atualizar para o mesmo valor)

### **Validações Implementadas**

- **Schema Validation**: Validação de campos obrigatórios via Pydantic
- **Unicidade**: Verificação de duplicatas antes de criar/atualizar
- **Existência**: Verificação de existência antes de operações
- **Paginação**: Parâmetros skip e limit para controle de listagem

### **Estrutura de Dados**

- **Tabela festival_types**: Armazena tipos de festivais com campo único
- **Campo Principal**: `type` (VARCHAR UNIQUE NOT NULL)
- **Timestamps**: Campos created_at e updated_at para rastreamento
- **Relacionamentos**: Referenciado por space_festival_types e bookings

### **Campos Principais**

- **id**: Chave primária auto-incrementada
- **type**: Nome/tipo do festival (único, obrigatório)
- **created_at**: Data/hora de criação
- **updated_at**: Data/hora da última atualização

### **Fluxos Especiais**

- **Validação de Unicidade**: Verificação antes de criar/atualizar
- **Paginação**: Controle de listagem com skip e limit
- **Conversão de Dados**: Transformação entre entidades, modelos e schemas
- **Tratamento de Erros**: Respostas específicas para diferentes cenários de erro

### **Relacionamentos**

- **space_festival_types**: Referenciado pela tabela de tipos de festivais de espaços
- **bookings**: Referenciado pela tabela de agendamentos

### **Comparação com Event Types**

O endpoint festival_types é **muito similar ao event_types**, com as principais diferenças:

1. **Validação de Schema**: Event types tem validação mais robusta (tamanho 1-100 caracteres), enquanto festival types tem validação básica
2. **Schemas**: Event types tem schemas mais detalhados com Field validators
3. **Funcionalidade**: Ambos implementam as mesmas operações CRUD e regras de negócio

### **Arquitetura de Dados**

- **Entidade**: FestivalType com campos id, type, created_at, updated_at
- **Schema**: FestivalTypeBase, FestivalTypeCreate, FestivalTypeUpdate, FestivalTypeResponse
- **Modelo**: FestivalTypeModel com constraints de unicidade e índices
- **Tabela**: festival_types com chave primária e campo type único

# Diagrama de Fluxo - Endpoint Festival Types

  

## Fluxo Detalhado da Arquitetura em Camadas

  

```mermaid

graph TB

%% Cliente

Client[Cliente/Postman]

%% Camada de Apresentação

subgraph "Camada de Apresentação (API)"

Router[FastAPI Router]

Endpoints[Festival Types Endpoints]

Schemas[Festival Type Schemas]

ResponseConverter[Response Converter]

end

%% Camada de Aplicação

subgraph "Camada de Aplicação (Services)"

FestivalTypeService[FestivalTypeService]

Dependencies[Dependency Injection]

end

%% Camada de Domínio

subgraph "Camada de Domínio (Domain)"

FestivalTypeEntity[FestivalType Entity]

FestivalTypeRepoInterface[FestivalTypeRepository Interface]

BusinessRules[Regras de Negócio]

end

%% Camada de Infraestrutura

subgraph "Camada de Infraestrutura (Infrastructure)"

FestivalTypeRepoImpl[FestivalTypeRepositoryImpl]

FestivalTypeModel[FestivalTypeModel SQLAlchemy]

Database[(PostgreSQL Database)]

end

%% Fluxo de Dados

Client --> Router

Router --> Endpoints

Endpoints --> Schemas

Endpoints --> ResponseConverter

Schemas --> Dependencies

Dependencies --> FestivalTypeService

FestivalTypeService --> FestivalTypeRepoInterface

FestivalTypeRepoInterface --> FestivalTypeRepoImpl

FestivalTypeRepoImpl --> FestivalTypeModel

FestivalTypeModel --> Database

%% Entidades

FestivalTypeService --> FestivalTypeEntity

FestivalTypeRepoImpl --> FestivalTypeEntity

FestivalTypeModel --> FestivalTypeEntity

%% Estilos

classDef apiLayer fill:#e1f5fe

classDef appLayer fill:#f3e5f5

classDef domainLayer fill:#e8f5e8

classDef infraLayer fill:#fff3e0

class Router,Endpoints,Schemas,ResponseConverter apiLayer

class FestivalTypeService,Dependencies appLayer

class FestivalTypeEntity,FestivalTypeRepoInterface,BusinessRules domainLayer

class FestivalTypeRepoImpl,FestivalTypeModel,Database infraLayer

```

  

## Fluxo Detalhado por Operação

  

```mermaid

sequenceDiagram

participant C as Cliente

participant API as API Layer

participant Service as Festival Type Service

participant Repo as Repository

participant DB as Database

%% Criação de Festival Type

Note over C,DB: POST /festival_types/ - Criar Festival Type

C->>API: POST /festival_types/ {"type": "Festival de Rock"}

API->>API: Validar FestivalTypeCreate schema

API->>Service: create_festival_type("Festival de Rock")

%% Validação de Unicidade

Service->>Repo: get_by_type("Festival de Rock")

Repo->>DB: SELECT * FROM festival_types WHERE type = 'Festival de Rock'

DB-->>Repo: FestivalTypeModel or None

alt Festival Type já existe

Repo-->>Service: FestivalType entity

Service-->>API: ValueError("FestivalType with type 'Festival de Rock' already exists")

API-->>C: 400 Bad Request

else Festival Type não existe

Service->>Service: Criar FestivalType entity

Service->>Repo: create(festival_type)

Repo->>Repo: Converter para FestivalTypeModel

Repo->>DB: INSERT INTO festival_types (type) VALUES ('Festival de Rock')

DB-->>Repo: Created FestivalTypeModel com ID

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service-->>API: FestivalType entity

API->>API: Converter para FestivalTypeResponse

API-->>C: 201 Created + FestivalTypeResponse

end

%% Listagem com Paginação

Note over C,DB: GET /festival_types/ - Listar Festival Types

C->>API: GET /festival_types/?skip=0&limit=10

API->>Service: get_all_festival_types(skip=0, limit=10)

Service->>Repo: get_all(skip=0, limit=10)

Repo->>DB: SELECT * FROM festival_types LIMIT 10 OFFSET 0

DB-->>Repo: [FestivalTypeModel]

Repo->>Repo: Converter para [FestivalType entities]

Repo-->>Service: [FestivalType entities]

Service-->>API: [FestivalType entities]

API->>API: Converter para [FestivalTypeResponse]

API-->>C: 200 OK + [FestivalTypeResponse]

%% Busca por ID

Note over C,DB: GET /festival_types/{id} - Buscar Festival Type por ID

C->>API: GET /festival_types/1

API->>Service: get_festival_type_by_id(1)

Service->>Repo: get_by_id(1)

Repo->>DB: SELECT * FROM festival_types WHERE id = 1

DB-->>Repo: FestivalTypeModel or None

alt Festival Type encontrado

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service-->>API: FestivalType entity

API->>API: Converter para FestivalTypeResponse

API-->>C: 200 OK + FestivalTypeResponse

else Festival Type não encontrado

Repo-->>Service: None

Service-->>API: None

API-->>C: 404 Not Found

end

%% Atualização

Note over C,DB: PUT /festival_types/{id} - Atualizar Festival Type

C->>API: PUT /festival_types/1 {"type": "Festival de Jazz"}

API->>API: Validar FestivalTypeUpdate schema

API->>Service: update_festival_type(1, "Festival de Jazz")

%% Verificar existência

Service->>Repo: get_by_id(1)

Repo->>DB: SELECT * FROM festival_types WHERE id = 1

DB-->>Repo: FestivalTypeModel or None

alt Festival Type não encontrado

Repo-->>Service: None

Service-->>API: ValueError("FestivalType with id 1 not found")

API-->>C: 400 Bad Request

else Festival Type encontrado

%% Verificar unicidade do novo tipo

Service->>Repo: get_by_type("Festival de Jazz")

Repo->>DB: SELECT * FROM festival_types WHERE type = 'Festival de Jazz'

DB-->>Repo: FestivalTypeModel or None

alt Novo tipo já existe (diferente ID)

Repo-->>Service: FestivalType entity (diferente ID)

Service-->>API: ValueError("FestivalType with type 'Festival de Jazz' already exists")

API-->>C: 400 Bad Request

else Novo tipo não existe ou é o mesmo

Service->>Service: Atualizar type

Service->>Repo: update(festival_type)

Repo->>DB: UPDATE festival_types SET type = 'Festival de Jazz', updated_at = NOW() WHERE id = 1

DB-->>Repo: Updated FestivalTypeModel

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service-->>API: FestivalType entity

API->>API: Converter para FestivalTypeResponse

API-->>C: 200 OK + FestivalTypeResponse

end

end

%% Exclusão

Note over C,DB: DELETE /festival_types/{id} - Deletar Festival Type

C->>API: DELETE /festival_types/1

API->>Service: delete_festival_type(1)

Service->>Repo: delete(1)

Repo->>DB: SELECT * FROM festival_types WHERE id = 1

DB-->>Repo: FestivalTypeModel or None

alt Festival Type encontrado

Repo->>DB: DELETE FROM festival_types WHERE id = 1

DB-->>Repo: Confirmação

Repo-->>Service: true

Service-->>API: true

API-->>C: 200 OK + {"message": "FestivalType com ID 1 foi deletado com sucesso"}

else Festival Type não encontrado

Repo-->>Service: false

Service-->>API: false

API-->>C: 404 Not Found

end

```

  

## Arquitetura de Validação e Regras de Negócio

  

```mermaid

graph TD

subgraph "Validações de Schema"

TypeValidation[type: string obrigatório]

RequiredValidation[type é obrigatório]

end

subgraph "Regras de Negócio"

UniquenessRule[Unicidade do campo type]

ExistenceRule[Verificação de existência por ID]

UpdateUniquenessRule[Unicidade na atualização]

end

subgraph "Validações de Entrada"

CreateValidation[FestivalTypeCreate validation]

UpdateValidation[FestivalTypeUpdate validation]

end

subgraph "Validações de Serviço"

CreateUniquenessCheck[Verificar se type já existe na criação]

UpdateExistenceCheck[Verificar se ID existe na atualização]

UpdateUniquenessCheck[Verificar se novo type já existe na atualização]

end

CreateValidation --> TypeValidation

CreateValidation --> RequiredValidation

UpdateValidation --> TypeValidation

CreateUniquenessCheck --> UniquenessRule

UpdateExistenceCheck --> ExistenceRule

UpdateUniquenessCheck --> UpdateUniquenessRule

TypeValidation --> CreateUniquenessCheck

TypeValidation --> UpdateExistenceCheck

TypeValidation --> UpdateUniquenessCheck

%% Estilos

classDef validation fill:#e3f2fd

classDef rule fill:#ffebee

classDef input fill:#f1f8e9

class TypeValidation,RequiredValidation validation

class UniquenessRule,ExistenceRule,UpdateUniquenessRule rule

class CreateValidation,UpdateValidation input

```

  

## Estrutura de Dados e Modelo de Banco

  

```mermaid

graph TD

subgraph "Entidade de Domínio"

FestivalTypeEntity[FestivalType Entity]

IdField[id: Optional[int]]

TypeField[type: str]

CreatedAtField[created_at: datetime]

UpdatedAtField[updated_at: datetime]

end

subgraph "Schema Pydantic"

FestivalTypeBase[FestivalTypeBase]

FestivalTypeCreate[FestivalTypeCreate]

FestivalTypeUpdate[FestivalTypeUpdate]

FestivalTypeResponse[FestivalTypeResponse]

end

subgraph "Modelo SQLAlchemy"

FestivalTypeModel[FestivalTypeModel]

IdColumn[id: INTEGER PRIMARY KEY]

TypeColumn[type: STRING UNIQUE NOT NULL]

CreatedAtColumn[created_at: TIMESTAMP]

UpdatedAtColumn[updated_at: TIMESTAMP]

end

subgraph "Tabela do Banco"

FestivalTypesTable[(festival_types)]

IdTableField[id: INTEGER PRIMARY KEY]

TypeTableField[type: VARCHAR UNIQUE NOT NULL]

CreatedAtTableField[created_at: TIMESTAMP DEFAULT NOW()]

UpdatedAtTableField[updated_at: TIMESTAMP DEFAULT NOW()]

end

%% Relacionamentos

FestivalTypeEntity --> IdField

FestivalTypeEntity --> TypeField

FestivalTypeEntity --> CreatedAtField

FestivalTypeEntity --> UpdatedAtField

FestivalTypeBase --> TypeField

FestivalTypeCreate --> FestivalTypeBase

FestivalTypeUpdate --> TypeField

FestivalTypeResponse --> FestivalTypeBase

FestivalTypeResponse --> IdField

FestivalTypeResponse --> CreatedAtField

FestivalTypeResponse --> UpdatedAtField

FestivalTypeModel --> IdColumn

FestivalTypeModel --> TypeColumn

FestivalTypeModel --> CreatedAtColumn

FestivalTypeModel --> UpdatedAtColumn

FestivalTypeModel --> FestivalTypesTable

IdColumn --> IdTableField

TypeColumn --> TypeTableField

CreatedAtColumn --> CreatedAtTableField

UpdatedAtColumn --> UpdatedAtTableField

%% Estilos

classDef entity fill:#e8f5e8

classDef schema fill:#fff3e0

classDef model fill:#e1f5fe

classDef table fill:#f3e5f5

class FestivalTypeEntity,IdField,TypeField,CreatedAtField,UpdatedAtField entity

class FestivalTypeBase,FestivalTypeCreate,FestivalTypeUpdate,FestivalTypeResponse schema

class FestivalTypeModel,IdColumn,TypeColumn,CreatedAtColumn,UpdatedAtColumn model

class FestivalTypesTable,IdTableField,TypeTableField,CreatedAtTableField,UpdatedAtTableField table

```

  

## Fluxo de Conversão de Dados

  

```mermaid

sequenceDiagram

participant API as API Layer

participant Service as Service Layer

participant Repo as Repository Layer

participant DB as Database

Note over API,DB: Conversão de Dados entre Camadas

%% Criação

API->>API: Receber FestivalTypeCreate {"type": "Festival de Rock"}

API->>Service: create_festival_type("Festival de Rock")

Service->>Service: Criar FestivalType entity

Service->>Repo: create(festival_type)

Repo->>Repo: Converter para FestivalTypeModel

Repo->>DB: INSERT INTO festival_types (type) VALUES ('Festival de Rock')

DB-->>Repo: FestivalTypeModel com ID gerado

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service-->>API: FestivalType entity

API->>API: Converter para FestivalTypeResponse

API-->>API: Retornar JSON

%% Busca

API->>Service: get_festival_type_by_id(1)

Service->>Repo: get_by_id(1)

Repo->>DB: SELECT * FROM festival_types WHERE id = 1

DB-->>Repo: FestivalTypeModel

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service-->>API: FestivalType entity

API->>API: Converter para FestivalTypeResponse

API-->>API: Retornar JSON

%% Atualização

API->>API: Receber FestivalTypeUpdate {"type": "Festival de Jazz"}

API->>Service: update_festival_type(1, "Festival de Jazz")

Service->>Repo: get_by_id(1)

Repo->>DB: SELECT * FROM festival_types WHERE id = 1

DB-->>Repo: FestivalTypeModel

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service->>Service: Atualizar type

Service->>Repo: update(festival_type)

Repo->>DB: UPDATE festival_types SET type = 'Festival de Jazz', updated_at = NOW()

DB-->>Repo: Updated FestivalTypeModel

Repo->>Repo: Converter para FestivalType entity

Repo-->>Service: FestivalType entity

Service-->>API: FestivalType entity

API->>API: Converter para FestivalTypeResponse

API-->>API: Retornar JSON

%% Listagem

API->>Service: get_all_festival_types(skip=0, limit=10)

Service->>Repo: get_all(skip=0, limit=10)

Repo->>DB: SELECT * FROM festival_types LIMIT 10 OFFSET 0

DB-->>Repo: [FestivalTypeModel]

Repo->>Repo: Converter para [FestivalType entities]

Repo-->>Service: [FestivalType entities]

Service-->>API: [FestivalType entities]

API->>API: Converter para [FestivalTypeResponse]

API-->>API: Retornar JSON array

```

  

## Endpoints e Operações CRUD

  

```mermaid

graph LR

subgraph "Endpoints Disponíveis"

CreateEndpoint[POST /festival_types/]

GetAllEndpoint[GET /festival_types/]

GetByIdEndpoint[GET /festival_types/{id}]

UpdateEndpoint[PUT /festival_types/{id}]

DeleteEndpoint[DELETE /festival_types/{id}]

end

subgraph "Operações CRUD"

CreateOp[Criar Festival Type]

ReadAllOp[Listar Festival Types]

ReadOp[Ler Festival Type]

UpdateOp[Atualizar Festival Type]

DeleteOp[Deletar Festival Type]

end

subgraph "Validações por Operação"

CreateValidation[Validação de unicidade na criação]

ReadValidation[Verificação de existência na leitura]

UpdateValidation[Validação de existência e unicidade na atualização]

DeleteValidation[Verificação de existência na exclusão]

end

subgraph "Respostas"

CreateResponse[201 Created + FestivalTypeResponse]

ReadAllResponse[200 OK + [FestivalTypeResponse]]

ReadResponse[200 OK + FestivalTypeResponse]

UpdateResponse[200 OK + FestivalTypeResponse]

DeleteResponse[200 OK + message]

ErrorResponse[400/404 + error detail]

end

CreateEndpoint --> CreateOp

GetAllEndpoint --> ReadAllOp

GetByIdEndpoint --> ReadOp

UpdateEndpoint --> UpdateOp

DeleteEndpoint --> DeleteOp

CreateOp --> CreateValidation

ReadOp --> ReadValidation

UpdateOp --> UpdateValidation

DeleteOp --> DeleteValidation

CreateValidation --> CreateResponse

ReadAllOp --> ReadAllResponse

ReadValidation --> ReadResponse

UpdateValidation --> UpdateResponse

DeleteValidation --> DeleteResponse

CreateValidation --> ErrorResponse

ReadValidation --> ErrorResponse

UpdateValidation --> ErrorResponse

DeleteValidation --> ErrorResponse

%% Estilos

classDef endpoint fill:#e1f5fe

classDef operation fill:#f3e5f5

classDef validation fill:#fff3e0

classDef response fill:#e8f5e8

class CreateEndpoint,GetAllEndpoint,GetByIdEndpoint,UpdateEndpoint,DeleteEndpoint endpoint

class CreateOp,ReadAllOp,ReadOp,UpdateOp,DeleteOp operation

class CreateValidation,ReadValidation,UpdateValidation,DeleteValidation validation

class CreateResponse,ReadAllResponse,ReadResponse,UpdateResponse,DeleteResponse,ErrorResponse response

```

  

## Arquitetura de Paginação

  

```mermaid

graph TD

subgraph "Parâmetros de Paginação"

SkipParam[skip: int = 0]

LimitParam[limit: int = 100]

end

subgraph "Implementação no Repository"

OffsetQuery[OFFSET skip]

LimitQuery[LIMIT limit]

PaginationQuery[SELECT * FROM festival_types LIMIT limit OFFSET skip]

end

subgraph "Validações de Paginação"

SkipValidation[skip >= 0]

LimitValidation[limit > 0]

MaxLimitValidation[limit <= 1000]

end

subgraph "Resposta Paginada"

FestivalTypesList[List[FestivalTypeResponse]]

TotalCount[Total de registros]

HasNext[Próxima página disponível]

HasPrevious[Página anterior disponível]

end

SkipParam --> SkipValidation

LimitParam --> LimitValidation

LimitParam --> MaxLimitValidation

SkipValidation --> OffsetQuery

LimitValidation --> LimitQuery

MaxLimitValidation --> LimitQuery

OffsetQuery --> PaginationQuery

LimitQuery --> PaginationQuery

PaginationQuery --> FestivalTypesList

PaginationQuery --> TotalCount

TotalCount --> HasNext

TotalCount --> HasPrevious

%% Estilos

classDef param fill:#e3f2fd

classDef query fill:#fff3e0

classDef validation fill:#ffebee

classDef response fill:#e8f5e8

class SkipParam,LimitParam param

class OffsetQuery,LimitQuery,PaginationQuery query

class SkipValidation,LimitValidation,MaxLimitValidation validation

class FestivalTypesList,TotalCount,HasNext,HasPrevious response

```

  

## Modelo de Banco de Dados

  

```mermaid

graph TD

subgraph "Tabela festival_types"

IdColumn[id: INTEGER PRIMARY KEY]

TypeColumn[type: VARCHAR UNIQUE NOT NULL]

CreatedAtColumn[created_at: TIMESTAMP DEFAULT NOW()]

UpdatedAtColumn[updated_at: TIMESTAMP DEFAULT NOW() ON UPDATE NOW()]

end

subgraph "Constraints"

PrimaryKey[PRIMARY KEY (id)]

UniqueType[UNIQUE (type)]

NotNullType[NOT NULL (type)]

IndexType[INDEX (type)]

end

subgraph "Relacionamentos"

SpaceFestivalTypes[space_festival_types.festival_type_id]

Bookings[bookings.space_festival_type_id]

end

subgraph "Operações"

InsertOp[INSERT INTO festival_types (type) VALUES (?)]

SelectOp[SELECT * FROM festival_types WHERE id = ?]

SelectByTypeOp[SELECT * FROM festival_types WHERE type = ?]

SelectAllOp[SELECT * FROM festival_types LIMIT ? OFFSET ?]

UpdateOp[UPDATE festival_types SET type = ?, updated_at = NOW() WHERE id = ?]

DeleteOp[DELETE FROM festival_types WHERE id = ?]

end

IdColumn --> PrimaryKey

TypeColumn --> UniqueType

TypeColumn --> NotNullType

TypeColumn --> IndexType

IdColumn --> SpaceFestivalTypes

IdColumn --> Bookings

PrimaryKey --> SelectOp

UniqueType --> SelectByTypeOp

IndexType --> SelectByTypeOp

PrimaryKey --> UpdateOp

PrimaryKey --> DeleteOp

%% Estilos

classDef column fill:#e1f5fe

classDef constraint fill:#f3e5f5

classDef relationship fill:#e8f5e8

classDef operation fill:#fff3e0

class IdColumn,TypeColumn,CreatedAtColumn,UpdatedAtColumn column

class PrimaryKey,UniqueType,NotNullType,IndexType constraint

class SpaceFestivalTypes,Bookings relationship

class InsertOp,SelectOp,SelectByTypeOp,SelectAllOp,UpdateOp,DeleteOp operation

```

  

## Comparação com Event Types

  

```mermaid

graph TD

subgraph "Event Types"

EventTypeEndpoint[POST /event_types/]

EventTypeService[EventTypeService]

EventTypeEntity[EventType Entity]

EventTypeModel[EventTypeModel]

end

subgraph "Festival Types"

FestivalTypeEndpoint[POST /festival_types/]

FestivalTypeService[FestivalTypeService]

FestivalTypeEntity[FestivalType Entity]

FestivalTypeModel[FestivalTypeModel]

end

subgraph "Características Comuns"

UniquenessValidation[Validação de Unicidade]

CRUDOperations[Operações CRUD]

Pagination[Paginação]

ErrorHandling[Tratamento de Erros]

end

subgraph "Diferenças"

EventTypeValidation[EventType: validação de tamanho 1-100]

FestivalTypeValidation[FestivalType: validação básica]

EventTypeSchema[EventType: schemas mais robustos]

FestivalTypeSchema[FestivalType: schemas simples]

end

EventTypeEndpoint --> EventTypeService

EventTypeService --> EventTypeEntity

EventTypeEntity --> EventTypeModel

FestivalTypeEndpoint --> FestivalTypeService

FestivalTypeService --> FestivalTypeEntity

FestivalTypeEntity --> FestivalTypeModel

EventTypeService --> UniquenessValidation

FestivalTypeService --> UniquenessValidation

EventTypeService --> CRUDOperations

FestivalTypeService --> CRUDOperations

EventTypeService --> Pagination

FestivalTypeService --> Pagination

EventTypeService --> ErrorHandling

FestivalTypeService --> ErrorHandling

EventTypeEntity --> EventTypeValidation

FestivalTypeEntity --> FestivalTypeValidation

EventTypeEntity --> EventTypeSchema

FestivalTypeEntity --> FestivalTypeSchema

%% Estilos

classDef eventType fill:#e1f5fe

classDef festivalType fill:#f3e5f5

classDef common fill:#e8f5e8

classDef difference fill:#fff3e0

class EventTypeEndpoint,EventTypeService,EventTypeEntity,EventTypeModel eventType

class FestivalTypeEndpoint,FestivalTypeService,FestivalTypeEntity,FestivalTypeModel festivalType

class UniquenessValidation,CRUDOperations,Pagination,ErrorHandling common

class EventTypeValidation,FestivalTypeValidation,EventTypeSchema,FestivalTypeSchema difference

```