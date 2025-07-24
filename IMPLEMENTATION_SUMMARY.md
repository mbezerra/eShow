# Resumo da Implementação - eShow API

## 🚀 Versão Atual: 0.13.6+

### ✨ Funcionalidades Implementadas na v0.12.0

#### **Sistema de Manifestações de Interesse (Interests) Completo:**

- **Interest**: Sistema completo de manifestações de interesse entre artistas e espaços
  - 15 endpoints REST funcionais com autenticação JWT
  - Gestão de manifestações de interesse bidirecionais (artista→espaço, espaço→artista)
  - Sistema de status com 3 estados: "AGUARDANDO_CONFIRMACAO", "ACEITO", "RECUSADO"
  - Validação de roles: apenas artistas podem manifestar interesse em espaços e vice-versa
  - Prevenção de duplicatas: não é possível manifestar interesse duplicado
  - Validações robustas: data futura, duração 0.5-8h, valores positivos, mensagem obrigatória
  - Endpoints especializados para aceitar/rejeitar manifestações
  - Consultas por profile (enviadas, recebidas, pendentes)
  - Estatísticas detalhadas por profile
  - Filtros avançados por status, tipo de evento e período
  - Relacionamentos com profiles, space_event_types e space_festival_types
  - Parâmetro `include_relations=true` para carregar dados relacionados
  - Migração de banco aplicada (tabela interests)
  - Dados de exemplo populados (17 manifestações com diferentes status)
  - **v0.13.4**: Correção do enum StatusInterest para compatibilidade com banco de dados
  - **v0.13.5**: Correção do método get_profile_by_user_id no ProfileService
  - **v0.13.6**: Correção do timeout do pool de conexões do banco de dados

### ✨ Funcionalidades Implementadas na v0.11.1

#### **Sistema Financeiro/Bancário Completo:**

- **Financial**: Sistema completo de dados financeiros/bancários com suporte a PIX
  - 13 endpoints REST funcionais com autenticação JWT
  - Gestão de dados bancários (código banco string 3 dígitos, agência, conta, tipo)
  - Sistema completo de chaves PIX com 5 tipos: CPF, CNPJ, Celular, E-mail, Aleatória
  - Validações robustas específicas por tipo de chave PIX
  - Código do banco como string 3 dígitos (001-999) seguindo padrão brasileiro
  - Garantia de unicidade de chaves PIX no sistema
  - Preferências de transferência (PIX/TED)
  - Relacionamento com profiles existentes
  - Estatísticas em tempo real por banco e tipo de chave PIX
  - Parâmetro `include_relations=true` para carregar dados relacionados
  - Endpoint de verificação de disponibilidade de chave PIX
  - Migração de banco aplicada (tabela financials com banco VARCHAR(3))
  - Dados de exemplo populados (6 registros com bancos "341", "237", "104", "001", "033", "260")

### ✨ Funcionalidades Implementadas na v0.10.3

#### **Sistema de Avaliações/Reviews Completo:**

- **Reviews**: Sistema completo de avaliações com notas de 1 a 5 estrelas
  - 11 endpoints REST funcionais
  - **Regras de negócio implementadas**: ADMIN não avalia, ARTISTA e ESPAÇO podem avaliar
  - **Profile_id determinado automaticamente** pelo usuário logado
  - Relacionamento com profiles, space_event_types e space_festival_types
  - Validações robustas (nota entre 1-5, depoimento mínimo 10 caracteres)
  - Cálculo de média de avaliações por profile
  - Filtros avançados por profile, nota, período, tipo de evento/festival
  - Parâmetro `include_relations=true` para carregar dados relacionados
  - Migração de banco de dados aplicada
  - **Dados de exemplo populados (12 reviews)** seguindo regras de negócio
- **Versão 0.13.1**: Correções no sistema de reviews implementadas
- **Versão 0.13.2**: Correção do parâmetro include_relations nos endpoints de reviews
- **Versão 0.13.3**: Padronização dos endpoints DELETE para retornar mensagens de sucesso
- **Versão 0.13.4**: Correção do enum StatusInterest para compatibilidade com banco de dados
- **Versão 0.13.5**: Correção do método get_profile_by_user_id no ProfileService
- **Versão 0.13.6**: Correção do timeout do pool de conexões do banco de dados

### ✨ Funcionalidades Implementadas na v0.10.0-0.10.2

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

### **📅 Sistema de Agendamentos (Bookings)**
- **4 tipos de agendamentos:** Espaço, Artista, Evento e Festival
- **Regras por role:** ADMIN não agenda, ARTISTA só agenda espaços/eventos/festivais, ESPAÇO só agenda artistas/eventos/festivais
- **Validações robustas:** Datas, horários e relacionamentos únicos
- **Filtros especializados:** Por profile, espaço, artista, evento, festival e período
- **CRUD completo:** Criar, ler, atualizar e deletar agendamentos
- **Autenticação obrigatória:** Todos endpoints protegidos por JWT

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

### 12. Sistema de Avaliações/Reviews ✨ **[v0.10.3]**
- ✅ **CRUD completo de reviews**
  - Criar, ler, atualizar e deletar avaliações
  - 11 endpoints REST funcionais
- ✅ **Sistema de notas de 1 a 5 estrelas**
  - Validação rigorosa de notas inteiras entre 1-5
  - Cálculo automático de média por profile
- ✅ **Validações robustas**
  - Depoimento mínimo 10 caracteres, máximo 1000
  - Relacionamento exclusivo: OU space_event_type OU space_festival_type
  - Profile_id imutável após criação
- ✅ **Filtros avançados**
  - Por profile avaliado
  - Por nota específica (1-5 estrelas)
  - Por período (data_inicio até data_fim)
  - Por tipo de evento ou festival
- ✅ **Relacionamentos incluídos**
  - Profile avaliado com dados completos
  - Space_event_type ou space_festival_type relacionados
  - Parâmetro `include_relations=true` disponível
- ✅ **Dados de exemplo**
  - 6 reviews iniciais com distribuição de notas
  - Relacionamentos com profiles, eventos e festivais existentes
- ✅ **Endpoint de estatísticas**
  - Média de avaliações por profile
  - Contagem total de reviews por profile

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
10. **festival_types**: Tipos de festival (Festa Religiosa, Festival de Música, etc.)
11. **spaces**: Espaços para apresentações com dados detalhados
12. **space_event_types**: Relacionamento N:N entre espaços e tipos de evento
13. **space_festival_types**: Relacionamento N:N entre espaços e tipos de festival
14. **bookings**: Agendamentos/reservas entre profiles
15. **reviews**: Avaliações/reviews com notas de 1-5 estrelas
16. **financials**: Dados financeiros/bancários com chaves PIX
17. **interests**: Manifestações de interesse entre artistas e espaços

### Relacionamentos
- **users** ↔ **profiles**: 1:1
- **roles** ↔ **profiles**: 1:N
- **profiles** ↔ **artists**: 1:1
- **profiles** ↔ **spaces**: 1:N
- **profiles** ↔ **reviews**: 1:N (profile avaliado)
- **profiles** ↔ **interests**: 1:N (profile interessado e profile interesse)
- **artist_types** ↔ **artists**: 1:N
- **space_types** ↔ **spaces**: 1:N
- **event_types** ↔ **spaces**: 1:N (opcional)
- **festival_types** ↔ **spaces**: 1:N (opcional)
- **artists** ↔ **musical_styles**: N:N (via artist_musical_style)
- **spaces** ↔ **event_types**: N:N (via space_event_types)
- **spaces** ↔ **festival_types**: N:N (via space_festival_types)
- **space_event_types** ↔ **reviews**: 1:N (opcional, mutuamente exclusivo)
- **space_festival_types** ↔ **reviews**: 1:N (opcional, mutuamente exclusivo)
- **space_event_types** ↔ **interests**: 1:N (opcional)
- **space_festival_types** ↔ **interests**: 1:N (opcional)
- **profiles** ↔ **financials**: 1:N

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

### Interests (Protegidos)
- `GET /api/v1/interests/` - Listar manifestações de interesse
- `GET /api/v1/interests/{id}` - Manifestação por ID
- `POST /api/v1/interests/` - Criar manifestação de interesse
- `PUT /api/v1/interests/{id}` - Atualizar manifestação completa
- `DELETE /api/v1/interests/{id}` - Deletar manifestação
- `PATCH /api/v1/interests/{id}/status` - Atualizar status da manifestação
- `PATCH /api/v1/interests/{id}/accept` - Aceitar manifestação de interesse
- `PATCH /api/v1/interests/{id}/reject` - Recusar manifestação de interesse
- `GET /api/v1/interests/profile/interessado/{profile_id}` - Manifestações enviadas por um profile
- `GET /api/v1/interests/profile/interesse/{profile_id}` - Manifestações recebidas por um profile
- `GET /api/v1/interests/profile/{profile_id}/pending` - Manifestações pendentes de um profile
- `GET /api/v1/interests/profile/{profile_id}/statistics` - Estatísticas de manifestações por profile
- `GET /api/v1/interests/status/{status}` - Filtrar manifestações por status
- `GET /api/v1/interests/space-event-type/{space_event_type_id}` - Manifestações por tipo de evento
- `GET /api/v1/interests/date-range/` - Filtrar manifestações por período

**Parâmetro `include_relations`**: Disponível nos endpoints GET para incluir dados relacionados (profile_interessado, profile_interesse, space_event_type, space_festival_type).

**⚠️ REGRAS DE NEGÓCIO**:
- Apenas **artistas** podem manifestar interesse em **espaços**
- Apenas **espaços** podem manifestar interesse em **artistas**
- **Prevenção de duplicatas**: Não é possível manifestar interesse duplicado
- **Estados de status**: "Aguardando Confirmação", "Aceito", "Recusado"
- **Validação de data**: Data inicial deve ser futura
- **Validação de duração**: Entre 0.5 e 8 horas
- **Validação de valores**: Valores devem ser positivos
- **Mensagem obrigatória**: Mínimo 10, máximo 1000 caracteres
- **Profile_id não pode ser alterado** após criação da manifestação

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
- `init_spaces.py` - Espaços de exemplo
- `init_space_event_types.py` - Relacionamentos espaço-evento
- `init_space_festival_types.py` - Relacionamentos espaço-festival
- `init_bookings.py` - Agendamentos de exemplo
- `init_reviews.py` - Avaliações de exemplo (6 reviews com notas variadas)
- `init_financials.py` - Dados financeiros de exemplo (6 registros com bancos reais)
- `init_interests.py` - Manifestações de interesse de exemplo (17 manifestações com diferentes status)
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
- [x] **Sistema de Bookings Completo** ✨ **[v0.10.0-0.10.2]**
- [x] **Sistema de Avaliações/Reviews** ✨ **[v0.10.3]**
- [x] **Sistema Financeiro/Bancário** ✨ **[v0.11.1]**
- [x] **Sistema de Manifestações de Interesse** ✨ **[v0.12.0]**
- [x] Validações e tratamento de erros
- [x] Documentação da API
- [x] Scripts de inicialização
- [x] Testes automatizados

### 🔄 Próximos Passos
- [ ] Gerenciamento de eventos
- [ ] Sistema de notificações
- [ ] Upload de arquivos e mídias
- [ ] Sistema de pagamentos
- [ ] Cache Redis
- [ ] Logs estruturados
- [ ] Métricas e monitoramento
- [ ] Sistema de relatórios

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