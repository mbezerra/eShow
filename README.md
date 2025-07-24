# eShow API

Sistema de gerenciamento para artistas e espaços de entretenimento, desenvolvido com **FastAPI** e arquitetura hexagonal.

## 🎯 **Funcionalidades Principais**

- **Gestão de Usuários** com autenticação JWT
- **Sistema de Perfis** (Artists e Spaces)
- **Gerenciamento de Artistas** e estilos musicais
- **Administração de Espaços** e tipos de evento
- **Sistema de Agendamentos/Reservas** (Bookings)
- **Sistema de Avaliações/Reviews** com notas de 1 a 5 estrelas
- **Sistema Financeiro/Bancário** com dados PIX e transferências
- **Sistema de Manifestações de Interesse** (Interests) entre artistas e espaços
- **Relacionamentos N:N** entre entidades
- **API REST** completa com documentação automática
- **Arquitetura Hexagonal** para facilitar manutenção

## 📊 **Estatísticas do Projeto**

- **Total de Endpoints:** 134 (+15 endpoints Interests)
- **Entidades de Domínio:** 17 (incluindo Interest)
- **Relacionamentos N:N:** 3
- **Tabelas no Banco:** 17 (incluindo interests)
- **Schemas Pydantic:** 75+ (incluindo schemas de Interests)
- **Cobertura de Testes:** Em desenvolvimento
- **Versão Atual:** v0.13.1

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
- **Usuários ADMIN (role_id = 1) NUNCA avaliam ou são avaliados** - Papel apenas administrativo
- **Usuários ARTISTA (role_id = 2) podem criar reviews normalmente**
- **Usuários ESPAÇO (role_id = 3) podem criar reviews normalmente**
- **Profile_id determinado automaticamente** pelo usuário logado
- Notas devem ser entre 1 e 5 (números inteiros)
- Depoimento deve ter no mínimo 10 caracteres e máximo 1000
- Cada review deve estar associado a UM space_event_type_id OU UM space_festival_type_id (não ambos)
- Profile_id não pode ser alterado após criação do review

### Financial (`/api/v1/financials/`) - Requer autenticação
- `POST /` - Criar novo registro financeiro/bancário
- `GET /` - Listar todos os registros financeiros
- `GET /{financial_id}` - Obter registro financeiro por ID
- `PUT /{financial_id}` - Atualizar registro financeiro
- `DELETE /{financial_id}` - Deletar registro financeiro
- `GET /profile/{profile_id}` - Obter registros financeiros de um profile
- `GET /banco/{banco}` - Obter registros por código do banco (1-999)
- `GET /tipo-conta/{tipo_conta}` - Filtrar por tipo de conta (Poupança/Corrente)
- `GET /tipo-chave-pix/{tipo_chave_pix}` - Filtrar por tipo de chave PIX
- `GET /chave-pix/{chave_pix}` - Buscar por chave PIX específica
- `GET /preferencia/{preferencia}` - Filtrar por preferência (PIX/TED)
- `GET /cpf-cnpj/{cpf_cnpj}` - Buscar por CPF ou CNPJ
- `GET /check-chave-pix/{chave_pix}` - Verificar disponibilidade de chave PIX
- `GET /statistics/banks` - Estatísticas de registros por banco
- `GET /statistics/pix-types` - Estatísticas por tipo de chave PIX

**Parâmetro `include_relations`**: Use `?include_relations=true` nos endpoints GET para incluir dados relacionados (profile).

**⚠️ REGRAS DE NEGÓCIO**:
- Código do banco deve ser uma string com 3 dígitos (001 a 999)
- Chave PIX deve ser única no sistema
- Validação específica por tipo de chave PIX (CPF: 11 dígitos, CNPJ: 14 dígitos, etc.)
- CPF/CNPJ deve ter formato válido (11 ou 14 dígitos respectivamente)
- Profile_id não pode ser alterado após criação do registro
- Tipos de conta: "Poupança" ou "Corrente"
- Tipos de chave PIX: "CPF", "CNPJ", "Celular", "E-mail", "Aleatória"
- Preferências de transferência: "PIX" ou "TED"

### Interests (`/api/v1/interests/`) - Requer autenticação
- `POST /` - Criar nova manifestação de interesse
- `GET /` - Listar todas as manifestações de interesse
- `GET /{interest_id}` - Obter manifestação por ID
- `PUT /{interest_id}` - Atualizar manifestação completa
- `DELETE /{interest_id}` - Deletar manifestação
- `PATCH /{interest_id}/status` - Atualizar status da manifestação
- `PATCH /{interest_id}/accept` - Aceitar manifestação de interesse
- `PATCH /{interest_id}/reject` - Recusar manifestação de interesse
- `GET /profile/interessado/{profile_id}` - Manifestações enviadas por um profile
- `GET /profile/interesse/{profile_id}` - Manifestações recebidas por um profile
- `GET /profile/{profile_id}/pending` - Manifestações pendentes de um profile
- `GET /profile/{profile_id}/statistics` - Estatísticas de manifestações por profile
- `GET /status/{status}` - Filtrar manifestações por status
- `GET /space-event-type/{space_event_type_id}` - Manifestações por tipo de evento
- `GET /date-range/` - Filtrar manifestações por período (query params: data_inicio, data_fim)

**Parâmetro `include_relations`**: Use `?include_relations=true` nos endpoints GET para incluir dados relacionados (profile_interessado, profile_interesse, space_event_type, space_festival_type).

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

A API estará disponível em `http://localhost:8000`
A documentação automática estará em `http://localhost:8000/docs` 