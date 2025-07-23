# eShow API

Sistema de gerenciamento para artistas e espaços de entretenimento, desenvolvido com **FastAPI** e arquitetura hexagonal.

## 🎯 **Funcionalidades Principais**

- **Gestão de Usuários** com autenticação JWT
- **Sistema de Perfis** (Artists e Spaces)
- **Gerenciamento de Artistas** e estilos musicais
- **Administração de Espaços** e tipos de evento
- **Sistema de Agendamentos/Reservas** (Bookings)
- **Sistema de Avaliações/Reviews** com notas de 1 a 5 estrelas
- **Relacionamentos N:N** entre entidades
- **API REST** completa com documentação automática
- **Arquitetura Hexagonal** para facilitar manutenção

## 📊 **Estatísticas do Projeto**

- **Total de Endpoints:** 106 (+11 endpoints Reviews)
- **Entidades de Domínio:** 15 (incluindo Review)
- **Relacionamentos N:N:** 3
- **Tabelas no Banco:** 15 (incluindo reviews)
- **Schemas Pydantic:** 55+ (incluindo schemas de Reviews)
- **Cobertura de Testes:** Em desenvolvimento

## 📁 **Estrutura do Projeto**

```
eShow/
├── app/                   # Camada de aplicação
│   ├── api/              # Endpoints da API
│   ├── core/             # Configurações e autenticação
│   ├── schemas/          # Modelos Pydantic
│   └── application/      # Serviços e casos de uso
├── domain/               # Camada de domínio
│   ├── entities/         # Entidades de negócio
│   └── repositories/     # Interfaces dos repositórios
├── infrastructure/       # Camada de infraestrutura
│   ├── database/         # Modelos e configuração do banco
│   ├── repositories/     # Implementação dos repositórios
│   └── external/          # Serviços externos
├── tests/                 # Testes unitários e de integração
└── alembic/               # Migrações do banco de dados
```

## Princípios da Arquitetura Hexagonal

1. **Domínio (Core)**: Contém as regras de negócio e entidades
2. **Aplicação**: Contém os casos de uso e adaptadores de entrada
3. **Infraestrutura**: Contém adaptadores de saída (banco de dados, APIs externas)

## Como Executar

### Versionamento Automático
O projeto utiliza versionamento automático baseado em tags Git. Veja [VERSIONING.md](VERSIONING.md) para detalhes.

```bash
# Verificar versão atual
python version.py show

# Criar nova versão
python version.py patch  # ou minor/major
```

### Desenvolvimento (SQLite)

**Opção 1: Usando script de inicialização (Recomendado)**
```bash
# Executar script que ativa ambiente virtual automaticamente
./start_server.sh
```

**Opção 2: Configuração manual**
1. Criar e ativar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp env.example .env
# Editar o arquivo .env e configurar SECRET_KEY
```

4. Inicializar banco de dados:
```bash
python init_db.py
```

5. Iniciar o servidor:
```bash
python run.py
```

### Produção (PostgreSQL)

1. Instalar PostgreSQL e criar banco:
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Criar banco e usuário
sudo -u postgres psql
CREATE DATABASE eshow;
CREATE USER eshow_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE eshow TO eshow_user;
\q
```

2. Configurar DATABASE_URL no .env:
```bash
DATABASE_URL=postgresql://eshow_user:your_password@localhost/eshow
```

3. Migrar dados do SQLite para PostgreSQL:
```bash
python migrate_to_postgres.py
```

4. Executar migrações:
```bash
alembic upgrade head
```

## Sistema de Roles

O sistema implementa controle de acesso baseado em roles para garantir que apenas usuários adequados possam cadastrar determinados tipos de entidades:

### Roles Disponíveis
- **ADMIN** (`role_id = 1`): Administradores do sistema
- **ARTISTA** (`role_id = 2`): Artistas e músicos
- **ESPACO** (`role_id = 3`): Estabelecimentos e espaços de eventos

### Restrições por Role
- **Artists**: Apenas profiles com role "ARTISTA" podem cadastrar artistas
- **Spaces**: Apenas profiles com role "ESPACO" podem cadastrar espaços
- **Profiles**: Cada usuário deve ter um profile associado a um role específico

## Endpoints

### Autenticação (`/api/v1/auth/`)
- `POST /register` - Registrar novo usuário
- `POST /login` - Fazer login
- `POST /refresh` - Renovar token de acesso

### Usuários (`/api/v1/users/`) - Requer autenticação
- `GET /me` - Obter informações do usuário atual
- `POST /` - Criar usuário
- `GET /` - Listar usuários
- `GET /{user_id}` - Obter usuário por ID
- `PUT /{user_id}` - Atualizar usuário
- `DELETE /{user_id}` - Deletar usuário

### Artists (`/api/v1/artists/`) - Requer autenticação
- `POST /` - Criar novo artista ⚠️ **Apenas profiles com role "ARTISTA"**
- `GET /` - Listar todos os artistas
- `GET /{artist_id}` - Obter artista por ID
- `GET /profile/{profile_id}` - Obter artista por profile ID
- `GET /type/{artist_type_id}` - Listar artistas por tipo
- `PUT /{artist_id}` - Atualizar artista ⚠️ **Validação de role ao alterar profile_id**
- `DELETE /{artist_id}` - Deletar artista

**Parâmetro `include_relations`**: Use `?include_relations=true` nos endpoints GET para incluir dados relacionados (profile e artist_type).

**⚠️ RESTRIÇÃO IMPORTANTE**: Apenas profiles com `role_id = 2` (role "ARTISTA") podem cadastrar artistas.

### Spaces (`/api/v1/spaces/`) - Requer autenticação
- `POST /` - Criar novo espaço ⚠️ **Apenas profiles com role "ESPACO"**
- `GET /` - Listar todos os espaços
- `GET /{space_id}` - Obter espaço por ID
- `GET /profile/{profile_id}` - Obter espaços por profile ID
- `GET /space-type/{space_type_id}` - Listar espaços por tipo de espaço
- `GET /event-type/{event_type_id}` - Listar espaços por tipo de evento
- `GET /festival-type/{festival_type_id}` - Listar espaços por tipo de festival
- `PUT /{space_id}` - Atualizar espaço ⚠️ **Validação de role ao alterar profile_id**
- `DELETE /{space_id}` - Deletar espaço

**Parâmetro `include_relations`**: Use `?include_relations=true` nos endpoints GET para incluir dados relacionados (profile, space_type, event_type, festival_type).

**⚠️ RESTRIÇÃO IMPORTANTE**: Apenas profiles com `role_id = 3` (role "ESPACO") podem cadastrar espaços.

### Space-Event Types (`/api/v1/space-event-types/`) - Requer autenticação
- `POST /` - Criar novo relacionamento entre espaço e tipo de evento
- `GET /` - Listar todos os relacionamentos
- `GET /{space_event_type_id}` - Obter relacionamento por ID
- `GET /space/{space_id}` - Obter todos os eventos de um espaço
- `GET /event-type/{event_type_id}` - Obter todos os espaços de um tipo de evento
- `GET /space/{space_id}/event-type/{event_type_id}` - Obter relacionamentos específicos
- `PUT /{space_event_type_id}` - Atualizar relacionamento
- `DELETE /{space_event_type_id}` - Deletar relacionamento específico
- `DELETE /space/{space_id}` - Deletar todos os relacionamentos de um espaço
- `DELETE /event-type/{event_type_id}` - Deletar todos os relacionamentos de um tipo de evento

### Space-Festival Types (`/api/v1/space-festival-types/`) - Requer autenticação
- `POST /` - Criar novo relacionamento entre espaço e tipo de festival
- `GET /` - Listar todos os relacionamentos
- `GET /{space_festival_type_id}` - Obter relacionamento por ID
- `GET /space/{space_id}` - Obter todos os festivais de um espaço
- `GET /festival-type/{festival_type_id}` - Obter todos os espaços de um tipo de festival
- `GET /space/{space_id}/festival-type/{festival_type_id}` - Obter relacionamentos específicos
- `PUT /{space_festival_type_id}` - Atualizar relacionamento
- `DELETE /{space_festival_type_id}` - Deletar relacionamento específico
- `DELETE /space/{space_id}` - Deletar todos os relacionamentos de um espaço
- `DELETE /festival-type/{festival_type_id}` - Deletar todos os relacionamentos de um tipo de festival

### Reviews (`/api/v1/reviews/`) - Requer autenticação
- `POST /` - Criar nova avaliação/review
- `GET /` - Listar todas as avaliações
- `GET /{review_id}` - Obter avaliação por ID
- `PUT /{review_id}` - Atualizar avaliação
- `DELETE /{review_id}` - Deletar avaliação
- `GET /profile/{profile_id}` - Obter avaliações de um profile específico
- `GET /profile/{profile_id}/average` - Obter média de avaliações de um profile
- `GET /space-event-type/{space_event_type_id}` - Avaliações por tipo de evento
- `GET /space-festival-type/{space_festival_type_id}` - Avaliações por tipo de festival
- `GET /rating/{nota}` - Filtrar avaliações por nota (1-5 estrelas)
- `GET /date-range/` - Filtrar avaliações por período (query params: data_inicio, data_fim)

**Parâmetro `include_relations`**: Use `?include_relations=true` nos endpoints GET para incluir dados relacionados (profile, space_event_type, space_festival_type).

**⚠️ REGRAS DE NEGÓCIO**:
- Notas devem ser entre 1 e 5 (números inteiros)
- Depoimento deve ter no mínimo 10 caracteres e máximo 1000
- Cada review deve estar associado a UM space_event_type_id OU UM space_festival_type_id (não ambos)
- Profile_id não pode ser alterado após criação do review

A API estará disponível em `http://localhost:8000`
A documentação automática estará em `http://localhost:8000/docs` 