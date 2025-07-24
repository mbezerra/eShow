# Implementação do Campo Status em Space Event Types

## Resumo das Mudanças

Este documento descreve as implementações realizadas para adicionar o campo `status` na tabela `space_event_types` com os valores enum: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO.

## 1. Enum StatusEventType

**Arquivo:** `domain/entities/space_event_type.py`

- Criado enum `StatusEventType` com os valores:
  - `CONTRATANDO`
  - `FECHADO`
  - `SUSPENSO`
  - `CANCELADO`
- Adicionado campo `status` na entidade `SpaceEventType` com valor padrão `CONTRATANDO`
- Adicionada validação para garantir que o status seja um valor válido do enum

## 2. Modelo de Banco de Dados

**Arquivo:** `infrastructure/database/models/space_event_type_model.py`

- Adicionada coluna `status` do tipo `SQLAlchemyEnum(StatusEventType)`
- Configurada como `nullable=False` com valor padrão `StatusEventType.CONTRATANDO`
- Atualizado método `__repr__` para incluir o status

## 3. Schemas Pydantic

**Arquivo:** `app/schemas/space_event_type.py`

- Adicionado campo `status` em todos os schemas relevantes:
  - `SpaceEventTypeBase`
  - `SpaceEventTypeCreate`
  - `SpaceEventTypeUpdate`
  - `SpaceEventTypeResponse`
- Criado schema específico `SpaceEventTypeStatusUpdate` para atualização de status
- Adicionadas validações para o campo status

## 4. Repositório

**Arquivo:** `domain/repositories/space_event_type_repository.py`
- Adicionado método abstrato `update_status()` na interface

**Arquivo:** `infrastructure/repositories/space_event_type_repository_impl.py`
- Implementado método `update_status()` para atualizar apenas o status
- Atualizado método `create()` para incluir o status
- Atualizado método `update()` para incluir o status
- Atualizado método `_to_entity()` para incluir o status

## 5. Serviço de Aplicação

**Arquivo:** `app/application/services/space_event_type_service.py`
- Adicionado campo `status` no método `create_space_event_type()`
- Adicionado campo `status` no método `update_space_event_type()`
- Criado método `update_space_event_type_status()` para atualização específica de status

## 6. Endpoints da API

**Arquivo:** `app/api/endpoints/space_event_types.py`
- Adicionado campo `status` na função `convert_space_event_type_to_response()`
- Criado novo endpoint `PATCH /{space_event_type_id}/status` para atualização de status
- Endpoint requer autenticação e retorna o objeto atualizado

## 7. Migração do Banco de Dados

**Arquivo:** `alembic/versions/131c5fdf2f57_adicionar_coluna_status_em_space_event_.py`
- Criada migração para adicionar a coluna `status`
- Configurada para SQLite com valor padrão

## 8. Script de Inicialização

**Arquivo:** `init_space_event_types.py`
- Atualizado para incluir o campo `status` nos dados de inicialização
- Adicionados diferentes status para demonstrar a funcionalidade

## 9. Script de Teste

**Arquivo:** `test_status_endpoint.py`
- Criado script para testar o novo endpoint de atualização de status
- Inclui teste dos valores do enum

## Novos Endpoints Disponíveis

### Atualizar Status
```
PATCH /api/space-event-types/{space_event_type_id}/status
```

**Body:**
```json
{
  "status": "FECHADO"
}
```

**Resposta:**
```json
{
  "id": 1,
  "space_id": 1,
  "event_type_id": 1,
  "tema": "Evento Teste",
  "descricao": "Descrição do evento",
  "status": "FECHADO",
  "link_divulgacao": "https://example.com",
  "banner": "/static/banner.jpg",
  "data": "2024-01-01T20:00:00",
  "horario": "20:00",
  "created_at": "2024-01-01T10:00:00"
}
```

## Valores de Status Disponíveis

- `CONTRATANDO` - Evento em processo de contratação
- `FECHADO` - Evento confirmado e fechado
- `SUSPENSO` - Evento temporariamente suspenso
- `CANCELADO` - Evento cancelado

## Como Testar

1. Execute o script de inicialização:
   ```bash
   python init_space_event_types.py
   ```

2. Inicie a API:
   ```bash
   python run.py
   ```

3. Teste o endpoint de atualização de status:
   ```bash
   python test_status_endpoint.py
   ```

## Compatibilidade

- Todos os endpoints existentes foram atualizados para lidar com o novo campo `status`
- Registros existentes foram atualizados com o status padrão `CONTRATANDO`
- A implementação é compatível com SQLite e pode ser facilmente adaptada para PostgreSQL 