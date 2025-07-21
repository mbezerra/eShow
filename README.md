# eShow API - Arquitetura Hexagonal

Esta é uma API construída usando FastAPI e arquitetura hexagonal (também conhecida como arquitetura de portas e adaptadores).

## Estrutura do Projeto

```
eshow/
├── app/                    # Camada de aplicação (adaptadores de entrada)
│   ├── api/               # Controllers/endpoints da API
│   ├── schemas/           # Schemas Pydantic para validação
│   └── main.py           # Ponto de entrada da aplicação
├── domain/                # Camada de domínio (núcleo da aplicação)
│   ├── entities/          # Entidades de domínio
│   ├── repositories/      # Interfaces dos repositórios
│   └── services/          # Serviços de domínio
├── infrastructure/        # Camada de infraestrutura (adaptadores de saída)
│   ├── database/          # Configuração e modelos do banco
│   ├── repositories/      # Implementações dos repositórios
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

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Configurar variáveis de ambiente:
```bash
cp env.example .env
# Editar o arquivo .env e configurar SECRET_KEY
```

3. Inicializar banco de dados:
```bash
python init_db.py
```

4. Iniciar o servidor:
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
- `POST /` - Criar novo artista
- `GET /` - Listar todos os artistas
- `GET /{artist_id}` - Obter artista por ID
- `GET /profile/{profile_id}` - Obter artista por profile ID
- `GET /type/{artist_type_id}` - Listar artistas por tipo
- `PUT /{artist_id}` - Atualizar artista
- `DELETE /{artist_id}` - Deletar artista

**Parâmetro `include_relations`**: Use `?include_relations=true` nos endpoints GET para incluir dados relacionados (profile e artist_type).

A API estará disponível em `http://localhost:8000`
A documentação automática estará em `http://localhost:8000/docs` 