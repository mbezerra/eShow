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
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM users;"
psql -U eshow_user -d eshow -c "SELECT COUNT(*) FROM artists;"
``` 