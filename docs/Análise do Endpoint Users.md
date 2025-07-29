### **Arquitetura em Camadas**

O endpoint users segue uma arquitetura em camadas bem definida, implementando o padrão **Clean Architecture** com as seguintes camadas:

#### **1. Camada de Apresentação (API Layer)**
- **Arquivo**: `app/api/endpoints/users.py`
- **Responsabilidade**: Receber requisições HTTP, validar dados de entrada e retornar respostas
- **Componentes**: FastAPI Router, endpoints HTTP (GET, POST, PUT, DELETE)

#### **2. Camada de Aplicação (Application Layer)**
- **Arquivos**: 
  - `app/application/services/user_service.py`
  - `app/application/services/auth_service.py`
  - `app/application/dependencies.py`
- **Responsabilidade**: Orquestrar a lógica de negócio, coordenar entre domínio e infraestrutura
- **Componentes**: Services, Dependencies (Injeção de Dependência)

#### **3. Camada de Domínio (Domain Layer)**
- **Arquivos**:
  - `domain/entities/user.py`
  - `domain/repositories/user_repository.py`
- **Responsabilidade**: Contém as regras de negócio centrais e interfaces dos repositórios
- **Componentes**: Entidades, Interfaces de Repositório

#### **4. Camada de Infraestrutura (Infrastructure Layer)**
- **Arquivos**:
  - `infrastructure/repositories/user_repository_impl.py`
  - `infrastructure/database/models/user_model.py`
  - `infrastructure/database/database.py`
- **Responsabilidade**: Implementação concreta de persistência e acesso a dados
- **Componentes**: Implementações de Repositório, Modelos SQLAlchemy, Banco de Dados

### **Fluxo Detalhado por Endpoint**

#### **POST /users/ (Criar Usuário)**
1. **Recepção**: FastAPI recebe requisição com dados do usuário
2. **Validação**: Pydantic valida o schema `UserRegister`
3. **Injeção**: Dependency injection fornece `UserService`
4. **Orquestração**: `AuthService.register_user()` é chamado
5. **Hash de Senha**: `get_password_hash()` criptografa a senha
6. **Criação**: `UserService.create_user()` cria entidade de domínio
7. **Persistência**: `UserRepositoryImpl.create()` salva no banco
8. **Resposta**: Retorna `UserResponse` com dados do usuário criado

#### **GET /users/me (Usuário Atual)**
1. **Autenticação**: `get_current_active_user()` valida token JWT
2. **Verificação**: Token é verificado e decodificado
3. **Busca**: Usuário é recuperado do banco
4. **Resposta**: Retorna dados do usuário autenticado

#### **GET /users/ (Listar Usuários)**
1. **Autenticação**: Verifica se usuário está autenticado
2. **Paginação**: Parâmetros `skip` e `limit` são processados
3. **Busca**: `UserService.get_users()` recupera lista paginada
4. **Transformação**: Entidades são convertidas para schemas de resposta
5. **Resposta**: Lista de `UserResponse` é retornada

#### **GET /users/{user_id} (Buscar Usuário Específico)**
1. **Autenticação**: Verifica autenticação do usuário
2. **Busca**: `UserService.get_user_by_id()` busca usuário específico
3. **Validação**: Verifica se usuário existe
4. **Resposta**: Retorna `UserResponse` ou erro 404

#### **PUT /users/{user_id} (Atualizar Usuário)**
1. **Autenticação**: Verifica autenticação
2. **Validação**: Pydantic valida `UserUpdate` schema
3. **Busca**: Recupera usuário existente
4. **Atualização**: Aplica mudanças na entidade
5. **Persistência**: Salva alterações no banco
6. **Resposta**: Retorna usuário atualizado

#### **DELETE /users/{user_id} (Deletar Usuário)**
1. **Autenticação**: Verifica autenticação
2. **Exclusão**: `UserService.delete_user()` remove do banco
3. **Validação**: Verifica se exclusão foi bem-sucedida
4. **Resposta**: Retorna mensagem de confirmação

### **Diagrama de Fluxo em Mermaid**

## Resumo da Análise do Endpoint Users

### **Arquitetura Implementada**

O endpoint users implementa uma **arquitetura em camadas bem estruturada** seguindo os princípios da **Clean Architecture**:

1. **Camada de Apresentação**: FastAPI com endpoints REST, validação Pydantic e middleware de autenticação
2. **Camada de Aplicação**: Services que orquestram a lógica de negócio e dependency injection
3. **Camada de Domínio**: Entidades puras e interfaces de repositório
4. **Camada de Infraestrutura**: Implementações concretas de persistência com SQLAlchemy

### **Características Principais**

- **Separação de Responsabilidades**: Cada camada tem responsabilidades bem definidas
- **Inversão de Dependência**: Interfaces no domínio, implementações na infraestrutura
- **Autenticação JWT**: Sistema robusto de autenticação com tokens
- **Validação de Dados**: Schemas Pydantic para validação de entrada e saída
- **Tratamento de Erros**: HTTP exceptions apropriadas para diferentes cenários
- **Paginação**: Suporte a listagem paginada de usuários

### **Endpoints Disponíveis**

1. **POST /users/** - Criar usuário (com hash de senha)
2. **GET /users/me** - Obter usuário atual autenticado
3. **GET /users/** - Listar usuários (com paginação)
4. **GET /users/{id}** - Buscar usuário específico
5. **PUT /users/{id}** - Atualizar usuário
6. **DELETE /users/{id}** - Deletar usuário

### **Segurança**

- **Hash de Senhas**: Senhas são criptografadas antes do armazenamento
- **Autenticação JWT**: Tokens Bearer para autenticação
- **Validação de Token**: Verificação de validade e tipo de token
- **Blacklist**: Sistema para invalidar tokens (estrutura preparada)

# Diagrama de Fluxo - Endpoint Users

## Fluxo Detalhado da Arquitetura em Camadas

  

```mermaid

graph TB

%% Cliente

Client[Cliente/Postman]

%% Camada de Apresentação

subgraph "Camada de Apresentação (API)"

Router[FastAPI Router]

Endpoints[Endpoints Users]

AuthMiddleware[Middleware de Autenticação]

Schemas[Pydantic Schemas]

end

%% Camada de Aplicação

subgraph "Camada de Aplicação (Services)"

UserService[UserService]

AuthService[AuthService]

Dependencies[Dependency Injection]

end

%% Camada de Domínio

subgraph "Camada de Domínio (Domain)"

UserEntity[User Entity]

UserRepoInterface[UserRepository Interface]

BusinessRules[Regras de Negócio]

end

%% Camada de Infraestrutura

subgraph "Camada de Infraestrutura (Infrastructure)"

UserRepoImpl[UserRepositoryImpl]

UserModel[UserModel SQLAlchemy]

Database[(PostgreSQL Database)]

end

%% Fluxo de Dados

Client --> Router

Router --> Endpoints

Endpoints --> AuthMiddleware

AuthMiddleware --> Schemas

Schemas --> Dependencies

Dependencies --> UserService

Dependencies --> AuthService

UserService --> UserRepoInterface

AuthService --> UserService

UserRepoInterface --> UserRepoImpl

UserRepoImpl --> UserModel

UserModel --> Database

%% Entidades

UserService --> UserEntity

UserRepoImpl --> UserEntity

UserModel --> UserEntity

%% Estilos

classDef apiLayer fill:#e1f5fe

classDef appLayer fill:#f3e5f5

classDef domainLayer fill:#e8f5e8

classDef infraLayer fill:#fff3e0

class Router,Endpoints,AuthMiddleware,Schemas apiLayer

class UserService,AuthService,Dependencies appLayer

class UserEntity,UserRepoInterface,BusinessRules domainLayer

class UserRepoImpl,UserModel,Database infraLayer

```

  

## Fluxo Detalhado por Operação

  

```mermaid

sequenceDiagram

participant C as Cliente

participant API as API Layer

participant Auth as Auth Service

participant UserS as User Service

participant Repo as Repository

participant DB as Database

%% Criação de Usuário

Note over C,DB: POST /users/ - Criar Usuário

C->>API: POST /users/ {name, email, password}

API->>API: Validar UserRegister schema

API->>Auth: register_user(user_data)

Auth->>Auth: get_password_hash(password)

Auth->>UserS: create_user(user_create)

UserS->>UserS: Verificar email duplicado

UserS->>UserS: Criar User entity

UserS->>Repo: create(user)

Repo->>DB: INSERT INTO users

DB-->>Repo: UserModel

Repo-->>UserS: User entity

UserS-->>Auth: UserResponse

Auth-->>API: UserResponse

API-->>C: 201 Created + UserResponse

%% Autenticação

Note over C,DB: GET /users/me - Usuário Atual

C->>API: GET /users/me + Bearer Token

API->>API: get_current_active_user()

API->>Auth: Verificar token JWT

Auth->>UserS: get_user_by_id(user_id)

UserS->>Repo: get_by_id(user_id)

Repo->>DB: SELECT * FROM users WHERE id = ?

DB-->>Repo: UserModel

Repo-->>UserS: User entity

UserS-->>API: UserResponse

API-->>C: 200 OK + UserResponse

%% Listagem

Note over C,DB: GET /users/ - Listar Usuários

C->>API: GET /users/?skip=0&limit=100 + Bearer Token

API->>API: get_current_active_user()

API->>UserS: get_users(skip, limit)

UserS->>Repo: get_all(skip, limit)

Repo->>DB: SELECT * FROM users LIMIT ? OFFSET ?

DB-->>Repo: [UserModel]

Repo-->>UserS: [User entity]

UserS-->>API: [UserResponse]

API-->>C: 200 OK + [UserResponse]

%% Atualização

Note over C,DB: PUT /users/{id} - Atualizar Usuário

C->>API: PUT /users/1 + {name, email} + Bearer Token

API->>API: get_current_active_user()

API->>API: Validar UserUpdate schema

API->>UserS: update_user(user_id, user_data)

UserS->>Repo: get_by_id(user_id)

Repo->>DB: SELECT * FROM users WHERE id = ?

DB-->>Repo: UserModel

Repo-->>UserS: User entity

UserS->>UserS: Atualizar campos

UserS->>Repo: update(user)

Repo->>DB: UPDATE users SET ...

DB-->>Repo: UserModel atualizado

Repo-->>UserS: User entity

UserS-->>API: UserResponse

API-->>C: 200 OK + UserResponse

%% Exclusão

Note over C,DB: DELETE /users/{id} - Deletar Usuário

C->>API: DELETE /users/1 + Bearer Token

API->>API: get_current_active_user()

API->>UserS: delete_user(user_id)

UserS->>Repo: delete(user_id)

Repo->>DB: DELETE FROM users WHERE id = ?

DB-->>Repo: Resultado da exclusão

Repo-->>UserS: boolean

UserS-->>API: boolean

API-->>C: 200 OK + {"message": "Usuário deletado"}

```

  

## Arquitetura de Dependências

  

```mermaid

graph TD

%% Dependências principais

API[API Endpoints] --> UserService

API --> AuthService

API --> Dependencies

UserService --> UserRepository

AuthService --> UserService

Dependencies --> UserRepositoryImpl

Dependencies --> UserService

UserRepositoryImpl --> UserModel

UserRepositoryImpl --> Database

%% Interfaces e implementações

UserRepository -.->|implements| UserRepositoryImpl

%% Schemas

API --> UserSchemas[User Schemas]

UserService --> UserSchemas

%% Entidades

UserService --> UserEntity

UserRepositoryImpl --> UserEntity

%% Estilos

classDef interface fill:#e3f2fd

classDef implementation fill:#f1f8e9

classDef schema fill:#fff8e1

class UserRepository interface

class UserRepositoryImpl,UserService,AuthService implementation

class UserSchemas schema

```

  

## Fluxo de Autenticação JWT

  

```mermaid

sequenceDiagram

participant C as Cliente

participant API as API Layer

participant Auth as Auth Middleware

participant Token as Token Service

participant UserS as User Service

participant DB as Database

Note over C,DB: Fluxo de Autenticação JWT

C->>API: Request + Bearer Token

API->>Auth: get_current_user()

Auth->>Token: verify_token(token)

Token-->>Auth: payload ou None

alt Token Válido

Auth->>Token: is_access_token(payload)

Token-->>Auth: true/false

alt É Access Token

Auth->>UserS: get_user_by_id(user_id)

UserS->>DB: SELECT * FROM users WHERE id = ?

DB-->>UserS: User data

UserS-->>Auth: User entity

Auth-->>API: User entity

API-->>C: 200 OK + Response

else Não é Access Token

Auth-->>API: 401 Unauthorized

API-->>C: 401 Unauthorized

end

else Token Inválido

Auth-->>API: 401 Unauthorized

API-->>C: 401 Unauthorized

end

```