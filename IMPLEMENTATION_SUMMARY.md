# Resumo da Implementação - eShow API

## Visão Geral
API RESTful desenvolvida em FastAPI seguindo a arquitetura hexagonal (Clean Architecture) para gerenciamento de artistas, espaços e eventos musicais.

## Arquitetura Implementada

### 1. Estrutura de Camadas
- **Domain Layer**: Entidades e interfaces de repositório
- **Application Layer**: Serviços de aplicação e schemas
- **Infrastructure Layer**: Implementações de repositório e modelos de banco
- **API Layer**: Endpoints e rotas

### 2. Padrões Utilizados
- **Repository Pattern**: Para abstração do acesso a dados
- **Dependency Injection**: Para injeção de dependências
- **DTO Pattern**: Schemas Pydantic para transferência de dados
- **JWT Authentication**: Autenticação baseada em tokens

## Funcionalidades Implementadas

### 1. Autenticação e Autorização
- ✅ Registro de usuários
- ✅ Login com JWT
- ✅ Logout com blacklist de tokens
- ✅ Renovação de tokens
- ✅ Proteção de endpoints

### 2. Gerenciamento de Usuários
- ✅ CRUD completo de usuários
- ✅ Validação de dados
- ✅ Ativação/desativação de usuários

### 3. Gerenciamento de Roles
- ✅ CRUD completo de roles
- ✅ Roles predefinidos: ADMIN, ARTISTA, ESPACO
- ✅ Validação de tipos de role

### 4. Gerenciamento de Profiles
- ✅ CRUD completo de profiles
- ✅ Relacionamento com usuários e roles
- ✅ Validação de dados de endereço
- ✅ Busca por role

### 5. Gerenciamento de Artist Types
- ✅ CRUD completo de tipos de artistas
- ✅ Tipos predefinidos: Cantor(a) solo, Dupla, Trio, Banda, Grupo
- ✅ Validação de tipos

### 6. Gerenciamento de Musical Styles
- ✅ CRUD completo de estilos musicais
- ✅ Estilos flexíveis (qualquer string)
- ✅ Validação de unicidade

### 7. Gerenciamento de Artists
- ✅ CRUD completo de artistas
- ✅ Relacionamento com profiles e artist types
- ✅ Validação de dados de apresentação
- ✅ Redes sociais opcionais
- ✅ Busca por tipo de artista
- ✅ Busca por profile

### 8. Relacionamento N:N Artists-Musical Styles
- ✅ Tabela de relacionamento N:N
- ✅ CRUD completo de relacionamentos
- ✅ Criação individual e em lote
- ✅ Busca por artista ou estilo musical
- ✅ Atualização em lote (substituição)
- ✅ Deleção individual e em lote
- ✅ Integração com endpoints de artists

## Estrutura do Banco de Dados

### Tabelas Principais
1. **users**: Usuários do sistema
2. **roles**: Tipos de perfil (ADMIN, ARTISTA, ESPACO)
3. **profiles**: Perfis detalhados dos usuários
4. **artist_types**: Tipos de artistas
5. **musical_styles**: Estilos musicais
6. **artists**: Artistas com dados de apresentação
7. **artist_musical_style**: Relacionamento N:N entre artistas e estilos

### Relacionamentos
- **users** ↔ **profiles**: 1:1
- **roles** ↔ **profiles**: 1:N
- **profiles** ↔ **artists**: 1:1
- **artist_types** ↔ **artists**: 1:N
- **artists** ↔ **musical_styles**: N:N (via artist_musical_style)

## Endpoints Disponíveis

### Autenticação
- `POST /api/auth/register` - Registro
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Renovar token

### Usuários (Protegidos)
- `GET /api/users/me` - Perfil atual
- `GET /api/users/{id}` - Usuário por ID
- `GET /api/users/` - Listar usuários
- `PUT /api/users/{id}` - Atualizar usuário
- `DELETE /api/users/{id}` - Deletar usuário

### Roles (Protegidos)
- `GET /api/v1/roles/` - Listar roles
- `GET /api/v1/roles/{id}` - Role por ID
- `POST /api/v1/roles/` - Criar role
- `PUT /api/v1/roles/{id}` - Atualizar role
- `DELETE /api/v1/roles/{id}` - Deletar role

### Profiles (Protegidos)
- `GET /api/v1/profiles/` - Listar profiles
- `GET /api/v1/profiles/{id}` - Profile por ID
- `GET /api/v1/profiles/role/{role_id}` - Profiles por role
- `POST /api/v1/profiles/` - Criar profile
- `PUT /api/v1/profiles/{id}` - Atualizar profile
- `DELETE /api/v1/profiles/{id}` - Deletar profile

### Artist Types (Protegidos)
- `GET /api/v1/artist-types/` - Listar tipos
- `GET /api/v1/artist-types/{id}` - Tipo por ID
- `POST /api/v1/artist-types/` - Criar tipo
- `PUT /api/v1/artist-types/{id}` - Atualizar tipo
- `DELETE /api/v1/artist-types/{id}` - Deletar tipo

### Musical Styles (Protegidos)
- `GET /api/v1/musical-styles/` - Listar estilos
- `GET /api/v1/musical-styles/{id}` - Estilo por ID
- `POST /api/v1/musical-styles/` - Criar estilo
- `PUT /api/v1/musical-styles/{id}` - Atualizar estilo
- `DELETE /api/v1/musical-styles/{id}` - Deletar estilo

### Artists (Protegidos)
- `GET /api/v1/artists/` - Listar artistas
- `GET /api/v1/artists/{id}` - Artista por ID
- `GET /api/v1/artists/profile/{profile_id}` - Artista por profile
- `GET /api/v1/artists/type/{artist_type_id}` - Artistas por tipo
- `POST /api/v1/artists/` - Criar artista
- `PUT /api/v1/artists/{id}` - Atualizar artista
- `DELETE /api/v1/artists/{id}` - Deletar artista

### Artist-Musical Styles (Protegidos)
- `POST /api/v1/artist-musical-styles/` - Criar relacionamento individual
- `POST /api/v1/artist-musical-styles/bulk` - Criar relacionamentos em lote
- `GET /api/v1/artist-musical-styles/artist/{artist_id}` - Estilos de um artista
- `GET /api/v1/artist-musical-styles/musical-style/{musical_style_id}` - Artistas de um estilo
- `GET /api/v1/artist-musical-styles/{artist_id}/{musical_style_id}` - Relacionamento específico
- `PUT /api/v1/artist-musical-styles/artist/{artist_id}` - Atualizar estilos de artista
- `DELETE /api/v1/artist-musical-styles/{artist_id}/{musical_style_id}` - Deletar relacionamento
- `DELETE /api/v1/artist-musical-styles/artist/{artist_id}` - Deletar todos os relacionamentos de artista
- `DELETE /api/v1/artist-musical-styles/musical-style/{musical_style_id}` - Deletar todos os relacionamentos de estilo

### Públicos
- `GET /health` - Health check

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web
- **SQLAlchemy**: ORM
- **Alembic**: Migrações de banco
- **Pydantic**: Validação de dados
- **JWT**: Autenticação
- **SQLite**: Banco de dados (desenvolvimento)

### Estrutura
- **Python 3.12+**
- **Arquitetura Hexagonal**
- **Repository Pattern**
- **Dependency Injection**

## Scripts de Inicialização

### Dados Iniciais
- `init_roles.py` - Roles padrão
- `init_users.py` - Usuário admin
- `init_profiles.py` - Profiles de exemplo
- `init_artist_types.py` - Tipos de artistas
- `init_musical_styles.py` - Estilos musicais
- `init_artists.py` - Artistas de exemplo
- `init_artist_musical_styles.py` - Relacionamentos de exemplo

### Testes
- `test_api_complete.py` - Testes completos da API
- `test_relationships.py` - Testes de relacionamentos
- `test_artist_musical_styles.py` - Testes específicos do relacionamento N:N

## Como Executar

### 1. Configuração Inicial
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações

# Executar migrações
alembic upgrade head
```

### 2. Popular Dados Iniciais
```bash
# Executar scripts de inicialização
python init_roles.py
python init_users.py
python init_profiles.py
python init_artist_types.py
python init_musical_styles.py
python init_artists.py
python init_artist_musical_styles.py
```

### 3. Executar Aplicação
```bash
# Desenvolvimento
uvicorn app.main:app --reload

# Produção
python run.py
```

### 4. Testar API
```bash
# Testes completos
python test_api_complete.py

# Testes de relacionamentos
python test_relationships.py

# Testes específicos do relacionamento N:N
python test_artist_musical_styles.py
```

## Documentação

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **API Usage**: `API_USAGE.md` - Guia detalhado de uso
- **Architecture**: `ARCHITECTURE.md` - Documentação da arquitetura

## Status da Implementação

### ✅ Concluído
- [x] Autenticação e autorização
- [x] Gerenciamento de usuários
- [x] Gerenciamento de roles
- [x] Gerenciamento de profiles
- [x] Gerenciamento de artist types
- [x] Gerenciamento de musical styles
- [x] Gerenciamento de artists
- [x] Relacionamento N:N Artists-Musical Styles
- [x] Validações e tratamento de erros
- [x] Documentação da API
- [x] Scripts de inicialização
- [x] Testes automatizados

### 🔄 Próximos Passos
- [ ] Gerenciamento de espaços
- [ ] Gerenciamento de eventos
- [ ] Sistema de agendamento
- [ ] Notificações
- [ ] Upload de arquivos
- [ ] Cache Redis
- [ ] Logs estruturados
- [ ] Métricas e monitoramento

## Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente seguindo os padrões estabelecidos
4. Adicione testes
5. Atualize a documentação
6. Submeta um pull request

## Licença

© 2025 eShow. Todos os direitos reservados. 