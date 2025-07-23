# Guia de Uso da API

- [Sistema de Agendamentos (Bookings)](#sistema-de-agendamentos-bookings)

## Endpoints de Autenticação

### 1. Registro de Usuário
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
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
curl -X POST "http://localhost:8000/api/v1/auth/login" \
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
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
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

**🆕 Novo:** Todos os endpoints de consulta suportam o parâmetro `include_relations=true` para obter dados relacionados (profile, space, artist, etc.) em uma única requisição.

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
# Listar todos os agendamentos (opcional: ?include_relations=true)
GET /api/v1/bookings/
Authorization: Bearer {token}

# Obter agendamento por ID (opcional: ?include_relations=true)
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
# Agendamentos por profile (opcional: ?include_relations=true)
GET /api/v1/bookings/profile/{profile_id}
Authorization: Bearer {token}

# Agendamentos por espaço (opcional: ?include_relations=true)
GET /api/v1/bookings/space/{space_id}
Authorization: Bearer {token}

# Agendamentos por artista (opcional: ?include_relations=true)
GET /api/v1/bookings/artist/{artist_id}
Authorization: Bearer {token}

# Agendamentos por evento específico (opcional: ?include_relations=true)
GET /api/v1/bookings/space-event-type/{space_event_type_id}
Authorization: Bearer {token}

# Agendamentos por festival específico (opcional: ?include_relations=true)
GET /api/v1/bookings/space-festival-type/{space_festival_type_id}
Authorization: Bearer {token}

# Agendamentos por período (opcional: &include_relations=true)
GET /api/v1/bookings/date-range?data_inicio=2025-01-01T00:00:00&data_fim=2025-01-31T23:59:59
Authorization: Bearer {token}
```

### Parâmetro `include_relations`

Todos os endpoints de consulta (GET) do sistema de bookings suportam o parâmetro opcional `include_relations` para incluir dados relacionados na resposta.

#### Como Usar
```bash
# Sem relacionamentos (padrão)
GET /api/v1/bookings/?include_relations=false

# Com relacionamentos
GET /api/v1/bookings/?include_relations=true

# Funciona em todos os endpoints de consulta:
GET /api/v1/bookings/{id}?include_relations=true
GET /api/v1/bookings/profile/{profile_id}?include_relations=true
GET /api/v1/bookings/space/{space_id}?include_relations=true
GET /api/v1/bookings/artist/{artist_id}?include_relations=true
GET /api/v1/bookings/space-event-type/{space_event_type_id}?include_relations=true
GET /api/v1/bookings/space-festival-type/{space_festival_type_id}?include_relations=true
GET /api/v1/bookings/date-range?data_inicio=...&data_fim=...&include_relations=true
```

#### Comparação de Respostas

**Sem relacionamentos (`include_relations=false`):**
```json
{
  "profile_id": 2,
  "data_inicio": "2025-08-22T20:00:00.565377",
  "horario_inicio": "20:00",
  "data_fim": "2025-08-22T23:00:00.565377",
  "horario_fim": "23:00",
  "space_id": 1,
  "artist_id": null,
  "space_event_type_id": null,
  "space_festival_type_id": null,
  "id": 1,
  "created_at": "2025-07-23T16:09:30",
  "updated_at": "2025-07-23T16:09:30"
}
```

**Com relacionamentos (`include_relations=true`):**
```json
{
  "profile_id": 2,
  "data_inicio": "2025-08-22T20:00:00.565377",
  "horario_inicio": "20:00",
  "data_fim": "2025-08-22T23:00:00.565377",
  "horario_fim": "23:00",
  "space_id": 1,
  "artist_id": null,
  "space_event_type_id": null,
  "space_festival_type_id": null,
  "id": 1,
  "created_at": "2025-07-23T16:09:30",
  "updated_at": "2025-07-23T16:09:30",
  "profile": {
    "role_id": 2,
    "full_name": "Bruno Souza",
    "artistic_name": "Bruno Show",
    "bio": "Cantor sertanejo.",
    "cep": "02002-000",
    "logradouro": "Av. Brasil",
    "numero": "200",
    "complemento": "Casa",
    "cidade": "Campinas",
    "uf": "SP",
    "telefone_fixo": "(19) 3333-2222",
    "telefone_movel": "(19) 99999-2222",
    "whatsapp": "(19) 99999-2222",
    "id": 2,
    "created_at": "2025-07-23T02:43:09",
    "updated_at": "2025-07-23T02:43:09"
  },
  "space": {
    "profile_id": 4,
    "nome": "Bar do Centro",
    "descricao": "Bar tradicional no centro da cidade com música ao vivo.",
    "cep": "04004-000",
    "logradouro": "Rua XV de Novembro",
    "numero": "150",
    "complemento": "Térreo",
    "cidade": "São Paulo",
    "uf": "SP",
    "acesso": "Público",
    "dias_apresentacao": ["sexta", "sábado"],
    "duracao_apresentacao": 3.0,
    "valor_hora": 150.0,
    "valor_couvert": 20.0,
    "requisitos_minimos": "Equipamento de som básico, microfone, instrumentos próprios",
    "oferecimentos": "Equipamento de som, iluminação, camarim, bebidas",
    "estrutura_apresentacao": "Palco de 4x3 metros, sistema de som profissional, iluminação cênica",
    "publico_estimado": "101-500",
    "fotos_ambiente": ["/fotos/bar1.jpg", "/fotos/bar2.jpg"],
    "instagram": "https://instagram.com/bar_exemplo",
    "tiktok": "https://tiktok.com/@bar_exemplo",
    "youtube": null,
    "facebook": "https://facebook.com/barexemplo",
    "id": 1,
    "created_at": "2025-07-23T02:37:10",
    "updated_at": "2025-07-23T02:37:10"
  },
  "artist": null,
  "space_event_type": null,
  "space_festival_type": null
}
```

#### Relacionamentos Incluídos
- **profile:** Dados completos do perfil que fez o agendamento
- **space:** Dados do espaço (quando `space_id` não for nulo)
- **artist:** Dados do artista (quando `artist_id` não for nulo)
- **space_event_type:** Dados do evento específico (quando `space_event_type_id` não for nulo)
- **space_festival_type:** Dados do festival específico (quando `space_festival_type_id` não for nulo)

#### Vantagens do `include_relations=true`
- **Reduz chamadas à API:** Uma única requisição traz todos os dados necessários
- **Performance otimizada:** Usa JOINs do banco de dados para carregar dados relacionados
- **Informações completas:** Evita necessidade de fazer múltiplas consultas para obter dados relacionados
- **Ideal para interfaces:** Frontend recebe todos os dados para exibição em uma única requisição

#### Considerações de Performance
- **Use `include_relations=true`** quando precisar dos dados relacionados imediatamente
- **Use `include_relations=false`** (padrão) quando precisar apenas dos IDs dos relacionamentos
- **Para listas grandes:** Considere usar paginação junto com `include_relations=false` para melhor performance
- **Dados mais pesados:** Com relacionamentos, cada item da resposta será significativamente maior

### Exemplos de Uso

#### Exemplos com `include_relations`

##### Listar todos os bookings com relacionamentos:
```bash
curl -X GET "http://localhost:8000/api/v1/bookings/?include_relations=true" \
  -H "Authorization: Bearer {token}"
```

##### Obter booking específico com relacionamentos:
```bash
curl -X GET "http://localhost:8000/api/v1/bookings/1?include_relations=true" \
  -H "Authorization: Bearer {token}"
```

##### Bookings por profile com relacionamentos:
```bash
curl -X GET "http://localhost:8000/api/v1/bookings/profile/2?include_relations=true" \
  -H "Authorization: Bearer {token}"
```

##### Bookings por espaço com relacionamentos:
```bash
curl -X GET "http://localhost:8000/api/v1/bookings/space/1?include_relations=true" \
  -H "Authorization: Bearer {token}"
```

##### Bookings por período com relacionamentos:
```bash
curl -X GET "http://localhost:8000/api/v1/bookings/date-range?data_inicio=2025-08-01T00:00:00&data_fim=2025-09-30T23:59:59&include_relations=true" \
  -H "Authorization: Bearer {token}"
```

#### Exemplos de Criação de Bookings

#### 1. Artista Agendando Espaço
```bash
curl -X POST "http://localhost:8000/api/v1/bookings/" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 2,
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

#### Regras de Negócio por Role
- **ADMIN (role_id = 1):** NUNCA pode fazer agendamentos
- **ARTISTA (role_id = 2):** NUNCA pode agendar artistas (artist_id), apenas espaços, eventos ou festivais
- **ESPAÇO (role_id = 3):** NUNCA pode agendar espaços (space_id), apenas artistas, eventos ou festivais

#### Regras Gerais
- **Relacionamento único:** Apenas um dos campos (space_id, artist_id, space_event_type_id, space_festival_type_id) pode estar preenchido
- **Data fim posterior:** Data/hora de fim deve ser posterior à data/hora de início
- **Profile obrigatório:** Todo agendamento deve estar vinculado a um profile
- **Foreign keys válidas:** IDs referenciados devem existir no banco de dados

#### Respostas de Erro
```json
// ADMIN tentando fazer agendamento
{
  "detail": "Usuários com role ADMIN não podem fazer agendamentos"
}

// ARTISTA tentando agendar outro artista
{
  "detail": "Usuários com role ARTISTA não podem agendar artistas, apenas espaços"
}

// ESPAÇO tentando agendar outro espaço
{
  "detail": "Usuários com role ESPACO não podem agendar espaços, apenas artistas"
}

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

## 🧪 Teste Rápido da Funcionalidade `include_relations`

### Exemplo Prático
```bash
# 1. Fazer login e obter token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@example.com", "password": "senha123"}' | \
  jq -r '.access_token')

# 2. Testar sem relacionamentos (resposta pequena)
curl -X GET "http://localhost:8000/api/v1/bookings/1?include_relations=false" \
  -H "Authorization: Bearer $TOKEN" | jq

# 3. Testar com relacionamentos (resposta completa)  
curl -X GET "http://localhost:8000/api/v1/bookings/1?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Comparar tamanhos das respostas
echo "Sem relacionamentos:"
curl -s -X GET "http://localhost:8000/api/v1/bookings/1?include_relations=false" \
  -H "Authorization: Bearer $TOKEN" | wc -c

echo "Com relacionamentos:"
curl -s -X GET "http://localhost:8000/api/v1/bookings/1?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | wc -c
```

### Resultado Esperado
- **Sem relacionamentos:** ~300 bytes, apenas IDs dos relacionamentos
- **Com relacionamentos:** ~1500+ bytes, dados completos de profile, space, artist, etc.
- **Campos extras incluídos:** `profile`, `space`, `artist`, `space_event_type`, `space_festival_type`

---

## 🔧 Configuração de Desenvolvimento

```API_USAGE.md