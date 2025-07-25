# Guia de Uso da API

- [Sistema de Perfis (Profiles)](#sistema-de-perfis-profiles)
- [Sistema de Agendamentos (Bookings)](#sistema-de-agendamentos-bookings)
- [Sistema de Avaliações/Reviews](#sistema-de-avaliaçõesreviews)
- [Sistema de Manifestações de Interesse (Interests)](#sistema-de-manifestações-de-interesse-interests)
- [Sistema de Space Event Types](#sistema-de-space-event-types)
- [Sistema de Space Festival Types](#sistema-de-space-festival-types)
- [Sistema Financeiro/Bancário (Financials)](#-financial---dados-financeirosbancários)
- [Sistema de Busca por Localização](#sistema-de-busca-por-localização)

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

## Sistema de Perfis (Profiles)

### Visão Geral
O sistema de perfis gerencia as informações pessoais e profissionais dos usuários, incluindo dados de localização com coordenadas geográficas (latitude e longitude) para facilitar buscas por proximidade.

**🆕 Novo:** Campos `latitude` e `longitude` opcionais para localização geográfica precisa.

### Estrutura do Perfil
```json
{
  "id": 1,
  "user_id": 1,
  "role_id": 2,
  "full_name": "João Silva",
  "artistic_name": "João Artista",
  "bio": "Músico profissional com experiência em diversos estilos",
  "cep": "01234-567",
  "logradouro": "Rua das Flores",
  "numero": "123",
  "complemento": "Apto 1",
  "cidade": "São Paulo",
  "uf": "SP",
  "telefone_fixo": "(11) 3333-1111",
  "telefone_movel": "(11) 99999-1111",
  "whatsapp": "(11) 99999-1111",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "created_at": "2025-07-23T14:16:15",
  "updated_at": "2025-07-23T14:16:15"
}
```

### Endpoints Disponíveis

#### CRUD Básico
```bash
# Listar todos os perfis
GET /api/v1/profiles/
Authorization: Bearer {token}

# Obter perfil por ID
GET /api/v1/profiles/{id}
Authorization: Bearer {token}

# Criar novo perfil
POST /api/v1/profiles/
Authorization: Bearer {token}
Content-Type: application/json
{
  "role_id": 2,
  "full_name": "João Silva",
  "artistic_name": "João Artista",
  "bio": "Músico profissional com experiência em diversos estilos",
  "cep": "01234-567",
  "logradouro": "Rua das Flores",
  "numero": "123",
  "complemento": "Apto 1",
  "cidade": "São Paulo",
  "uf": "SP",
  "telefone_fixo": "(11) 3333-1111",
  "telefone_movel": "(11) 99999-1111",
  "whatsapp": "(11) 99999-1111",
  "latitude": -23.5505,
  "longitude": -46.6333
}

# Atualizar perfil
PUT /api/v1/profiles/{id}
Authorization: Bearer {token}
Content-Type: application/json
{
  "artistic_name": "João Artista Atualizado",
  "bio": "Bio atualizada com mais informações",
  "latitude": -23.5631,
  "longitude": -46.6544
}

# Deletar perfil
DELETE /api/v1/profiles/{id}
Authorization: Bearer {token}
```

#### Filtros Especializados
```bash
# Perfis por role (tipo de usuário)
GET /api/v1/profiles/role/{role_id}
Authorization: Bearer {token}

# Perfil por usuário
GET /api/v1/profiles/user/{user_id}
Authorization: Bearer {token}
```

### Campos de Localização Geográfica

#### Latitude e Longitude
- **Tipo:** `float` (opcional)
- **Formato:** Coordenadas decimais (ex: -23.5505, -46.6333)
- **Uso:** Para cálculos de distância e busca por proximidade
- **Validação:** Valores válidos entre -90 e 90 para latitude, -180 e 180 para longitude

#### Exemplo de Uso com Coordenadas
```bash
# Criar perfil com coordenadas
curl -X POST "http://localhost:8000/api/v1/profiles/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "full_name": "Maria Santos",
    "artistic_name": "Maria Cantora",
    "bio": "Cantora de MPB e bossa nova",
    "cep": "20000-000",
    "logradouro": "Av. Rio Branco",
    "numero": "100",
    "cidade": "Rio de Janeiro",
    "uf": "RJ",
    "telefone_movel": "(21) 99999-9999",
    "latitude": -22.9068,
    "longitude": -43.1729
  }'

# Atualizar coordenadas de um perfil existente
curl -X PUT "http://localhost:8000/api/v1/profiles/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -23.5631,
    "longitude": -46.6544
  }'
```

### Regras de Negócio

#### Campos Obrigatórios
- `role_id`: ID do tipo de usuário (1=ADMIN, 2=ARTISTA, 3=ESPAÇO)
- `full_name`: Nome completo ou razão social
- `artistic_name`: Nome artístico ou nome de fantasia
- `bio`: Apresentação/biografia
- `cep`: CEP válido (8-10 caracteres)
- `logradouro`: Endereço
- `numero`: Número do endereço
- `cidade`: Cidade
- `uf`: Estado (2 caracteres)
- `telefone_movel`: Telefone móvel

#### Campos Opcionais
- `user_id`: ID do usuário associado
- `complemento`: Complemento do endereço
- `telefone_fixo`: Telefone fixo
- `whatsapp`: WhatsApp
- `latitude`: Coordenada de latitude
- `longitude`: Coordenada de longitude

#### Validações
- **CEP:** Entre 8 e 10 caracteres
- **UF:** Exatamente 2 caracteres
- **Telefones:** Máximo 20 caracteres
- **Latitude:** Entre -90 e 90
- **Longitude:** Entre -180 e 180
- **Bio:** Mínimo 1 caractere
- **Nomes:** Máximo 255 caracteres

### Exemplo Prático: Gerenciar Perfil Completo

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@eshow.com", "password": "admin123"}' | jq -r '.access_token')

# 2. Criar perfil com coordenadas
curl -X POST "http://localhost:8000/api/v1/profiles/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "full_name": "Carlos Eduardo",
    "artistic_name": "Carlos Guitarra",
    "bio": "Guitarrista profissional com 15 anos de experiência em rock e blues",
    "cep": "01310-100",
    "logradouro": "Av. Paulista",
    "numero": "1000",
    "complemento": "Apto 45",
    "cidade": "São Paulo",
    "uf": "SP",
    "telefone_fixo": "(11) 3333-4444",
    "telefone_movel": "(11) 99999-4444",
    "whatsapp": "(11) 99999-4444",
    "latitude": -23.5631,
    "longitude": -46.6544
  }' | jq

# 3. Buscar perfil criado
curl -X GET "http://localhost:8000/api/v1/profiles/1" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Atualizar coordenadas
curl -X PUT "http://localhost:8000/api/v1/profiles/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -23.5505,
    "longitude": -46.6333,
    "bio": "Guitarrista profissional com 15 anos de experiência em rock e blues. Especializado em solos improvisados."
  }' | jq

# 5. Listar perfis de artistas
curl -X GET "http://localhost:8000/api/v1/profiles/role/2" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Integração com Sistema de Busca por Localização

Os campos `latitude` e `longitude` dos perfis são utilizados pelo sistema de busca por localização para:

- **Calcular distâncias** entre artistas e espaços
- **Filtrar resultados** por raio de atuação
- **Ordenar resultados** por proximidade
- **Otimizar buscas** geográficas

### Respostas de Erro Comuns

```json
// Coordenadas inválidas
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "latitude"],
      "msg": "Value error, Latitude deve estar entre -90 e 90"
    }
  ]
}

// CEP inválido
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "cep"],
      "msg": "Value error, CEP deve ter entre 8 e 10 caracteres"
    }
  ]
}

// UF inválida
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "uf"],
      "msg": "Value error, UF deve ter exatamente 2 caracteres"
    }
  ]
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

## Sistema de Avaliações/Reviews

### Visão Geral
O sistema de reviews permite criar avaliações com notas de 1 a 5 estrelas para profiles, associadas a eventos ou festivais específicos.

**✅ Funcional:** Todos os endpoints de consulta suportam o parâmetro `include_relations=true` para obter dados relacionados (profile, space_event_type, space_festival_type) em uma única requisição.

### Estrutura da Avaliação
```json
{
  "id": 1,
  "profile_id": 1,
  "space_event_type_id": 3,
  "space_festival_type_id": null,
  "data_hora": "2025-07-23T20:30:00",
  "nota": 5,
  "depoimento": "Excelente apresentação! Muito profissional e pontual.",
  "created_at": "2025-07-23T20:29:31",
  "updated_at": "2025-07-23T20:29:31"
}
```

### Endpoints Disponíveis

#### CRUD Básico
```bash
# Listar todas as avaliações (com dados relacionados: ?include_relations=true)
GET /api/v1/reviews/
Authorization: Bearer {token}

# Obter avaliação por ID (com dados relacionados: ?include_relations=true)
GET /api/v1/reviews/{id}
Authorization: Bearer {token}

# Criar nova avaliação
POST /api/v1/reviews/
Authorization: Bearer {token}
Content-Type: application/json
{
  "space_event_type_id": 3,
  "data_hora": "2025-07-23T20:30:00",
  "nota": 5,
  "depoimento": "Excelente apresentação! Muito profissional e pontual."
}

# Atualizar avaliação
PUT /api/v1/reviews/{id}
Authorization: Bearer {token}
Content-Type: application/json
{
  "nota": 4,
  "depoimento": "Muito boa apresentação, com pequenos pontos de melhoria."
}

# Deletar avaliação
DELETE /api/v1/reviews/{id}
Authorization: Bearer {token}
```

#### Filtros e Estatísticas
```bash
# Avaliações de um profile específico (com dados relacionados: ?include_relations=true)
GET /api/v1/reviews/profile/{profile_id}
Authorization: Bearer {token}

# Média de avaliações de um profile
GET /api/v1/reviews/profile/{profile_id}/average
Authorization: Bearer {token}
# Resposta: {"profile_id": 1, "average_rating": 4.5, "total_reviews": 10}

# Avaliações por nota específica (com dados relacionados: ?include_relations=true)
GET /api/v1/reviews/rating/{nota}
Authorization: Bearer {token}
# Exemplo: /api/v1/reviews/rating/5 (todas as avaliações 5 estrelas)

# Avaliações por tipo de evento (com dados relacionados: ?include_relations=true)
GET /api/v1/reviews/space-event-type/{space_event_type_id}
Authorization: Bearer {token}

# Avaliações por tipo de festival (com dados relacionados: ?include_relations=true)
GET /api/v1/reviews/space-festival-type/{space_festival_type_id}
Authorization: Bearer {token}

# Avaliações por período
GET /api/v1/reviews/date-range/?data_inicio=2025-01-01T00:00:00&data_fim=2025-12-31T23:59:59&include_relations=true
Authorization: Bearer {token}
```

### Regras de Negócio
- **Usuários ADMIN (role_id = 1) NUNCA avaliam ou são avaliados** - Papel apenas administrativo
- **Usuários ARTISTA (role_id = 2) podem criar reviews normalmente**
- **Usuários ESPAÇO (role_id = 3) podem criar reviews normalmente**
- **Profile_id determinado automaticamente** pelo usuário logado (não enviar no request)
- **Notas**: Apenas valores inteiros de 1 a 5
- **Depoimento**: Mínimo 10 caracteres, máximo 1000 caracteres
- **Endpoints DELETE**: Retornam status 200 com mensagem de sucesso
- **Relacionamento exclusivo**: Cada review deve ter OU `space_event_type_id` OU `space_festival_type_id` (nunca ambos)
- **Profile imutável**: O `profile_id` não pode ser alterado após a criação
- **Autenticação obrigatória**: Todos os endpoints requerem token JWT válido

### Exemplo Prático - Criação e Consulta
```bash
# 1. Fazer login e obter token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@eshow.com", "password": "admin123"}' | \
  jq -r '.access_token')

# 2. Criar uma nova avaliação
curl -X POST "http://localhost:8000/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 1,
    "space_event_type_id": 3,
    "data_hora": "2025-07-23T20:30:00",
    "nota": 5,
    "depoimento": "Apresentação excepcional! Superou todas as expectativas."
  }'

# 3. Consultar avaliações de um profile com relacionamentos
curl -X GET "http://localhost:8000/api/v1/reviews/profile/1?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Obter média de avaliações
curl -X GET "http://localhost:8000/api/v1/reviews/profile/1/average" \
  -H "Authorization: Bearer $TOKEN" | jq

# 5. Filtrar avaliações 5 estrelas
curl -X GET "http://localhost:8000/api/v1/reviews/rating/5" \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## Sistema de Manifestações de Interesse (Interests)

### Visão Geral
O sistema de **Interests** permite que artistas manifestem interesse em se apresentar em espaços específicos e vice-versa, facilitando a conexão entre profissionais e estabelecimentos.

**🆕 Novo:** Todos os endpoints de consulta suportam o parâmetro `include_relations=true` para obter dados relacionados (profile_interessado, profile_interesse, space_event_type, space_festival_type) em uma única requisição.

### Estrutura da Manifestação de Interesse
```json
{
  "id": 1,
  "profile_id_interessado": 2,
  "profile_id_interesse": 3,
  "data_inicial": "2025-08-07",
  "horario_inicial": "18:00",
  "duracao_apresentacao": 2.5,
  "valor_hora_ofertado": 150.0,
  "valor_couvert_ofertado": 20.0,
  "mensagem": "Gostaria de manifestar interesse em uma apresentação no seu espaço. Tenho experiência com o público do local.",
  "status": "AGUARDANDO_CONFIRMACAO",
  "resposta": null,
  "space_event_type_id": 3,
  "space_festival_type_id": null,
  "created_at": "2025-07-23T20:30:00",
  "updated_at": "2025-07-23T20:30:00"
}
```

### Endpoints Disponíveis

#### CRUD Básico
```bash
# Listar todas as manifestações (opcional: ?include_relations=true)
GET /api/v1/interests/
Authorization: Bearer {token}

# Obter manifestação por ID (opcional: ?include_relations=true)
GET /api/v1/interests/{id}
Authorization: Bearer {token}

# Criar nova manifestação de interesse
POST /api/v1/interests/
Authorization: Bearer {token}
Content-Type: application/json
{
  "profile_id_interessado": 2,
  "profile_id_interesse": 3,
  "data_inicial": "2025-08-07",
  "horario_inicial": "18:00",
  "duracao_apresentacao": 2.5,
  "valor_hora_ofertado": 150.0,
  "valor_couvert_ofertado": 20.0,
  "mensagem": "Gostaria de manifestar interesse em uma apresentação no seu espaço.",
  "space_event_type_id": 3
}

# Atualizar manifestação completa
PUT /api/v1/interests/{id}
Authorization: Bearer {token}
Content-Type: application/json
{
  "duracao_apresentacao": 3.0,
  "valor_hora_ofertado": 180.0,
  "mensagem": "Atualizando proposta com nova duração e valor."
}

# Deletar manifestação
DELETE /api/v1/interests/{id}
Authorization: Bearer {token}
```

#### Gestão de Status
```bash
# Atualizar status da manifestação
PATCH /api/v1/interests/{id}/status
Authorization: Bearer {token}
Content-Type: application/json
{
  "status": "ACEITO",
  "resposta": "Aceito! Vamos combinar os detalhes da apresentação."
}

# Aceitar manifestação de interesse
PATCH /api/v1/interests/{id}/accept?resposta=Resposta%20opcional
Authorization: Bearer {token}

# Recusar manifestação de interesse
PATCH /api/v1/interests/{id}/reject?resposta=Motivo%20da%20recusa
Authorization: Bearer {token}
```

#### Consultas por Profile
```bash
# Manifestações enviadas por um profile (opcional: ?include_relations=true)
GET /api/v1/interests/profile/interessado/{profile_id}
Authorization: Bearer {token}

# Manifestações recebidas por um profile (opcional: ?include_relations=true)
GET /api/v1/interests/profile/interesse/{profile_id}
Authorization: Bearer {token}

# Manifestações pendentes de um profile (opcional: ?include_relations=true)
GET /api/v1/interests/profile/{profile_id}/pending
Authorization: Bearer {token}

# Estatísticas de manifestações por profile
GET /api/v1/interests/profile/{profile_id}/statistics
Authorization: Bearer {token}
# Resposta: {"total_manifestado": 5, "total_recebido": 3, "pendentes_enviadas": 2, "pendentes_recebidas": 1}
```

#### Filtros Avançados
```bash
# Filtrar manifestações por status (opcional: ?include_relations=true)
GET /api/v1/interests/status/AGUARDANDO_CONFIRMACAO
Authorization: Bearer {token}

# Manifestações por tipo de evento (opcional: ?include_relations=true)
GET /api/v1/interests/space-event-type/{space_event_type_id}
Authorization: Bearer {token}

# Manifestações por período (opcional: &include_relations=true)
GET /api/v1/interests/date-range/?data_inicio=2025-01-01&data_fim=2025-12-31
Authorization: Bearer {token}
```

### Parâmetro `include_relations`

Todos os endpoints de consulta (GET) do sistema de interests suportam o parâmetro opcional `include_relations` para incluir dados relacionados na resposta.

#### Como Usar
```bash
# Sem relacionamentos (padrão)
GET /api/v1/interests/?include_relations=false

# Com relacionamentos
GET /api/v1/interests/?include_relations=true

# Funciona em todos os endpoints de consulta:
GET /api/v1/interests/{id}?include_relations=true
GET /api/v1/interests/profile/interessado/{profile_id}?include_relations=true
GET /api/v1/interests/profile/interesse/{profile_id}?include_relations=true
GET /api/v1/interests/profile/{profile_id}/pending?include_relations=true
GET /api/v1/interests/status/{status}?include_relations=true
GET /api/v1/interests/space-event-type/{space_event_type_id}?include_relations=true
GET /api/v1/interests/date-range?data_inicio=...&data_fim=...&include_relations=true
```

#### Comparação de Respostas

**Sem relacionamentos (`include_relations=false`):**
```json
{
  "profile_id_interessado": 2,
  "profile_id_interesse": 3,
  "data_inicial": "2025-08-07",
  "horario_inicial": "18:00",
  "duracao_apresentacao": 2.5,
  "valor_hora_ofertado": 150.0,
  "valor_couvert_ofertado": 20.0,
  "mensagem": "Gostaria de manifestar interesse...",
  "status": "AGUARDANDO_CONFIRMACAO",
  "resposta": null,
  "space_event_type_id": 3,
  "space_festival_type_id": null,
  "id": 1,
  "created_at": "2025-07-23T20:30:00",
  "updated_at": "2025-07-23T20:30:00"
}
```

**Com relacionamentos (`include_relations=true`):**
```json
{
  "profile_id_interessado": 2,
  "profile_id_interesse": 3,
  "data_inicial": "2025-08-07",
  "horario_inicial": "18:00",
  "duracao_apresentacao": 2.5,
  "valor_hora_ofertado": 150.0,
  "valor_couvert_ofertado": 20.0,
  "mensagem": "Gostaria de manifestar interesse...",
  "status": "AGUARDANDO_CONFIRMACAO",
  "resposta": null,
  "space_event_type_id": 3,
  "space_festival_type_id": null,
  "id": 1,
  "created_at": "2025-07-23T20:30:00",
  "updated_at": "2025-07-23T20:30:00",
  "profile_interessado": {
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
  "profile_interesse": {
    "role_id": 3,
    "full_name": "Carla Lima",
    "artistic_name": null,
    "bio": "Espaço para eventos musicais.",
    "cep": "06006-000",
    "logradouro": "Rua das Flores",
    "numero": "300",
    "complemento": "Sala 101",
    "cidade": "São Paulo",
    "uf": "SP",
    "telefone_fixo": "(11) 4444-3333",
    "telefone_movel": "(11) 88888-3333",
    "whatsapp": "(11) 88888-3333",
    "id": 3,
    "created_at": "2025-07-23T02:43:09",
    "updated_at": "2025-07-23T02:43:09"
  },
  "space_event_type": {
    "space_id": 1,
    "event_type_id": 3,
    "banner_url": "/banners/evento_aniversario.jpg",
    "descricao": "Evento de aniversário com música ao vivo",
    "id": 3,
    "created_at": "2025-07-23T02:37:10",
    "updated_at": "2025-07-23T02:37:10"
  },
  "space_festival_type": null
}
```

#### Relacionamentos Incluídos
- **profile_interessado:** Dados completos do profile que manifestou interesse
- **profile_interesse:** Dados completos do profile que recebeu a manifestação
- **space_event_type:** Dados do evento específico (quando `space_event_type_id` não for nulo)
- **space_festival_type:** Dados do festival específico (quando `space_festival_type_id` não for nulo)

### Regras de Negócio
- **Validação de roles:** Apenas **artistas** podem manifestar interesse em **espaços** e vice-versa
- **Prevenção de duplicatas:** Não é possível manifestar interesse duplicado entre os mesmos profiles
- **Estados de status:** "AGUARDANDO_CONFIRMACAO" (padrão), "ACEITO", "RECUSADO"
- **Validação de data:** Data inicial deve ser futura
- **Validação de duração:** Entre 0.5 e 8 horas
- **Validação de valores:** Valores monetários devem ser positivos
- **Mensagem obrigatória:** Entre 10 e 1000 caracteres
- **Profile_id imutável:** Os IDs de profile não podem ser alterados após criação
- **Relacionamento opcional:** Evento OU festival OU nenhum (nunca ambos)

### Exemplo Prático - Fluxo Completo

```bash
# 1. Fazer login e obter token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@eshow.com", "password": "admin123"}' | \
  jq -r '.access_token')

# 2. Artista manifesta interesse em espaço
curl -X POST "http://localhost:8000/api/v1/interests/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id_interessado": 2,
    "profile_id_interesse": 3,
    "data_inicial": "2025-08-15",
    "horario_inicial": "20:00",
    "duracao_apresentacao": 3.0,
    "valor_hora_ofertado": 200.0,
    "valor_couvert_ofertado": 25.0,
    "mensagem": "Gostaria de manifestar interesse em uma apresentação no seu espaço. Tenho experiência com o público do local e posso oferecer um repertório variado.",
    "space_event_type_id": 3
  }' | jq

# 3. Consultar manifestações pendentes do espaço
curl -X GET "http://localhost:8000/api/v1/interests/profile/3/pending?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Espaço aceita a manifestação
curl -X PATCH "http://localhost:8000/api/v1/interests/1/accept?resposta=Aceito!%20Vamos%20combinar%20os%20detalhes%20da%20apresentação." \
  -H "Authorization: Bearer $TOKEN" | jq

# 5. Consultar estatísticas do artista
curl -X GET "http://localhost:8000/api/v1/interests/profile/2/statistics" \
  -H "Authorization: Bearer $TOKEN" | jq

# 6. Filtrar manifestações aceitas
curl -X GET "http://localhost:8000/api/v1/interests/status/ACEITO?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Respostas de Erro Comuns

```json
// Tentativa de manifestação duplicada
{
  "detail": "Já existe uma manifestação de interesse entre estes profiles"
}

// Roles incompatíveis
{
  "detail": "Apenas artistas podem manifestar interesse em espaços e vice-versa"
}

// Data no passado
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "data_inicial"],
      "msg": "Value error, Data inicial deve ser futura"
    }
  ]
}

// Duração inválida
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "duracao_apresentacao"],
      "msg": "Value error, Duração deve ser entre 0.5 e 8 horas"
    }
  ]
}

// Mensagem muito curta
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "mensagem"],
      "msg": "Value error, Mensagem deve ter entre 10 e 1000 caracteres"
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

## 💰 Financial - Dados Financeiros/Bancários

**Base URL:** `/api/v1/financials/`  
**Autenticação:** Bearer Token obrigatório

### **Criar Registro Financeiro**

```bash
# POST /api/v1/financials/
curl -X POST "http://localhost:8000/api/v1/financials/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "profile_id": 1,
    "banco": "341",
    "agencia": "1234",
    "conta": "12345-6",
    "tipo_conta": "Corrente",
    "cpf_cnpj": "12345678901",
    "tipo_chave_pix": "CPF",
    "chave_pix": "12345678901",
    "preferencia": "PIX"
  }'
```

### **Buscar por ID**

```bash
# GET /api/v1/financials/{id}
curl -X GET "http://localhost:8000/api/v1/financials/1" \
  -H "Authorization: Bearer $TOKEN"

# Com relacionamentos
curl -X GET "http://localhost:8000/api/v1/financials/1?include_relations=true" \
  -H "Authorization: Bearer $TOKEN"
```

### **Filtros Especializados**

```bash
# Por banco específico
curl -X GET "http://localhost:8000/api/v1/financials/banco/341" \
  -H "Authorization: Bearer $TOKEN"

# Por tipo de conta
curl -X GET "http://localhost:8000/api/v1/financials/tipo-conta/Poupança" \
  -H "Authorization: Bearer $TOKEN"

# Por tipo de chave PIX
curl -X GET "http://localhost:8000/api/v1/financials/tipo-chave-pix/EMAIL" \
  -H "Authorization: Bearer $TOKEN"

# Por chave PIX específica
curl -X GET "http://localhost:8000/api/v1/financials/chave-pix/usuario@example.com" \
  -H "Authorization: Bearer $TOKEN"

# Por preferência de transferência
curl -X GET "http://localhost:8000/api/v1/financials/preferencia/PIX" \
  -H "Authorization: Bearer $TOKEN"

# Por CPF/CNPJ
curl -X GET "http://localhost:8000/api/v1/financials/cpf-cnpj/12345678901" \
  -H "Authorization: Bearer $TOKEN"
```

### **Verificação de Chave PIX**

```bash
# Verificar se chave PIX está disponível
curl -X GET "http://localhost:8000/api/v1/financials/check-chave-pix/nova@chave.com" \
  -H "Authorization: Bearer $TOKEN"

# Verificar excluindo um ID específico (para updates)
curl -X GET "http://localhost:8000/api/v1/financials/check-chave-pix/chave@test.com?exclude_id=1" \
  -H "Authorization: Bearer $TOKEN"
```

### **Estatísticas**

```bash
# Estatísticas por banco
curl -X GET "http://localhost:8000/api/v1/financials/statistics/banks" \
  -H "Authorization: Bearer $TOKEN" | jq

# Estatísticas por tipo de chave PIX
curl -X GET "http://localhost:8000/api/v1/financials/statistics/pix-types" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### **Atualizar Registro**

```bash
# PUT /api/v1/financials/{id}
curl -X PUT "http://localhost:8000/api/v1/financials/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "banco": "237",
    "agencia": "5678",
    "conta": "98765-4",
    "tipo_conta": "Poupança",
    "chave_pix": "novachave@email.com",
    "tipo_chave_pix": "E-mail",
    "preferencia": "TED"
  }'
```

### **Regras de Negócio**

- **Código do banco:** String com 3 dígitos (001 a 999) seguindo padrão brasileiro
- **Chave PIX única:** Não pode haver duplicatas no sistema
- **Validação por tipo:**
  - CPF: 11 dígitos
  - CNPJ: 14 dígitos  
  - Celular: 10 ou 11 dígitos
  - E-mail: Formato válido de email
  - Aleatória: 32-36 caracteres
- **Profile_id imutável:** Não pode ser alterado após criação
- **Tipos de conta:** "Poupança" ou "Corrente"
- **Preferências:** "PIX" ou "TED"

### **Exemplo Prático: Gerenciar Dados Bancários**

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@eshow.com", "password": "admin123"}' | jq -r '.access_token')

# 2. Criar dados financeiros
curl -X POST "http://localhost:8000/api/v1/financials/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "profile_id": 1,
    "banco": "104",
    "agencia": "0001",
    "conta": "12345-6",
    "tipo_conta": "Corrente",
    "cpf_cnpj": "12345678901",
    "tipo_chave_pix": "CPF",
    "chave_pix": "12345678901",
    "preferencia": "PIX"
  }' | jq

# 3. Verificar disponibilidade antes de atualizar
curl -X GET "http://localhost:8000/api/v1/financials/check-chave-pix/novachave@test.com" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Listar por banco
curl -X GET "http://localhost:8000/api/v1/financials/banco/104" \
  -H "Authorization: Bearer $TOKEN" | jq

# 5. Ver estatísticas
curl -X GET "http://localhost:8000/api/v1/financials/statistics/banks" \
  -H "Authorization: Bearer $TOKEN" | jq
```

### **Parâmetro `include_relations`**

```bash
# Comparar resposta com e sem relacionamentos
echo "Sem relacionamentos:"
curl -s -X GET "http://localhost:8000/api/v1/financials/1?include_relations=false" \
  -H "Authorization: Bearer $TOKEN" | jq .profile

echo "Com relacionamentos:"
curl -s -X GET "http://localhost:8000/api/v1/financials/1?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq .profile
```

### **Resultado Esperado**
- **Sem relacionamentos:** `profile: null`
- **Com relacionamentos:** Objeto profile completo com name, email, address, etc.
- **Campos extras incluídos:** `profile` (dados completos do profile associado)

---

## Sistema de Space Event Types

### Visão Geral
O sistema de Space Event Types gerencia relacionamentos N:N entre espaços e tipos de eventos, permitindo que espaços ofereçam diferentes tipos de eventos com informações detalhadas como tema, descrição, data, horário e status.

**🆕 Novo:** Campo `status` com valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO

### Estrutura do Space Event Type
```json
{
  "id": 1,
  "space_id": 1,
  "event_type_id": 1,
  "tema": "Noite de Jazz Clássico",
  "descricao": "Uma noite especial dedicada aos grandes clássicos do jazz",
  "status": "CONTRATANDO",
  "link_divulgacao": "https://example.com/jazz-classico",
  "banner": "/static/banners/jazz-night.jpg",
  "data": "2025-05-15T20:00:00",
  "horario": "20:00",
  "created_at": "2025-07-23T14:16:15"
}
```

### Valores de Status Disponíveis
- **CONTRATANDO** - Evento em processo de contratação
- **FECHADO** - Evento confirmado e fechado
- **SUSPENSO** - Evento temporariamente suspenso
- **CANCELADO** - Evento cancelado

### Endpoints Disponíveis

#### CRUD Básico
```bash
# Listar todos os space event types
GET /api/v1/space-event-types/

# Obter space event type por ID
GET /api/v1/space-event-types/{id}

# Criar novo space event type
POST /api/v1/space-event-types/

# Atualizar space event type
PUT /api/v1/space-event-types/{id}

# Deletar space event type
DELETE /api/v1/space-event-types/{id}
```

#### Endpoints Específicos
```bash
# Atualizar apenas o status de um space event type
PATCH /api/v1/space-event-types/{id}/status

# Listar eventos de um espaço específico
GET /api/v1/space-event-types/space/{space_id}

# Listar espaços de um tipo de evento específico
GET /api/v1/space-event-types/event-type/{event_type_id}

# Listar relacionamentos específicos entre espaço e tipo de evento
GET /api/v1/space-event-types/space/{space_id}/event-type/{event_type_id}

# Deletar todos os relacionamentos de um espaço
DELETE /api/v1/space-event-types/space/{space_id}

# Deletar todos os relacionamentos de um tipo de evento
DELETE /api/v1/space-event-types/event-type/{event_type_id}
```

### Exemplos de Uso

#### 1. Criar Space Event Type
```bash
curl -X POST "http://localhost:8000/api/v1/space-event-types/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "event_type_id": 1,
    "tema": "Noite de Jazz Clássico",
    "descricao": "Uma noite especial dedicada aos grandes clássicos do jazz",
    "status": "CONTRATANDO",
    "link_divulgacao": "https://example.com/jazz-classico",
    "banner": "/static/banners/jazz-night.jpg",
    "data": "2025-05-15T20:00:00",
    "horario": "20:00"
  }'
```

#### 2. Atualizar Status
```bash
curl -X PATCH "http://localhost:8000/api/v1/space-event-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "FECHADO"
  }'
```

#### 3. Listar Eventos de um Espaço
```bash
curl -X GET "http://localhost:8000/api/v1/space-event-types/space/1" \
  -H "Authorization: Bearer $TOKEN"
```

#### 4. Atualizar Space Event Type
```bash
curl -X PUT "http://localhost:8000/api/v1/space-event-types/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tema": "Noite de Jazz Clássico - Atualizado",
    "descricao": "Descrição atualizada do evento",
    "status": "FECHADO",
    "link_divulgacao": "https://example.com/jazz-atualizado",
    "data": "2025-05-20T20:00:00",
    "horario": "20:30"
  }'
```

### Regras de Negócio

- **Status obrigatório:** Todos os space event types devem ter um status definido
- **Status padrão:** CONTRATANDO (aplicado automaticamente em novos registros)
- **Validação de relacionamentos:** Space ID e Event Type ID devem existir
- **Campos obrigatórios:** tema, descricao, data, horario
- **Campos opcionais:** link_divulgacao, banner
- **Autenticação:** Todos os endpoints requerem autenticação

### Exemplo Prático: Gerenciar Eventos de um Espaço

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@eshow.com", "password": "admin123"}' | jq -r '.access_token')

# 2. Criar evento
curl -X POST "http://localhost:8000/api/v1/space-event-types/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "event_type_id": 1,
    "tema": "Festival de Música Eletrônica",
    "descricao": "Festival com os melhores DJs da cidade",
    "status": "CONTRATANDO",
    "link_divulgacao": "https://example.com/eletronica-festival",
    "banner": "/static/banners/electronic-festival.jpg",
    "data": "2025-06-15T22:00:00",
    "horario": "22:00"
  }' | jq

# 3. Listar eventos do espaço
curl -X GET "http://localhost:8000/api/v1/space-event-types/space/1" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Atualizar status para FECHADO
curl -X PATCH "http://localhost:8000/api/v1/space-event-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "FECHADO"}' | jq

# 5. Verificar evento atualizado
curl -X GET "http://localhost:8000/api/v1/space-event-types/1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## Sistema de Space Festival Types

### Visão Geral
O sistema de Space Festival Types gerencia relacionamentos N:N entre espaços e tipos de festivais, permitindo que espaços ofereçam diferentes tipos de festivais com informações detalhadas como tema, descrição, data, horário e status.

**🆕 Novo:** Campo `status` com valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO

### Estrutura do Space Festival Type
```json
{
  "id": 1,
  "space_id": 1,
  "festival_type_id": 1,
  "tema": "Festival de Rock Paulista dos Anos 80",
  "descricao": "Festival dedicado ao rock nacional paulista dos anos 80, com shows de bandas clássicas e cover.",
  "status": "CONTRATANDO",
  "link_divulgacao": "https://rockpaulista80.com.br",
  "banner": "static/banners/rock_paulista_80.jpg",
  "data": "2024-07-15T20:00:00",
  "horario": "20:00-02:00",
  "created_at": "2025-07-24T13:24:49"
}
```

### Valores de Status Disponíveis
- **CONTRATANDO** - Festival em processo de contratação
- **FECHADO** - Festival confirmado e fechado
- **SUSPENSO** - Festival temporariamente suspenso
- **CANCELADO** - Festival cancelado

### Endpoints Disponíveis

#### CRUD Básico
```bash
# Listar todos os space festival types
GET /api/v1/space-festival-types/

# Obter space festival type por ID
GET /api/v1/space-festival-types/{id}

# Criar novo space festival type
POST /api/v1/space-festival-types/

# Atualizar space festival type
PUT /api/v1/space-festival-types/{id}

# Deletar space festival type
DELETE /api/v1/space-festival-types/{id}
```

#### Endpoints Específicos
```bash
# Atualizar apenas o status de um space festival type
PATCH /api/v1/space-festival-types/{id}/status

# Listar festivais de um espaço específico
GET /api/v1/space-festival-types/space/{space_id}

# Listar espaços de um tipo de festival específico
GET /api/v1/space-festival-types/festival-type/{festival_type_id}

# Listar relacionamentos específicos entre espaço e tipo de festival
GET /api/v1/space-festival-types/space/{space_id}/festival-type/{festival_type_id}

# Deletar todos os relacionamentos de um espaço
DELETE /api/v1/space-festival-types/space/{space_id}

# Deletar todos os relacionamentos de um tipo de festival
DELETE /api/v1/space-festival-types/festival-type/{festival_type_id}
```

### Exemplos de Uso

#### 1. Criar Space Festival Type
```bash
curl -X POST "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "festival_type_id": 1,
    "tema": "Festival de Jazz Internacional",
    "descricao": "Festival com artistas internacionais de jazz",
    "status": "CONTRATANDO",
    "link_divulgacao": "https://example.com/jazz-internacional",
    "banner": "/static/banners/jazz-internacional.jpg",
    "data": "2025-08-15T20:00:00",
    "horario": "20:00-02:00"
  }'
```

#### 2. Atualizar Status
```bash
curl -X PATCH "http://localhost:8000/api/v1/space-festival-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "FECHADO"
  }'
```

#### 3. Listar Festivais de um Espaço
```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/space/1" \
  -H "Authorization: Bearer $TOKEN"
```

#### 4. Atualizar Space Festival Type
```bash
curl -X PUT "http://localhost:8000/api/v1/space-festival-types/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "tema": "Festival de Jazz Internacional - Atualizado",
    "descricao": "Descrição atualizada do festival",
    "status": "FECHADO",
    "link_divulgacao": "https://example.com/jazz-atualizado",
    "data": "2025-08-20T20:00:00",
    "horario": "20:30-02:30"
  }'
```

### Regras de Negócio

- **Status obrigatório:** Todos os space festival types devem ter um status definido
- **Status padrão:** CONTRATANDO (aplicado automaticamente em novos registros)
- **Validação de relacionamentos:** Space ID e Festival Type ID devem existir
- **Campos obrigatórios:** tema, descricao, data, horario
- **Campos opcionais:** link_divulgacao, banner
- **Autenticação:** Todos os endpoints requerem autenticação

### Exemplo Prático: Gerenciar Festivais de um Espaço

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@eshow.com", "password": "admin123"}' | jq -r '.access_token')

# 2. Criar festival
curl -X POST "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "space_id": 1,
    "festival_type_id": 1,
    "tema": "Festival de Música Eletrônica",
    "descricao": "Festival com os melhores DJs da cidade",
    "status": "CONTRATANDO",
    "link_divulgacao": "https://example.com/eletronica-festival",
    "banner": "/static/banners/electronic-festival.jpg",
    "data": "2025-06-15T22:00:00",
    "horario": "22:00-06:00"
  }' | jq

# 3. Listar festivais do espaço
curl -X GET "http://localhost:8000/api/v1/space-festival-types/space/1" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Atualizar status para FECHADO
curl -X PATCH "http://localhost:8000/api/v1/space-festival-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "FECHADO"}' | jq

# 5. Verificar festival atualizado
curl -X GET "http://localhost:8000/api/v1/space-festival-types/1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## Sistema de Busca por Localização

### Visão Geral
O sistema de busca por localização permite encontrar espaços para artistas e artistas para espaços baseado em raio de atuação, utilizando cálculo de distância geográfica e verificação de disponibilidade.

**🆕 Atualização Importante:**
- **Obtenção de Coordenadas 100% Local:**
  - O sistema utiliza uma base local de coordenadas de municípios brasileiros, importada do IBGE (malha municipal) e/ou bases de CEPs com latitude/longitude.
  - Não há mais dependência de APIs externas (ViaCEP, Nominatim, Google, etc) para busca de coordenadas.
  - A busca por coordenadas é feita diretamente no banco de dados local, garantindo performance, disponibilidade e precisão.
  - Caso o CEP não seja encontrado, o sistema tenta buscar por prefixo ou por cidade/UF na base local.

**Como funciona a busca de coordenadas:**
- Para cada CEP informado, o sistema:
  1. Busca o CEP exato na tabela local de coordenadas.
  2. Se não encontrar, busca por prefixo (primeiros 5 dígitos).
  3. Se ainda não encontrar, busca por cidade/UF (extraído do endereço cadastrado).
  4. Se não houver correspondência, retorna erro ou utiliza fallback para o município mais próximo.
- A base pode ser atualizada a qualquer momento via script, sem necessidade de expor API pública ou depender de terceiros.

**Vantagens da Solução Atual:**
- 100% offline/local, sem limites de requisição ou falhas externas
- Performance máxima (busca SQL/indexada)
- Fácil de atualizar e expandir (basta importar novos dumps de CEPs ou municípios)
- Resposta de API mais limpa (campo distance_km só no root do resultado)

### Endpoints Disponíveis

#### Buscar Espaços para Artista

GET `/api/v1/location-search/spaces-for-artist`
Busca espaços disponíveis para um artista baseado no seu raio de atuação.

#### Buscar Artistas para Espaço

GET `/api/v1/location-search/artists-for-space`
Busca artistas disponíveis para um espaço baseado no raio de atuação dos artistas.

#### Parâmetros de Query
- `return_full_data` (boolean, opcional): Se deve retornar dados completos ou apenas IDs. Padrão: `true`
- `max_results` (integer, opcional): Limite máximo de resultados. Padrão: `100`

#### Exemplo de Requisição
```bash
GET /api/v1/location-search/artists-for-space?return_full_data=true&max_results=50
Authorization: Bearer <token>
```

#### Exemplo de Resposta
```json
{
  "results": [
    {
      "id": 3,
      "profile_id": 8,
      "artist_type_id": 1,
      "raio_atuacao": 30.0,
      "valor_hora": 200.0,
      "valor_couvert": 30.0,
      "distance_km": 8.2,
      "profile": {
        "id": 8,
        "full_name": "João Silva",
        "artistic_name": "João Músico",
        "cep": "01234-890",
        "cidade": "São Paulo",
        "uf": "SP"
      }
    }
  ],
  "total_count": 1,
  "search_radius_km": 0,
  "origin_cep": "01234-567"
}
```

### Lógica de Busca

1. **Obtenção de Coordenadas:** Busca 100% local na base de municípios/CEPs.
2. **Cálculo de Distância:** Fórmula de Haversine entre as coordenadas dos CEPs.
3. **Filtro por Raio:** Apenas resultados dentro do raio de atuação do artista ou espaço.
4. **Verificação de Disponibilidade:** Checa conflitos de agenda e status de contratação.
5. **Retorno:** Lista de resultados ordenados por distância.

### Limitações Removidas
- **Não há mais dependência de APIs externas** para coordenadas.
- **Não há mais limitação de volume** (pode importar quantos CEPs/municípios quiser).
- **Não há mais delays de rede** para busca de localização.

### Como Atualizar a Base de Coordenadas
- Utilize os scripts de importação fornecidos para importar novos dumps do IBGE, BrasilCeps, OSM, etc.
- A base pode ser expandida a qualquer momento sem downtime.

---

## 🔧 Configuração de Desenvolvimento

```API_USAGE.md
```