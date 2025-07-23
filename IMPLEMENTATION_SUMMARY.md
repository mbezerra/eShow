# Resumo da Implementação - eShow API

## 🚀 Versão Atual: 0.10.0

### ✨ Funcionalidades Implementadas na v0.10.0

#### **Relacionamentos N:N Implementados:**

- **Space-Event Types**: Sistema completo de associação entre espaços e tipos de eventos
  - 10 endpoints REST funcionais
  - Sistema de banners para eventos
  - Operações CRUD e em lote
  - Filtros avançados por espaço, tipo de evento ou combinação
  - Migração de banco de dados aplicada
  - Dados de exemplo populados

- **Space-Festival Types**: Sistema completo de associação entre espaços e tipos de festivais
  - 10 endpoints REST funcionais
  - Sistema de banners para festivais
  - Operações CRUD e em lote
  - Filtros avançados por espaço, tipo de festival ou combinação
  - Migração de banco de dados aplicada
  - Dados de exemplo populados

- **Sistema de Bookings (Agendamentos)**: Sistema completo de agendamentos/reservas
  - 4 tipos de agendamentos: Espaço, Artista, Evento e Festival
  - 11 endpoints REST funcionais
  - Validações robustas e regras de negócio
  - Filtros especializados (profile, space, artist, event, festival, date-range)
  - Autenticação JWT obrigatória
  - Migração de banco de dados aplicada
  - 10 agendamentos de exemplo populados
  - Testado completamente via API (18 testes realizados)

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

### 8.1. Sistema de Controle de Acesso por Roles ✨
- ✅ **Validação de roles nos serviços**
  - Artists: Apenas profiles com role "ARTISTA" (`role_id = 2`)
  - Spaces: Apenas profiles com role "ESPACO" (`role_id = 3`)
- ✅ **Validação na criação e atualização**
  - Verificação automática do role do profile
  - Mensagens de erro claras e específicas
- ✅ **Integração com ProfileRepository**
  - Dependência injetada nos serviços
  - Validação em tempo real
- ✅ **Dados de exemplo reestruturados**
  - Profiles criados com roles adequados
  - Artists e Spaces apenas com profiles válidos

### 9. Gerenciamento de Space Types
- ✅ CRUD completo de tipos de espaço
- ✅ 15 tipos pré-cadastrados (Bar, Restaurante, Clube, etc.)
- ✅ Validação de unicidade de tipos
- ✅ Flexibilidade para adicionar novos tipos
- ✅ Padrão consistente com outros endpoints
- ✅ Script de inicialização automática

### 10. Gerenciamento de Event Types
- ✅ CRUD completo de tipos de evento
- ✅ 7 tipos pré-cadastrados (Aniversário, Casamento, Formatura, etc.)
- ✅ Validação de unicidade de tipos
- ✅ Flexibilidade para adicionar novos tipos
- ✅ Padrão consistente com outros endpoints
- ✅ Script de inicialização automática

### 11. Gerenciamento de Festival Types
- ✅ CRUD completo de tipos de festival
- ✅ 14 tipos pré-cadastrados (Aniversário de Emancipação Política, Festa Religiosa, etc.)
- ✅ Validação de unicidade de tipos
- ✅ Flexibilidade para adicionar novos tipos
- ✅ Padrão consistente com outros endpoints
- ✅ Script de inicialização automática

## Estrutura do Banco de Dados

### Tabelas Principais
1. **users**: Usuários do sistema
2. **roles**: Tipos de perfil (ADMIN, ARTISTA, ESPACO)
3. **profiles**: Perfis detalhados dos usuários
4. **artist_types**: Tipos de artistas
5. **musical_styles**: Estilos musicais
6. **artists**: Artistas com dados de apresentação
7. **artist_musical_style**: Relacionamento N:N entre artistas e estilos
8. **space_types**: Tipos de espaço (Bar, Restaurante, Clube, etc.)
9. **event_types**: Tipos de evento (Aniversário, Casamento, Formatura, etc.)
10. **festival_types**: Tipos de festival (Aniversário de Emancipação Política, Festa Religiosa, etc.)
11. **spaces**: Espaços para apresentações com relacionamentos para profiles, space_types, event_types e festival_types
12. **space_event_types**: Relacionamento N:N entre espaços e tipos de evento com dados específicos

### Relacionamentos
- **users** ↔ **profiles**: 1:1
- **roles** ↔ **profiles**: 1:N
- **profiles** ↔ **artists**: 1:1
- **profiles** ↔ **spaces**: 1:N
- **artist_types** ↔ **artists**: 1:N
- **space_types** ↔ **spaces**: 1:N
- **event_types** ↔ **spaces**: 1:N (opcional)
- **festival_types** ↔ **spaces**: 1:N (opcional)
- **artists** ↔ **musical_styles**: N:N (via artist_musical_style)
- **spaces** ↔ **event_types**: N:N (via space_event_types)
- **spaces** ↔ **festival_types**: N:N (via space_festival_types)

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

### Space Types (Protegidos)
- `GET /api/v1/space-types/` - Listar tipos de espaço
- `GET /api/v1/space-types/{id}` - Tipo de espaço por ID
- `POST /api/v1/space-types/` - Criar tipo de espaço
- `PUT /api/v1/space-types/{id}` - Atualizar tipo de espaço
- `DELETE /api/v1/space-types/{id}` - Deletar tipo de espaço

### Event Types (Protegidos)
- `GET /api/v1/event-types/` - Listar tipos de evento
- `GET /api/v1/event-types/{id}` - Tipo de evento por ID
- `POST /api/v1/event-types/` - Criar tipo de evento
- `PUT /api/v1/event-types/{id}` - Atualizar tipo de evento
- `DELETE /api/v1/event-types/{id}` - Deletar tipo de evento

### Festival Types (Protegidos)
- `GET /api/v1/festival-types/` - Listar tipos de festival
- `GET /api/v1/festival-types/{id}` - Tipo de festival por ID
- `POST /api/v1/festival-types/` - Criar tipo de festival
- `PUT /api/v1/festival-types/{id}` - Atualizar tipo de festival
- `DELETE /api/v1/festival-types/{id}` - Deletar tipo de festival

### Spaces (Protegidos)
- `GET /api/v1/spaces/` - Listar espaços
- `GET /api/v1/spaces/{id}` - Espaço por ID
- `GET /api/v1/spaces/profile/{profile_id}` - Espaços por profile
- `GET /api/v1/spaces/space-type/{space_type_id}` - Espaços por tipo de espaço
- `GET /api/v1/spaces/event-type/{event_type_id}` - Espaços por tipo de evento
- `GET /api/v1/spaces/festival-type/{festival_type_id}` - Espaços por tipo de festival
- `POST /api/v1/spaces/` - Criar espaço
- `PUT /api/v1/spaces/{id}` - Atualizar espaço
- `DELETE /api/v1/spaces/{id}` - Deletar espaço

### Space-Event Types (Protegidos)
- `GET /api/v1/space-event-types/` - Listar relacionamentos
- `GET /api/v1/space-event-types/{id}` - Relacionamento por ID
- `GET /api/v1/space-event-types/space/{space_id}` - Eventos de um espaço
- `GET /api/v1/space-event-types/event-type/{event_type_id}` - Espaços de um tipo de evento
- `GET /api/v1/space-event-types/space/{space_id}/event-type/{event_type_id}` - Relacionamentos específicos
- `POST /api/v1/space-event-types/` - Criar relacionamento
- `PUT /api/v1/space-event-types/{id}` - Atualizar relacionamento
- `DELETE /api/v1/space-event-types/{id}` - Deletar relacionamento
- `DELETE /api/v1/space-event-types/space/{space_id}` - Deletar todos de um espaço
- `DELETE /api/v1/space-event-types/event-type/{event_type_id}` - Deletar todos de um tipo

**Parâmetro `include_relations`**: Disponível nos endpoints GET de Artists e Spaces para incluir dados relacionados.

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
- `init_space_types.py` - Tipos de espaço (15 tipos pré-cadastrados)
- `init_event_types.py` - Tipos de evento (7 tipos pré-cadastrados)
- `init_festival_types.py` - Tipos de festival (14 tipos pré-cadastrados)
- `start_server.sh` - Script de inicialização automática do servidor

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
- [x] **Gerenciamento de espaços** ✨
- [x] **Sistema de controle de acesso por roles** ✨
- [x] **Validação de roles para Artists e Spaces** ✨
- [x] **Relacionamento N:N Space-Event Types** ✨
- [x] **Relacionamento N:N Space-Festival Types** ✨ **[v0.9.0]**
- [x] **Sistema de Bookings Completo** ✨ **[v0.10.0]**
- [x] Validações e tratamento de erros
- [x] Documentação da API
- [x] Scripts de inicialização
- [x] Testes automatizados

### 🔄 Próximos Passos
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