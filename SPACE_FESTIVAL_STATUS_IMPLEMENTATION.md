# Implementação do Campo Status em Space Festival Types

## 📋 Visão Geral

Implementação completa do campo `status` na entidade `SpaceFestivalType`, seguindo o mesmo padrão estabelecido para `SpaceEventType`. O campo permite controlar o estado dos festivais com 4 valores possíveis.

## 🎯 Funcionalidades Implementadas

### 1. Enum StatusFestivalType
```python
class StatusFestivalType(Enum):
    """Enum para os status possíveis de um festival"""
    CONTRATANDO = "CONTRATANDO"
    FECHADO = "FECHADO"
    SUSPENSO = "SUSPENSO"
    CANCELADO = "CANCELADO"
```

### 2. Entidade de Domínio Atualizada
- **Arquivo**: `domain/entities/space_festival_type.py`
- **Campo adicionado**: `status: StatusFestivalType = StatusFestivalType.CONTRATANDO`
- **Validação**: Verificação se o status é um valor válido do enum

### 3. Modelo de Banco de Dados
- **Arquivo**: `infrastructure/database/models/space_festival_type_model.py`
- **Coluna adicionada**: `status = Column(SQLAlchemyEnum(StatusFestivalType), nullable=False, default=StatusFestivalType.CONTRATANDO)`
- **Tipo**: SQLAlchemyEnum com valor padrão

### 4. Schemas Pydantic
- **Arquivo**: `app/schemas/space_festival_type.py`
- **Schemas atualizados**:
  - `SpaceFestivalTypeBase`: Campo status com validação
  - `SpaceFestivalTypeUpdate`: Campo status opcional
  - `SpaceFestivalTypeStatusUpdate`: Schema específico para atualização de status
- **Validações**: Verificação de valores válidos do enum

### 5. Repositório
- **Interface**: `domain/repositories/space_festival_type_repository.py`
  - Método `update_status()` adicionado
- **Implementação**: `infrastructure/repositories/space_festival_type_repository_impl.py`
  - Método `update_status()` implementado
  - Campo status incluído em `create()`, `update()` e `_to_entity()`

### 6. Serviço
- **Arquivo**: `app/application/services/space_festival_type_service.py`
- **Método adicionado**: `update_space_festival_type_status()`
- **Campo status**: Incluído em `create_space_festival_type()` e `update_space_festival_type()`

### 7. Endpoints
- **Arquivo**: `app/api/endpoints/space_festival_types.py`
- **Novo endpoint**: `PATCH /{id}/status` para atualização específica de status
- **Funções atualizadas**: `convert_space_festival_type_to_response()` inclui campo status
- **Autenticação**: Todos os endpoints requerem autenticação JWT

## 🔄 Migração do Banco de Dados

### Arquivo de Migração
- **Arquivo**: `alembic/versions/6a3d349eb6db_adicionar_coluna_status_em_space_.py`
- **Comando**: `alembic revision --autogenerate -m "adicionar_coluna_status_em_space_festival_types"`
- **Ajustes**: Configurado para SQLite com `server_default='CONTRATANDO'`

### Aplicação da Migração
```bash
alembic upgrade head
```

### Verificação
```sql
-- Estrutura da tabela
PRAGMA table_info(space_festival_types);

-- Dados inseridos
SELECT id, tema, status FROM space_festival_types LIMIT 5;
```

## 📊 Script de Inicialização

### Arquivo Atualizado
- **Arquivo**: `init_space_festival_types.py`
- **Campo status**: Adicionado em todos os dados de exemplo
- **Distribuição de status**:
  - CONTRATANDO: 3 registros
  - FECHADO: 3 registros
  - SUSPENSO: 2 registros
  - CANCELADO: 2 registros

### Execução
```bash
python init_space_festival_types.py
```

## 🧪 Testes Realizados

### 1. Teste de Listagem
```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Authorization: Bearer $TOKEN"
```

**Resultado**: ✅ Campo status retornado corretamente

### 2. Teste de Atualização de Status
```bash
curl -X PATCH "http://localhost:8000/api/v1/space-festival-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "FECHADO"}'
```

**Resultado**: ✅ Status atualizado com sucesso

### 3. Verificação no Banco
```sql
SELECT id, tema, status FROM space_festival_types WHERE id = 1;
-- Resultado: 1|Rock Paulista dos Anos 80|FECHADO
```

## 📋 Endpoints Disponíveis

### CRUD Básico
- `GET /api/v1/space-festival-types/` - Listar todos
- `GET /api/v1/space-festival-types/{id}` - Obter por ID
- `POST /api/v1/space-festival-types/` - Criar novo
- `PUT /api/v1/space-festival-types/{id}` - Atualizar completo
- `DELETE /api/v1/space-festival-types/{id}` - Deletar

### Endpoints Específicos
- `PATCH /api/v1/space-festival-types/{id}/status` - **NOVO**: Atualizar apenas status
- `GET /api/v1/space-festival-types/space/{space_id}` - Por espaço
- `GET /api/v1/space-festival-types/festival-type/{festival_type_id}` - Por tipo de festival
- `GET /api/v1/space-festival-types/space/{space_id}/festival-type/{festival_type_id}` - Combinação específica

## 🔧 Exemplos de Uso

### 1. Criar Festival com Status
```bash
curl -X POST "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "festival_type_id": 1,
    "tema": "Festival de Jazz",
    "descricao": "Festival de jazz com artistas renomados",
    "status": "CONTRATANDO",
    "data": "2025-08-15T20:00:00",
    "horario": "20:00"
  }'
```

### 2. Atualizar Status
```bash
curl -X PATCH "http://localhost:8000/api/v1/space-festival-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "FECHADO"}'
```

### 3. Atualizar Festival Completo
```bash
curl -X PUT "http://localhost:8000/api/v1/space-festival-types/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tema": "Festival de Jazz Atualizado",
    "status": "SUSPENSO",
    "data": "2025-09-15T20:00:00"
  }'
```

## ✅ Validações Implementadas

### 1. Validação de Enum
- Verificação se o status é um valor válido do enum
- Mensagem de erro clara para valores inválidos

### 2. Validação de Campos Obrigatórios
- `space_id`: Deve ser maior que zero
- `festival_type_id`: Deve ser maior que zero
- `tema`: Não pode estar vazio
- `descricao`: Não pode estar vazio
- `horario`: Não pode estar vazio

### 3. Validação de Relacionamentos
- Verificação se o espaço existe
- Verificação se o tipo de festival existe

## 🔄 Consistência com Space Event Types

A implementação segue exatamente o mesmo padrão estabelecido para `SpaceEventType`:

- ✅ **Mesmo enum**: StatusEventType vs StatusFestivalType
- ✅ **Mesmos valores**: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
- ✅ **Mesma estrutura**: Entidade, modelo, schema, repositório, serviço, endpoint
- ✅ **Mesmo endpoint**: PATCH /{id}/status
- ✅ **Mesmas validações**: Enum, campos obrigatórios, relacionamentos
- ✅ **Mesma migração**: Alembic com server_default

## 📈 Próximos Passos

1. **Verificação de Consistência**: Verificar se todos os endpoints relacionados (reviews, interests, bookings) lidam corretamente com o campo status
2. **Documentação**: Atualizar API_USAGE.md e outras documentações
3. **Testes**: Implementar testes unitários e de integração
4. **Validações Adicionais**: Considerar regras de negócio específicas para cada status

## 🎉 Conclusão

A implementação do campo `status` em `SpaceFestivalType` foi concluída com sucesso, seguindo os padrões estabelecidos e mantendo consistência total com a implementação anterior em `SpaceEventType`. Todos os endpoints estão funcionando corretamente e o sistema está pronto para uso. 