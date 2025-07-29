### **Arquitetura Implementada**

O endpoint auth implementa uma **arquitetura de autenticação robusta** seguindo os princípios da **Clean Architecture** com foco especial em segurança:

1. **Camada de Apresentação**: FastAPI com endpoints de autenticação, validação Pydantic e middleware de segurança
2. **Camada de Aplicação**: AuthService que orquestra toda a lógica de autenticação e UserService para operações de usuário
3. **Camada de Domínio**: Entidades de usuário e regras de negócio de autenticação
4. **Camada de Infraestrutura**: Implementações de persistência e sistema de blacklist de tokens

### **Características Principais**

- **Sistema JWT Completo**: Access tokens e refresh tokens com expiração configurável
- **Hash de Senhas Seguro**: Uso do bcrypt para criptografia de senhas
- **Blacklist de Tokens**: Sistema para invalidar tokens durante logout
- **Validação Robusta**: Schemas Pydantic para validação de entrada
- **Tratamento de Erros**: HTTP exceptions apropriadas para diferentes cenários de autenticação
- **Login Automático**: Após registro, o usuário é automaticamente autenticado

### **Endpoints Disponíveis**

1. **POST /auth/register** - Registrar novo usuário e fazer login automático
2. **POST /auth/login** - Fazer login com email e senha
3. **POST /auth/logout** - Fazer logout (invalidar token)
4. **POST /auth/refresh** - Renovar token de acesso usando refresh token

### **Segurança Implementada**

- **Tokens JWT**: Access tokens (30 min) e refresh tokens (7 dias) por padrão
- **Hash de Senhas**: Bcrypt com salt automático
- **Blacklist**: Sistema para invalidar tokens durante logout
- **Validação de Token**: Verificação de validade, expiração e tipo
- **Configuração Flexível**: Tempos de expiração configuráveis via variáveis de ambiente

### **Fluxo de Autenticação**

1. **Registro**: Cria usuário com senha hasheada e retorna tokens
2. **Login**: Valida credenciais e retorna tokens de acesso
3. **Refresh**: Renova tokens usando refresh token válido
4. **Logout**: Adiciona token à blacklist para invalidação

### **Configurações de Segurança**

- **SECRET_KEY**: Chave secreta para assinatura de tokens
- **ALGORITHM**: HS256 para assinatura JWT
- **ACCESS_TOKEN_EXPIRE_MINUTES**: 30 minutos (padrão)
- **REFRESH_TOKEN_EXPIRE_DAYS**: 7 dias (padrão)

# Diagrama de Fluxo - Endpoint Auth

## Fluxo Detalhado da Arquitetura em Camadas

  

```mermaid

graph TB

%% Cliente

Client[Cliente/Postman]

%% Camada de Apresentação

subgraph "Camada de Apresentação (API)"

AuthRouter[FastAPI Auth Router]

AuthEndpoints[Auth Endpoints]

AuthSchemas[Auth Schemas]

SecurityUtils[Security Utils]

end

%% Camada de Aplicação

subgraph "Camada de Aplicação (Services)"

AuthService[AuthService]

UserService[UserService]

AuthDependencies[Auth Dependencies]

end

%% Camada de Domínio

subgraph "Camada de Domínio (Domain)"

UserEntity[User Entity]

UserRepoInterface[UserRepository Interface]

AuthRules[Regras de Autenticação]

end

%% Camada de Infraestrutura

subgraph "Camada de Infraestrutura (Infrastructure)"

UserRepoImpl[UserRepositoryImpl]

UserModel[UserModel SQLAlchemy]

Database[(PostgreSQL Database)]

TokenBlacklist[Token Blacklist]

end

%% Fluxo de Dados

Client --> AuthRouter

AuthRouter --> AuthEndpoints

AuthEndpoints --> AuthSchemas

AuthEndpoints --> SecurityUtils

AuthSchemas --> AuthDependencies

AuthDependencies --> AuthService

AuthDependencies --> UserService

AuthService --> UserService

UserService --> UserRepoInterface

UserRepoInterface --> UserRepoImpl

UserRepoImpl --> UserModel

UserModel --> Database

%% Segurança

SecurityUtils --> AuthService

AuthService --> TokenBlacklist

%% Entidades

UserService --> UserEntity

UserRepoImpl --> UserEntity

UserModel --> UserEntity

%% Estilos

classDef apiLayer fill:#e1f5fe

classDef appLayer fill:#f3e5f5

classDef domainLayer fill:#e8f5e8

classDef infraLayer fill:#fff3e0

classDef securityLayer fill:#ffebee

class AuthRouter,AuthEndpoints,AuthSchemas apiLayer

class AuthService,UserService,AuthDependencies appLayer

class UserEntity,UserRepoInterface,AuthRules domainLayer

class UserRepoImpl,UserModel,Database infraLayer

class SecurityUtils,TokenBlacklist securityLayer

```

  

## Fluxo Detalhado por Operação

  

```mermaid

sequenceDiagram

participant C as Cliente

participant API as Auth API

participant AuthS as Auth Service

participant UserS as User Service

participant Security as Security Utils

participant Repo as Repository

participant DB as Database

participant Blacklist as Token Blacklist

%% Registro de Usuário

Note over C,Blacklist: POST /auth/register - Registrar Usuário

C->>API: POST /auth/register {name, email, password}

API->>API: Validar UserRegister schema

API->>AuthS: register_user(user_data)

AuthS->>AuthS: Verificar email duplicado

AuthS->>Security: get_password_hash(password)

Security-->>AuthS: hashed_password

AuthS->>UserS: create_user(user_create)

UserS->>Repo: create(user)

Repo->>DB: INSERT INTO users

DB-->>Repo: UserModel

Repo-->>UserS: User entity

UserS-->>AuthS: UserResponse

%% Login Automático após Registro

AuthS->>AuthS: login_user(login_data)

AuthS->>UserS: get_user_by_email_for_auth(email)

UserS->>Repo: get_by_email(email)

Repo->>DB: SELECT * FROM users WHERE email = ?

DB-->>Repo: UserModel

Repo-->>UserS: User entity

AuthS->>Security: verify_password(password, hashed_password)

Security-->>AuthS: true/false

alt Senha Correta

AuthS->>Security: create_access_token(data)

Security-->>AuthS: access_token

AuthS->>Security: create_refresh_token(data)

Security-->>AuthS: refresh_token

AuthS-->>API: Token {access_token, refresh_token}

API-->>C: 201 Created + Token

else Senha Incorreta

AuthS-->>API: ValueError

API-->>C: 400 Bad Request

end

%% Login de Usuário

Note over C,Blacklist: POST /auth/login - Login

C->>API: POST /auth/login {email, password}

API->>API: Validar UserLogin schema

API->>AuthS: login_user(user_data)

AuthS->>UserS: get_user_by_email_for_auth(email)

UserS->>Repo: get_by_email(email)

Repo->>DB: SELECT * FROM users WHERE email = ?

DB-->>Repo: UserModel

Repo-->>UserS: User entity

AuthS->>Security: verify_password(password, hashed_password)

Security-->>AuthS: true/false

alt Autenticação Válida

AuthS->>Security: create_access_token(data)

Security-->>AuthS: access_token

AuthS->>Security: create_refresh_token(data)

Security-->>AuthS: refresh_token

AuthS-->>API: Token {access_token, refresh_token}

API-->>C: 200 OK + Token

else Autenticação Inválida

AuthS-->>API: ValueError

API-->>C: 401 Unauthorized

end

%% Refresh Token

Note over C,Blacklist: POST /auth/refresh - Renovar Token

C->>API: POST /auth/refresh {refresh_token}

API->>API: Validar RefreshToken schema

API->>AuthS: refresh_access_token(refresh_token)

AuthS->>Blacklist: is_token_blacklisted(token)

Blacklist-->>AuthS: true/false

alt Token não está na Blacklist

AuthS->>Security: verify_token(refresh_token)

Security-->>AuthS: payload ou None

alt Token Válido

AuthS->>Security: is_refresh_token(payload)

Security-->>AuthS: true/false

alt É Refresh Token

AuthS->>UserS: get_user_by_id(user_id)

UserS->>Repo: get_by_id(user_id)

Repo->>DB: SELECT * FROM users WHERE id = ?

DB-->>Repo: UserModel

Repo-->>UserS: User entity

AuthS->>Security: create_access_token(data)

Security-->>AuthS: new_access_token

AuthS->>Security: create_refresh_token(data)

Security-->>AuthS: new_refresh_token

AuthS-->>API: Token {new_access_token, new_refresh_token}

API-->>C: 200 OK + Token

else Não é Refresh Token

AuthS-->>API: ValueError

API-->>C: 401 Unauthorized

end

else Token Inválido

AuthS-->>API: ValueError

API-->>C: 401 Unauthorized

end

else Token na Blacklist

AuthS-->>API: ValueError

API-->>C: 401 Unauthorized

end

%% Logout

Note over C,Blacklist: POST /auth/logout - Logout

C->>API: POST /auth/logout + Bearer Token

API->>API: get_current_user() - Validar token

API->>AuthS: add_token_to_blacklist(token)

AuthS->>Blacklist: add(token)

Blacklist-->>AuthS: Confirmação

AuthS-->>API: Sucesso

API-->>C: 200 OK + {"message": "Logout realizado com sucesso"}

```

  

## Arquitetura de Segurança

  

```mermaid

graph TD

%% Componentes de Segurança

subgraph "Segurança JWT"

JWTConfig[JWT Configuration]

TokenUtils[Token Utils]

PasswordUtils[Password Utils]

end

subgraph "Autenticação"

AuthService[AuthService]

AuthMiddleware[Auth Middleware]

TokenBlacklist[Token Blacklist]

end

subgraph "Configuração"

Settings[Settings]

SecretKey[SECRET_KEY]

Algorithm[ALGORITHM]

TokenExpiry[Token Expiry]

end

%% Fluxo de Segurança

AuthService --> JWTConfig

AuthService --> TokenUtils

AuthService --> PasswordUtils

AuthService --> TokenBlacklist

AuthMiddleware --> TokenUtils

AuthMiddleware --> TokenBlacklist

JWTConfig --> Settings

TokenUtils --> SecretKey

TokenUtils --> Algorithm

TokenUtils --> TokenExpiry

PasswordUtils --> Settings

%% Estilos

classDef security fill:#ffebee

classDef auth fill:#e3f2fd

classDef config fill:#f1f8e9

class JWTConfig,TokenUtils,PasswordUtils security

class AuthService,AuthMiddleware,TokenBlacklist auth

class Settings,SecretKey,Algorithm,TokenExpiry config

```

  

## Fluxo de Criação e Validação de Tokens

  

```mermaid

sequenceDiagram

participant AuthS as Auth Service

participant Security as Security Utils

participant JWT as JWT Library

participant Config as Settings

Note over AuthS,Config: Criação de Access Token

AuthS->>Security: create_access_token(data)

Security->>Security: Preparar payload

Security->>Config: ACCESS_TOKEN_EXPIRE_DELTA

Config-->>Security: timedelta

Security->>Security: Adicionar exp e type

Security->>JWT: jwt.encode(payload, SECRET_KEY, ALGORITHM)

JWT-->>Security: encoded_token

Security-->>AuthS: access_token

Note over AuthS,Config: Criação de Refresh Token

AuthS->>Security: create_refresh_token(data)

Security->>Security: Preparar payload

Security->>Config: REFRESH_TOKEN_EXPIRE_DELTA

Config-->>Security: timedelta

Security->>Security: Adicionar exp e type

Security->>JWT: jwt.encode(payload, SECRET_KEY, ALGORITHM)

JWT-->>Security: encoded_token

Security-->>AuthS: refresh_token

Note over AuthS,Config: Validação de Token

AuthS->>Security: verify_token(token)

Security->>JWT: jwt.decode(token, SECRET_KEY, ALGORITHM)

alt Token Válido

JWT-->>Security: payload

Security->>Security: Verificar expiração

Security-->>AuthS: payload

else Token Inválido

JWT-->>Security: JWTError

Security-->>AuthS: None

end

Note over AuthS,Config: Verificação de Tipo de Token

AuthS->>Security: is_access_token(payload)

Security->>Security: Verificar type == "access"

Security-->>AuthS: true/false

AuthS->>Security: is_refresh_token(payload)

Security->>Security: Verificar type == "refresh"

Security-->>AuthS: true/false

```

  

## Fluxo de Hash e Verificação de Senhas

  

```mermaid

sequenceDiagram

participant AuthS as Auth Service

participant Security as Security Utils

participant Bcrypt as Bcrypt Library

Note over AuthS,Bcrypt: Hash de Senha (Registro)

AuthS->>Security: get_password_hash(plain_password)

Security->>Bcrypt: pwd_context.hash(password)

Bcrypt-->>Security: hashed_password

Security-->>AuthS: hashed_password

Note over AuthS,Bcrypt: Verificação de Senha (Login)

AuthS->>Security: verify_password(plain_password, hashed_password)

Security->>Bcrypt: pwd_context.verify(plain_password, hashed_password)

alt Senha Correta

Bcrypt-->>Security: true

Security-->>AuthS: true

else Senha Incorreta

Bcrypt-->>Security: false

Security-->>AuthS: false

end

```

  

## Estrutura de Tokens JWT

  

```mermaid

graph LR

subgraph "Access Token"

ATHeader[Header: alg=HS256, typ=JWT]

ATPayload[Payload: sub, exp, type=access]

ATSignature[Signature]

end

subgraph "Refresh Token"

RTHeader[Header: alg=HS256, typ=JWT]

RTPayload[Payload: sub, exp, type=refresh]

RTSignature[Signature]

end

ATHeader --> ATPayload

ATPayload --> ATSignature

RTHeader --> RTPayload

RTPayload --> RTSignature

%% Estilos

classDef token fill:#e8f5e8

classDef header fill:#e3f2fd

classDef payload fill:#fff3e0

classDef signature fill:#ffebee

class ATHeader,RTHeader header

class ATPayload,RTPayload payload

class ATSignature,RTSignature signature

```