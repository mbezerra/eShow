# Guia de Uso da API

- [Sistema de Agendamentos (Bookings)](#sistema-de-agendamentos-bookings)

## Endpoints de Autenticação

### 1. Registro de Usuário
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123",
    "is_active": true
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Renovar Token
```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## Sistema de Agendamentos (Bookings)

### Visão Geral
O sistema de bookings permite gerenciar agendamentos/reservas com 4 tipos diferentes:
1. **Agendamento de Espaço:** Artista reserva espaço para apresentação
2. **Agendamento de Artista:** Espaço contrata artista para evento  
3. **Agendamento para Evento:** Vinculado a um space-event-type específico
4. **Agendamento para Festival:** Vinculado a um space-festival-type específico

### Estrutura do Agendamento
```json
{
  "id": 1,
  "profile_id": 1,
  "data_inicio": "2025-05-15T19:00:00",
  "horario_inicio": "19:00",
  "data_fim": "2025-05-15T23:00:00", 
  "horario_fim": "23:00",
  "space_id": 1,
  "artist_id": null,
  "space_event_type_id": null,
  "space_festival_type_id": null,
  "created_at": "2025-07-23T14:16:15",
  "updated_at": "2025-07-23T14:16:15"
}
```

### Endpoints Disponíveis

#### CRUD Básico
```bash
# Listar todos os agendamentos
GET /api/v1/bookings/
Authorization: Bearer {token}

# Obter agendamento por ID
GET /api/v1/bookings/{id}
Authorization: Bearer {token}

# Criar novo agendamento
POST /api/v1/bookings/
Authorization: Bearer {token}
Content-Type: application/json
{
  "profile_id": 1,
  "data_inicio": "2025-05-15T19:00:00",
  "horario_inicio": "19:00",
  "data_fim": "2025-05-15T23:00:00",
  "horario_fim": "23:00",
  "space_id": 1,
  "artist_id": null,
  "space_event_type_id": null,
  "space_festival_type_id": null
}

# Atualizar agendamento
PUT /api/v1/bookings/{id}
Authorization: Bearer {token}
Content-Type: application/json
{
  "horario_inicio": "20:00",
  "horario_fim": "00:00"
}

# Deletar agendamento
DELETE /api/v1/bookings/{id}
Authorization: Bearer {token}
```

#### Filtros Especializados
```bash
# Agendamentos por profile
GET /api/v1/bookings/profile/{profile_id}
Authorization: Bearer {token}

# Agendamentos por espaço
GET /api/v1/bookings/space/{space_id}
Authorization: Bearer {token}

# Agendamentos por artista
GET /api/v1/bookings/artist/{artist_id}
Authorization: Bearer {token}

# Agendamentos por evento específico
GET /api/v1/bookings/space-event-type/{space_event_type_id}
Authorization: Bearer {token}

# Agendamentos por festival específico
GET /api/v1/bookings/space-festival-type/{space_festival_type_id}
Authorization: Bearer {token}

# Agendamentos por período
GET /api/v1/bookings/date-range?data_inicio=2025-01-01T00:00:00&data_fim=2025-01-31T23:59:59
Authorization: Bearer {token}
```

### Exemplos de Uso

#### 1. Artista Agendando Espaço
```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "data_inicio": "2025-05-15T19:00:00",
    "horario_inicio": "19:00",
    "data_fim": "2025-05-15T23:00:00",
    "horario_fim": "23:00",
    "space_id": 1,
    "artist_id": null,
    "space_event_type_id": null,
    "space_festival_type_id": null
  }'
```

#### 2. Espaço Contratando Artista
```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 2,
    "data_inicio": "2025-06-10T21:00:00",
    "horario_inicio": "21:00",
    "data_fim": "2025-06-11T02:00:00",
    "horario_fim": "02:00",
    "space_id": null,
    "artist_id": 1,
    "space_event_type_id": null,
    "space_festival_type_id": null
  }'
```

#### 3. Agendamento para Evento Específico
```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 3,
    "data_inicio": "2025-07-20T18:00:00",
    "horario_inicio": "18:00",
    "data_fim": "2025-07-21T01:00:00",
    "horario_fim": "01:00",
    "space_id": null,
    "artist_id": null,
    "space_event_type_id": 3,
    "space_festival_type_id": null
  }'
```

#### 4. Agendamento para Festival Específico
```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 4,
    "data_inicio": "2025-08-15T16:00:00",
    "horario_inicio": "16:00",
    "data_fim": "2025-08-16T04:00:00",
    "horario_fim": "04:00",
    "space_id": null,
    "artist_id": null,
    "space_event_type_id": null,
    "space_festival_type_id": 6
  }'
```

### Validações Implementadas

#### Regras de Negócio
- **Relacionamento único:** Apenas um dos campos (space_id, artist_id, space_event_type_id, space_festival_type_id) pode estar preenchido
- **Data fim posterior:** Data/hora de fim deve ser posterior à data/hora de início
- **Profile obrigatório:** Todo agendamento deve estar vinculado a um profile
- **Foreign keys válidas:** IDs referenciados devem existir no banco de dados

#### Respostas de Erro
```json
// Múltiplos relacionamentos
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "space_festival_type_id"],
      "msg": "Value error, Apenas um tipo de relacionamento pode ser especificado por booking"
    }
  ]
}

// Data inválida
{
  "detail": [
    {
      "type": "value_error", 
      "loc": ["body", "data_fim"],
      "msg": "Value error, Data de fim deve ser posterior à data de início"
    }
  ]
}
```

---

## 🔧 Configuração de Desenvolvimento

```API_USAGE.md