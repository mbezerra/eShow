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
    banco INTEGER NOT NULL CHECK (banco >= 1 AND banco <= 999),
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
- ✅ **Validação de banco**: Códigos de 1 a 999 (padrão brasileiro)
- ✅ **Tipos de conta**: Apenas "Poupança" ou "Corrente"
- ✅ **Tipos de chave PIX**: 5 tipos suportados (CPF, CNPJ, Celular, E-mail, Aleatória)
- ✅ **Preferências**: PIX ou TED para transferências
- ✅ **Auditoria**: Campos created_at e updated_at automáticos
- ✅ **Integridade**: Foreign key para profiles

### **Consultas Úteis:**
```sql
-- Distribuição por banco
SELECT banco, COUNT(*) as quantidade
FROM financials 
GROUP BY banco 
ORDER BY quantidade DESC;

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
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM users;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM artists;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM reviews;"

# Verificar médias de avaliação
sqlite3 eshow.db "SELECT profile_id, AVG(nota) as media FROM reviews GROUP BY profile_id;"
psql -U eshow_user -d eshow -c "SELECT profile_id, AVG(nota::float) as media FROM reviews GROUP BY profile_id;"
``` 