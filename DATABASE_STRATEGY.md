# Estratégia de Banco de Dados - eShow API

## 🎯 Visão Geral

A API eShow utiliza uma estratégia de **desenvolvimento local** com **migração para produção**, permitindo desenvolvimento rápido e deploy robusto.

## 💻 Desenvolvimento (SQLite)

### **Vantagens:**
- ✅ **Rápido**: Não precisa de instalação
- ✅ **Portátil**: Arquivo único
- ✅ **Simples**: Configuração mínima
- ✅ **Isolado**: Não interfere com outros projetos

### **Configuração:**
```bash
# Arquivo .env
DATABASE_URL=sqlite:///./eshow.db
```

### **Estrutura:**
```
eshow/
├── eshow.db          # Banco SQLite local
├── init_db.py        # Script de inicialização
└── migrate_to_postgres.py  # Script de migração
```

## 🚀 Produção (PostgreSQL)

### **Vantagens:**
- ✅ **Robusto**: Banco de dados enterprise
- ✅ **Concorrência**: Múltiplas conexões simultâneas
- ✅ **Performance**: Otimizado para grandes volumes
- ✅ **Recursos**: Triggers, procedures, views
- ✅ **Backup**: Ferramentas nativas de backup

### **Migração:**
```bash
# 1. Configurar PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/eshow

# 2. Executar migração
python migrate_to_postgres.py

# 3. Verificar dados
psql -U user -d eshow -c "SELECT * FROM users;"
```

## 🔄 Processo de Migração

### **1. Preparação**
```bash
# Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Criar banco e usuário
sudo -u postgres psql
CREATE DATABASE eshow;
CREATE USER eshow_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE eshow TO eshow_user;
\q
```

### **2. Configuração**
```bash
# Editar .env
DATABASE_URL=postgresql://eshow_user:secure_password@localhost/eshow
```

### **3. Migração**
```bash
# Executar script de migração
python migrate_to_postgres.py
```

### **4. Verificação**
```bash
# Testar conexão
python -c "
from infrastructure.database.database import engine
with engine.connect() as conn:
    result = conn.execute('SELECT COUNT(*) FROM users')
    print(f'Usuários migrados: {result.fetchone()[0]}')
    result = conn.execute('SELECT COUNT(*) FROM artists')
    print(f'Artistas migrados: {result.fetchone()[0]}')
"
```

## 📊 Compatibilidade

### **Modelos SQLAlchemy:**
- ✅ **Completamente compatíveis** entre SQLite e PostgreSQL
- ✅ **Tipos de dados** mapeados corretamente
- ✅ **Índices** criados automaticamente
- ✅ **Constraints** mantidos

### **Diferenças:**
| Recurso | SQLite | PostgreSQL |
|---------|--------|------------|
| Timestamps | `CURRENT_TIMESTAMP` | `NOW()` |
| Boolean | `0/1` | `true/false` |
| Text | `VARCHAR` | `VARCHAR/TEXT` |
| Concorrência | Limitada | Alta |

## 🛠️ Ferramentas

### **Desenvolvimento:**
- `init_db.py` - Inicializar SQLite
- `sqlite3 eshow.db` - Acessar banco diretamente

### **Migração:**
- `migrate_to_postgres.py` - Script de migração
- `alembic` - Migrações de schema

### **Produção:**
- `psql` - Cliente PostgreSQL
- `pg_dump` - Backup
- `pg_restore` - Restore

## 🔒 Segurança

### **Desenvolvimento:**
- Banco local, sem acesso externo
- Dados de teste apenas

### **Produção:**
- Usuário dedicado com privilégios mínimos
- Conexão via SSL
- Backup automático
- Monitoramento de performance

## 📈 Monitoramento

### **SQLite:**
```bash
# Verificar tamanho
ls -lh eshow.db

# Verificar integridade
sqlite3 eshow.db "PRAGMA integrity_check;"
```

### **PostgreSQL:**
```sql
-- Verificar conexões
SELECT count(*) FROM pg_stat_activity;

-- Verificar performance
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
FROM pg_stat_user_tables;
```

## 📋 Estrutura de Dados - Interests

### **Tabela Interests:**
```sql
CREATE TABLE interests (
    id INTEGER PRIMARY KEY,
    profile_id_interessado INTEGER NOT NULL REFERENCES profiles(id),
    profile_id_interesse INTEGER NOT NULL REFERENCES profiles(id),
    data_inicial DATE NOT NULL,
    horario_inicial TIME NOT NULL,
    duracao_apresentacao DECIMAL(3,1) NOT NULL CHECK (duracao_apresentacao >= 0.5 AND duracao_apresentacao <= 8.0),
    valor_hora_ofertado DECIMAL(10,2) NOT NULL CHECK (valor_hora_ofertado > 0),
    valor_couvert_ofertado DECIMAL(10,2) NOT NULL CHECK (valor_couvert_ofertado > 0),
    mensagem TEXT NOT NULL CHECK (LENGTH(mensagem) >= 10 AND LENGTH(mensagem) <= 1000),
    status VARCHAR(50) NOT NULL DEFAULT 'AGUARDANDO_CONFIRMACAO' CHECK (status IN ('AGUARDANDO_CONFIRMACAO', 'ACEITO', 'RECUSADO')),
    resposta TEXT,
    space_event_type_id INTEGER REFERENCES space_event_types(id),
    space_festival_type_id INTEGER REFERENCES space_festival_types(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (space_event_type_id IS NOT NULL AND space_festival_type_id IS NULL) OR
        (space_event_type_id IS NULL AND space_festival_type_id IS NOT NULL) OR
        (space_event_type_id IS NULL AND space_festival_type_id IS NULL)
    ),
    UNIQUE(profile_id_interessado, profile_id_interesse)
);
```

### **Características:**
- ✅ **Relacionamento bidirecional**: Profile interessado ↔ Profile interesse
- ✅ **Prevenção de duplicatas**: Constraint UNIQUE para evitar manifestações duplicadas
- ✅ **Validação de duração**: Entre 0.5 e 8.0 horas
- ✅ **Valores monetários**: Positivos com precisão decimal
- ✅ **Mensagem obrigatória**: Entre 10 e 1000 caracteres
- ✅ **Estados de status**: 3 estados predefinidos com constraint
- ✅ **Relacionamento opcional**: Evento OU festival OU nenhum
- ✅ **Auditoria**: Campos created_at e updated_at automáticos
- ✅ **Integridade**: Foreign keys para profiles e tipos

### **Consultas Úteis:**
```sql
-- Distribuição por status
SELECT status, COUNT(*) as quantidade
FROM interests 
GROUP BY status 
ORDER BY quantidade DESC;

-- Manifestações por profile interessado
SELECT p.name, COUNT(i.id) as manifestacoes_enviadas
FROM profiles p
LEFT JOIN interests i ON p.id = i.profile_id_interessado
GROUP BY p.id, p.name
ORDER BY manifestacoes_enviadas DESC;

-- Manifestações por profile de interesse
SELECT p.name, COUNT(i.id) as manifestacoes_recebidas
FROM profiles p
LEFT JOIN interests i ON p.id = i.profile_id_interesse
GROUP BY p.id, p.name
ORDER BY manifestacoes_recebidas DESC;

-- Estatísticas por profile
SELECT 
    p.name,
    COUNT(CASE WHEN i.profile_id_interessado = p.id THEN 1 END) as enviadas,
    COUNT(CASE WHEN i.profile_id_interesse = p.id THEN 1 END) as recebidas,
    COUNT(CASE WHEN i.profile_id_interessado = p.id AND i.status = 'AGUARDANDO_CONFIRMACAO' THEN 1 END) as pendentes_enviadas,
COUNT(CASE WHEN i.profile_id_interesse = p.id AND i.status = 'AGUARDANDO_CONFIRMACAO' THEN 1 END) as pendentes_recebidas,
    AVG(CASE WHEN i.profile_id_interessado = p.id THEN i.valor_hora_ofertado END) as media_valor_enviado,
    AVG(CASE WHEN i.profile_id_interesse = p.id THEN i.valor_hora_ofertado END) as media_valor_recebido
FROM profiles p
LEFT JOIN interests i ON p.id IN (i.profile_id_interessado, i.profile_id_interesse)
GROUP BY p.id, p.name
ORDER BY (enviadas + recebidas) DESC;

-- Manifestações por período
SELECT DATE(data_inicial) as data, COUNT(*) as total
FROM interests 
WHERE data_inicial >= '2025-01-01'
GROUP BY DATE(data_inicial)
ORDER BY data;

-- Verificar duplicatas (não deve retornar nada)
SELECT profile_id_interessado, profile_id_interesse, COUNT(*) as total
FROM interests
GROUP BY profile_id_interessado, profile_id_interesse
HAVING COUNT(*) > 1;

-- Manifestações por tipo de evento
SELECT set.id, et.name as tipo_evento, COUNT(i.id) as total_manifestacoes
FROM space_event_types set
JOIN event_types et ON set.event_type_id = et.id
LEFT JOIN interests i ON set.id = i.space_event_type_id
GROUP BY set.id, et.name
ORDER BY total_manifestacoes DESC;

-- Manifestações por tipo de festival
SELECT sft.id, ft.name as tipo_festival, COUNT(i.id) as total_manifestacoes
FROM space_festival_types sft
JOIN festival_types ft ON sft.festival_type_id = ft.id
LEFT JOIN interests i ON sft.id = i.space_festival_type_id
GROUP BY sft.id, ft.name
ORDER BY total_manifestacoes DESC;

-- Valores médios por status
SELECT 
    status,
    COUNT(*) as total,
    AVG(valor_hora_ofertado) as media_valor_hora,
    AVG(valor_couvert_ofertado) as media_couvert,
    AVG(duracao_apresentacao) as media_duracao
FROM interests
GROUP BY status
ORDER BY total DESC;
```

## 📋 Estrutura de Dados - Reviews

### **Tabela Reviews:**
```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    profile_id INTEGER NOT NULL REFERENCES profiles(id),
    space_event_type_id INTEGER REFERENCES space_event_types(id),
    space_festival_type_id INTEGER REFERENCES space_festival_types(id),
    data_hora TIMESTAMP NOT NULL,
    nota INTEGER NOT NULL CHECK (nota >= 1 AND nota <= 5),
    depoimento TEXT NOT NULL CHECK (LENGTH(depoimento) >= 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (space_event_type_id IS NOT NULL AND space_festival_type_id IS NULL) OR
        (space_event_type_id IS NULL AND space_festival_type_id IS NOT NULL)
    )
);
```

### **Características:**
- ✅ **Regras de role**: ADMIN não avalia, ARTISTA e ESPAÇO podem avaliar
- ✅ **Profile_id automático**: Determinado pelo usuário logado
- ✅ **Notas**: Apenas valores inteiros de 1 a 5
- ✅ **Relacionamento exclusivo**: OU evento OU festival, nunca ambos
- ✅ **Depoimento obrigatório**: Mínimo 10 caracteres
- ✅ **Auditoria**: Campos created_at e updated_at automáticos
- ✅ **Integridade**: Foreign keys para profiles e tipos

### **Consultas Úteis:**
```sql
-- Média de avaliações por profile
SELECT profile_id, AVG(nota::float) as media, COUNT(*) as total
FROM reviews 
GROUP BY profile_id;

-- Distribuição de notas
SELECT nota, COUNT(*) as quantidade
FROM reviews 
GROUP BY nota 
ORDER BY nota;

-- Reviews por período
SELECT DATE(data_hora) as data, COUNT(*) as total
FROM reviews 
WHERE data_hora >= '2025-01-01'
GROUP BY DATE(data_hora)
ORDER BY data;
```

## 📋 Estrutura de Dados - Financial

### **Tabela Financials:**
```sql
CREATE TABLE financials (
    id INTEGER PRIMARY KEY,
    profile_id INTEGER NOT NULL REFERENCES profiles(id),
    banco VARCHAR(3) NOT NULL CHECK (LENGTH(banco) = 3 AND banco GLOB '[0-9][0-9][0-9]' AND CAST(banco AS INTEGER) >= 1 AND CAST(banco AS INTEGER) <= 999),
    agencia VARCHAR(10) NOT NULL,
    conta VARCHAR(15) NOT NULL,
    tipo_conta VARCHAR(20) NOT NULL CHECK (tipo_conta IN ('Poupança', 'Corrente')),
    cpf_cnpj VARCHAR(20) NOT NULL,
    tipo_chave_pix VARCHAR(20) NOT NULL CHECK (tipo_chave_pix IN ('CPF', 'CNPJ', 'Celular', 'E-mail', 'Aleatória')),
    chave_pix VARCHAR(50) NOT NULL UNIQUE,
    preferencia VARCHAR(10) NOT NULL CHECK (preferencia IN ('PIX', 'TED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Características:**
- ✅ **Chave PIX única**: Constraint de unicidade para evitar duplicações
- ✅ **Código do banco**: String com 3 dígitos (001 a 999) seguindo padrão brasileiro
- ✅ **Tipos de conta**: Apenas "Poupança" ou "Corrente"
- ✅ **Tipos de chave PIX**: 5 tipos suportados (CPF, CNPJ, Celular, E-mail, Aleatória)
- ✅ **Preferências**: PIX ou TED para transferências
- ✅ **Auditoria**: Campos created_at e updated_at automáticos
- ✅ **Integridade**: Foreign key para profiles

### **Consultas Úteis:**
```sql
-- Distribuição por banco (string com 3 dígitos)
SELECT banco, COUNT(*) as quantidade
FROM financials 
GROUP BY banco 
ORDER BY banco;

-- Distribuição por tipo de chave PIX
SELECT tipo_chave_pix, COUNT(*) as quantidade
FROM financials 
GROUP BY tipo_chave_pix 
ORDER BY quantidade DESC;

-- Registros por profile
SELECT p.name, COUNT(f.id) as total_financials
FROM profiles p
LEFT JOIN financials f ON p.id = f.profile_id
GROUP BY p.id, p.name
ORDER BY total_financials DESC;

-- Verificar chaves PIX duplicadas (não deve retornar nada)
SELECT chave_pix, COUNT(*) as total
FROM financials
GROUP BY chave_pix
HAVING COUNT(*) > 1;

-- Bancos mais utilizados com nomes
SELECT 
    CASE banco
        WHEN '001' THEN 'Banco do Brasil'
        WHEN '033' THEN 'Santander'
        WHEN '104' THEN 'Caixa'
        WHEN '237' THEN 'Bradesco'
        WHEN '260' THEN 'Nu Pagamentos'
        WHEN '341' THEN 'Itaú'
        ELSE 'Banco ' || banco
    END as nome_banco,
    banco,
    COUNT(*) as total
FROM financials
GROUP BY banco
ORDER BY total DESC;
```

## 📋 Estrutura de Dados - Space Event Types

### **Tabela Space Event Types:**
```sql
CREATE TABLE space_event_types (
    id INTEGER PRIMARY KEY,
    space_id INTEGER NOT NULL REFERENCES spaces(id),
    event_type_id INTEGER NOT NULL REFERENCES event_types(id),
    tema VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    status VARCHAR(11) NOT NULL DEFAULT 'CONTRATANDO' CHECK (status IN ('CONTRATANDO', 'FECHADO', 'SUSPENSO', 'CANCELADO')),
    link_divulgacao VARCHAR(500),
    banner VARCHAR(500),
    data DATETIME NOT NULL,
    horario VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Características:**
- ✅ **Relacionamento N:N**: Espaços ↔ Tipos de Eventos
- ✅ **Campo status**: 4 estados predefinidos com constraint
- ✅ **Valor padrão**: CONTRATANDO para novos registros
- ✅ **Campos obrigatórios**: tema, descricao, data, horario
- ✅ **Campos opcionais**: link_divulgacao, banner
- ✅ **Integridade**: Foreign keys para spaces e event_types
- ✅ **Auditoria**: Campo created_at automático

### **Consultas Úteis:**
```sql
-- Distribuição por status
SELECT status, COUNT(*) as quantidade
FROM space_event_types 
GROUP BY status 
ORDER BY quantidade DESC;

-- Eventos por espaço
SELECT s.profile_id, COUNT(set.id) as total_eventos
FROM spaces s
LEFT JOIN space_event_types set ON s.id = set.space_id
GROUP BY s.id, s.profile_id
ORDER BY total_eventos DESC;

-- Eventos por tipo
SELECT et.type, COUNT(set.id) as total_eventos
FROM event_types et
LEFT JOIN space_event_types set ON et.id = set.event_type_id
GROUP BY et.id, et.type
ORDER BY total_eventos DESC;

-- Eventos futuros
SELECT set.tema, set.data, set.horario, set.status
FROM space_event_types set
WHERE set.data >= CURRENT_DATE
ORDER BY set.data, set.horario;

-- Eventos por status e período
SELECT 
    set.status,
    DATE(set.data) as data_evento,
    COUNT(*) as total
FROM space_event_types set
WHERE set.data >= '2025-01-01'
GROUP BY set.status, DATE(set.data)
ORDER BY data_evento, set.status;

-- Espaços com mais eventos ativos
SELECT 
    s.profile_id,
    COUNT(CASE WHEN set.status = 'CONTRATANDO' THEN 1 END) as contratando,
    COUNT(CASE WHEN set.status = 'FECHADO' THEN 1 END) as fechado,
    COUNT(CASE WHEN set.status = 'SUSPENSO' THEN 1 END) as suspenso,
    COUNT(CASE WHEN set.status = 'CANCELADO' THEN 1 END) as cancelado
FROM spaces s
LEFT JOIN space_event_types set ON s.id = set.space_id
GROUP BY s.id, s.profile_id
ORDER BY (contratando + fechado) DESC;

-- Verificar eventos sem banner
SELECT set.id, set.tema, set.data
FROM space_event_types set
WHERE set.banner IS NULL OR set.banner = '';

-- Eventos com links de divulgação
SELECT set.tema, set.link_divulgacao, set.status
FROM space_event_types set
WHERE set.link_divulgacao IS NOT NULL AND set.link_divulgacao != ''
ORDER BY set.data;
```

## 📋 Estrutura de Dados - Space Festival Types

### **Tabela Space Festival Types:**
```sql
CREATE TABLE space_festival_types (
    id INTEGER PRIMARY KEY,
    space_id INTEGER NOT NULL REFERENCES spaces(id),
    festival_type_id INTEGER NOT NULL REFERENCES festival_types(id),
    tema VARCHAR(200) NOT NULL,
    descricao TEXT NOT NULL,
    status VARCHAR(11) NOT NULL DEFAULT 'CONTRATANDO' CHECK (status IN ('CONTRATANDO', 'FECHADO', 'SUSPENSO', 'CANCELADO')),
    link_divulgacao VARCHAR(500),
    banner VARCHAR(500),
    data DATETIME NOT NULL,
    horario VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### **Características:**
- ✅ **Relacionamento N:N**: Espaços ↔ Tipos de Festivais
- ✅ **Campo status**: 4 estados predefinidos com constraint
- ✅ **Valor padrão**: CONTRATANDO para novos registros
- ✅ **Campos obrigatórios**: tema, descricao, data, horario
- ✅ **Campos opcionais**: link_divulgacao, banner
- ✅ **Integridade**: Foreign keys para spaces e festival_types
- ✅ **Auditoria**: Campo created_at automático

### **Consultas Úteis:**
```sql
-- Distribuição por status
SELECT status, COUNT(*) as quantidade
FROM space_festival_types 
GROUP BY status 
ORDER BY quantidade DESC;

-- Festivais por espaço
SELECT s.profile_id, COUNT(sft.id) as total_festivais
FROM spaces s
LEFT JOIN space_festival_types sft ON s.id = sft.space_id
GROUP BY s.id, s.profile_id
ORDER BY total_festivais DESC;

-- Festivais por tipo
SELECT ft.type, COUNT(sft.id) as total_festivais
FROM festival_types ft
LEFT JOIN space_festival_types sft ON ft.id = sft.festival_type_id
GROUP BY ft.id, ft.type
ORDER BY total_festivais DESC;

-- Festivais futuros
SELECT sft.tema, sft.data, sft.horario, sft.status
FROM space_festival_types sft
WHERE sft.data >= CURRENT_DATE
ORDER BY sft.data, sft.horario;

-- Festivais por status e período
SELECT 
    sft.status,
    DATE(sft.data) as data_festival,
    COUNT(*) as total
FROM space_festival_types sft
WHERE sft.data >= '2025-01-01'
GROUP BY sft.status, DATE(sft.data)
ORDER BY data_festival, sft.status;

-- Espaços com mais festivais ativos
SELECT 
    s.profile_id,
    COUNT(CASE WHEN sft.status = 'CONTRATANDO' THEN 1 END) as contratando,
    COUNT(CASE WHEN sft.status = 'FECHADO' THEN 1 END) as fechado,
    COUNT(CASE WHEN sft.status = 'SUSPENSO' THEN 1 END) as suspenso,
    COUNT(CASE WHEN sft.status = 'CANCELADO' THEN 1 END) as cancelado
FROM spaces s
LEFT JOIN space_festival_types sft ON s.id = sft.space_id
GROUP BY s.id, s.profile_id
ORDER BY (contratando + fechado) DESC;

-- Verificar festivais sem banner
SELECT sft.id, sft.tema, sft.data
FROM space_festival_types sft
WHERE sft.banner IS NULL OR sft.banner = '';

-- Festivais com links de divulgação
SELECT sft.tema, sft.link_divulgacao, sft.status
FROM space_festival_types sft
WHERE sft.link_divulgacao IS NOT NULL AND sft.link_divulgacao != ''
ORDER BY sft.data;
```

## 🎯 Próximos Passos

1. **Desenvolvimento**: Continuar com SQLite
2. **Testes**: Implementar testes com banco em memória
3. **Staging**: Configurar PostgreSQL para testes
4. **Produção**: Migração final com backup

## 📝 Comandos Úteis

```bash
# Backup SQLite
cp eshow.db eshow_backup_$(date +%Y%m%d).db

# Backup PostgreSQL
pg_dump -U eshow_user eshow > eshow_backup_$(date +%Y%m%d).sql

# Restore PostgreSQL
psql -U eshow_user eshow < eshow_backup_20250719.sql

# Verificar dados
sqlite3 eshow.db "SELECT COUNT(*) FROM users;"
sqlite3 eshow.db "SELECT COUNT(*) FROM artists;"
sqlite3 eshow.db "SELECT COUNT(*) FROM reviews;"
sqlite3 eshow.db "SELECT COUNT(*) FROM interests;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM users;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM artists;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM reviews;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM interests;"

# Verificar médias de avaliação
sqlite3 eshow.db "SELECT profile_id, AVG(nota) as media FROM reviews GROUP BY profile_id;"
psql -U eshow_user -d eshow -c "SELECT profile_id, AVG(nota::float) as media FROM reviews GROUP BY profile_id;"

# Verificar reviews por role (deve excluir ADMIN)
sqlite3 eshow.db "SELECT p.role_id, COUNT(r.id) as total_reviews FROM profiles p LEFT JOIN reviews r ON p.id = r.profile_id GROUP BY p.role_id ORDER BY p.role_id;"
psql -U eshow_user -d eshow -c "SELECT p.role_id, COUNT(r.id) as total_reviews FROM profiles p LEFT JOIN reviews r ON p.id = r.profile_id GROUP BY p.role_id ORDER BY p.role_id;"

# Verificar dados financeiros
sqlite3 eshow.db "SELECT COUNT(*) FROM financials;"
sqlite3 eshow.db "SELECT banco, COUNT(*) FROM financials GROUP BY banco ORDER BY banco;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM financials;"
psql -U eshow_user -d eshow -c "SELECT banco, COUNT(*) FROM financials GROUP BY banco ORDER BY banco;"

# Verificar manifestações de interesse
sqlite3 eshow.db "SELECT status, COUNT(*) FROM interests GROUP BY status;"
sqlite3 eshow.db "SELECT COUNT(*) FROM interests WHERE status = 'AGUARDANDO_CONFIRMACAO';"
psql -U eshow_user -d eshow -c "SELECT status, COUNT(*) FROM interests GROUP BY status;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM interests WHERE status = 'AGUARDANDO_CONFIRMACAO';"

# Verificar estrutura da coluna banco (deve ser VARCHAR(3))
sqlite3 eshow.db "PRAGMA table_info(financials);" | grep banco
psql -U eshow_user -d eshow -c "\d financials" | grep banco

# Verificar estrutura da tabela interests
sqlite3 eshow.db "PRAGMA table_info(interests);"
psql -U eshow_user -d eshow -c "\d interests"

# Verificar estrutura da tabela space_event_types
sqlite3 eshow.db "PRAGMA table_info(space_event_types);"
psql -U eshow_user -d eshow -c "\d space_event_types"

# Verificar campo status em space_event_types
sqlite3 eshow.db "SELECT status, COUNT(*) FROM space_event_types GROUP BY status;"
psql -U eshow_user -d eshow -c "SELECT status, COUNT(*) FROM space_event_types GROUP BY status;"

# Verificar estrutura da tabela space_festival_types
sqlite3 eshow.db "PRAGMA table_info(space_festival_types);"
psql -U eshow_user -d eshow -c "\d space_festival_types"

# Verificar campo status em space_festival_types
sqlite3 eshow.db "SELECT status, COUNT(*) FROM space_festival_types GROUP BY status;"
psql -U eshow_user -d eshow -c "SELECT status, COUNT(*) FROM space_festival_types GROUP BY status;"

# Verificar eventos por status
sqlite3 eshow.db "SELECT status, COUNT(*) as total FROM space_event_types GROUP BY status ORDER BY total DESC;"
psql -U eshow_user -d eshow -c "SELECT status, COUNT(*) as total FROM space_event_types GROUP BY status ORDER BY total DESC;"

# Verificar dados de busca por localização
sqlite3 eshow.db "SELECT COUNT(*) FROM artists WHERE raio_atuacao > 0;"
sqlite3 eshow.db "SELECT AVG(raio_atuacao) as media_raio FROM artists;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM artists WHERE raio_atuacao > 0;"
psql -U eshow_user -d eshow -c "SELECT AVG(raio_atuacao) as media_raio FROM artists;"

# Verificar CEPs válidos
sqlite3 eshow.db "SELECT COUNT(*) FROM profiles WHERE cep IS NOT NULL AND cep != '';"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM profiles WHERE cep IS NOT NULL AND cep != '';"
```

## 📋 Estrutura de Dados - Location Search

### **Visão Geral:**
O sistema de busca por localização utiliza os dados existentes das tabelas `profiles`, `artists`, `spaces`, `space_event_types`, `space_festival_types` e `bookings` para realizar cálculos geográficos e verificações de disponibilidade.

### **Dados Utilizados:**

#### **Tabela Profiles (CEP e Coordenadas Geográficas):**
```sql
-- CEPs e coordenadas dos profiles são usados para cálculo de distância
SELECT id, cep, cidade, uf, role_id, latitude, longitude 
FROM profiles 
WHERE role_id IN (2, 3); -- Artistas e Espaços
```

#### **Tabela Artists (Raio de Atuação):**
```sql
-- Campo raio_atuacao define o alcance geográfico do artista
SELECT id, profile_id, raio_atuacao 
FROM artists;
```

#### **Tabela Spaces (Dados do Espaço):**
```sql
-- Dados do espaço para retorno completo
SELECT id, profile_id, space_type_id, valor_hora, valor_couvert 
FROM spaces;
```

#### **Tabela Space Event Types (Disponibilidade):**
```sql
-- Eventos com status CONTRATANDO são considerados disponíveis
SELECT id, space_id, status, data, horario 
FROM space_event_types 
WHERE status = 'CONTRATANDO';
```

#### **Tabela Space Festival Types (Disponibilidade):**
```sql
-- Festivais com status CONTRATANDO são considerados disponíveis
SELECT id, space_id, status, data, horario 
FROM space_festival_types 
WHERE status = 'CONTRATANDO';
```

#### **Tabela Bookings (Conflitos de Agenda):**
```sql
-- Agendamentos existentes para verificar conflitos
SELECT id, artist_id, space_id, data_inicio, data_fim, horario_inicio, horario_fim 
FROM bookings;
```

### **Consultas de Busca:**

#### **Busca de Espaços para Artista:**
```sql
-- 1. Obter dados do artista
SELECT a.id, a.raio_atuacao, p.cep as cep_artista, p.latitude as lat_artista, p.longitude as lng_artista
FROM artists a
JOIN profiles p ON a.profile_id = p.id
WHERE p.id = ?;

-- 2. Buscar espaços com eventos/festivais disponíveis
SELECT DISTINCT s.id, s.profile_id, sp.cep as cep_espaco, sp.latitude as lat_espaco, sp.longitude as lng_espaco
FROM spaces s
JOIN profiles sp ON s.profile_id = sp.id
WHERE sp.role_id = 3
AND (
    EXISTS (
        SELECT 1 FROM space_event_types set 
        WHERE set.space_id = s.id 
        AND set.status = 'CONTRATANDO'
    )
    OR
    EXISTS (
        SELECT 1 FROM space_festival_types sft 
        WHERE sft.space_id = s.id 
        AND sft.status = 'CONTRATANDO'
    )
);
```

#### **Busca de Artistas para Espaço:**
```sql
-- 1. Obter dados do espaço
SELECT s.id, sp.cep as cep_espaco, sp.latitude as lat_espaco, sp.longitude as lng_espaco
FROM spaces s
JOIN profiles sp ON s.profile_id = sp.id
WHERE sp.id = ?;

-- 2. Buscar artistas disponíveis
SELECT a.id, a.profile_id, a.raio_atuacao, p.cep as cep_artista, p.latitude as lat_artista, p.longitude as lng_artista
FROM artists a
JOIN profiles p ON a.profile_id = p.id
WHERE p.role_id = 2
AND NOT EXISTS (
    -- Verificar conflitos de agenda
    SELECT 1 FROM bookings b
    WHERE b.artist_id = a.id
    AND b.data_inicio = ? -- Data do evento/festival
    AND (
        (b.horario_inicio <= ? AND b.horario_fim > ?) OR -- Conflito de horário
        (b.horario_inicio < ? AND b.horario_fim >= ?) OR -- Conflito de horário
        (b.horario_inicio >= ? AND b.horario_fim <= ?)   -- Conflito de horário
    )
);
```

### **Otimizações de Performance:**

#### **Índices Recomendados:**
```sql
-- Para busca por role_id em profiles
CREATE INDEX idx_profiles_role_id ON profiles(role_id);

-- Para busca por status em space_event_types
CREATE INDEX idx_space_event_types_status ON space_event_types(status);

-- Para busca por status em space_festival_types
CREATE INDEX idx_space_festival_types_status ON space_festival_types(status);

-- Para busca por artist_id e data em bookings
CREATE INDEX idx_bookings_artist_date ON bookings(artist_id, data_inicio, data_fim);

-- Para busca por space_id em space_event_types
CREATE INDEX idx_space_event_types_space_id ON space_event_types(space_id);

-- Para busca por space_id em space_festival_types
CREATE INDEX idx_space_festival_types_space_id ON space_festival_types(space_id);
```

#### **Consultas de Monitoramento:**
```sql
-- Verificar performance das buscas
EXPLAIN ANALYZE
SELECT DISTINCT s.id, s.profile_id
FROM spaces s
JOIN profiles sp ON s.profile_id = sp.id
WHERE sp.role_id = 3
AND EXISTS (
    SELECT 1 FROM space_event_types set 
    WHERE set.space_id = s.id 
    AND set.status = 'CONTRATANDO'
);

-- Estatísticas de uso
SELECT 
    'Artistas' as tipo,
    COUNT(*) as total,
    AVG(raio_atuacao) as media_raio
FROM artists
UNION ALL
SELECT 
    'Espaços' as tipo,
    COUNT(*) as total,
    NULL as media_raio
FROM spaces;

-- Distribuição de raios de atuação
SELECT 
    CASE 
        WHEN raio_atuacao <= 10 THEN '0-10km'
        WHEN raio_atuacao <= 25 THEN '11-25km'
        WHEN raio_atuacao <= 50 THEN '26-50km'
        WHEN raio_atuacao <= 100 THEN '51-100km'
        ELSE '100+km'
    END as faixa_raio,
    COUNT(*) as quantidade
FROM artists
GROUP BY faixa_raio
ORDER BY quantidade DESC;

-- Eventos/festivais disponíveis por região
SELECT 
    p.uf,
    COUNT(CASE WHEN set.status = 'CONTRATANDO' THEN 1 END) as eventos_disponiveis,
    COUNT(CASE WHEN sft.status = 'CONTRATANDO' THEN 1 END) as festivais_disponiveis
FROM profiles p
LEFT JOIN spaces s ON p.id = s.profile_id
LEFT JOIN space_event_types set ON s.id = set.space_id
LEFT JOIN space_festival_types sft ON s.id = sft.space_id
WHERE p.role_id = 3
GROUP BY p.uf
ORDER BY (eventos_disponiveis + festivais_disponiveis) DESC;
```

### **Considerações de Escalabilidade:**

1. **Cache de Coordenadas**: Implementar cache Redis para coordenadas geográficas
2. **Índices Espaciais**: Considerar índices espaciais para PostgreSQL com PostGIS
3. **Particionamento**: Particionar por região geográfica em grandes volumes
4. **CDN**: Cache de resultados de busca frequentes 