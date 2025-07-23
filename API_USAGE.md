# Guia de Uso da API

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

### 3. Logout
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "message": "Logout realizado com sucesso"
}
```

**Nota:** Após o logout, o token será invalidado e não poderá ser usado novamente.

### 4. Renovar Token
```bash
curl -X POST "http://localhost:8000/api/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "SEU_REFRESH_TOKEN_AQUI"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Endpoints de Usuários (Protegidos)

### 1. Obter Perfil do Usuário Atual
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 2. Obter Usuário por ID
```bash
curl -X GET "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 3. Listar Todos os Usuários
```bash
curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 4. Atualizar Usuário
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva Atualizado",
    "email": "joao.novo@example.com",
    "is_active": true
  }'
```

### 5. Deletar Usuário
```bash
curl -X DELETE "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

## Endpoints de Roles (Protegidos)

### 1. Listar Todos os Roles
```bash
curl -X GET "http://localhost:8000/api/v1/roles/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 2. Obter Role por ID
```bash
curl -X GET "http://localhost:8000/api/v1/roles/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 3. Criar Novo Role
```bash
curl -X POST "http://localhost:8000/api/v1/roles/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Admin"
  }'
```

**Valores válidos para role:**
- `"Admin"`
- `"Artista"`
- `"Espaço"`

### 4. Atualizar Role
```bash
curl -X PUT "http://localhost:8000/api/v1/roles/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Artista"
  }'
```

### 5. Deletar Role
```bash
curl -X DELETE "http://localhost:8000/api/v1/roles/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

## Endpoints de Profiles (Protegidos)

### 1. Listar Todos os Profiles
```bash
curl -X GET "http://localhost:8000/api/v1/profiles/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

**Parâmetros de Paginação:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)

### 2. Obter Profile por ID
```bash
curl -X GET "http://localhost:8000/api/v1/profiles/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 3. Obter Profiles por Role
```bash
curl -X GET "http://localhost:8000/api/v1/profiles/role/2" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

### 4. Criar Novo Profile
```bash
curl -X POST "http://localhost:8000/api/v1/profiles/" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "full_name": "João Silva Costa",
    "artistic_name": "João Artista",
    "bio": "Artista versátil com experiência em diversos estilos musicais",
    "cep": "12345-678",
    "logradouro": "Rua das Flores",
    "numero": "123",
    "complemento": "Apto 45",
    "cidade": "São Paulo",
    "uf": "SP",
    "telefone_movel": "(11) 99999-8888",
    "whatsapp": "(11) 99999-8888"
  }'
```

**Campos Obrigatórios:**
- `role_id`: ID do role associado (deve existir na tabela roles)
- `full_name`: Nome completo ou Razão Social (máx: 255 caracteres)
- `artistic_name`: Nome artístico ou Nome de Fantasia (máx: 255 caracteres)
- `bio`: Bio/apresentação (texto livre)
- `cep`: CEP (8-10 caracteres)
- `logradouro`: Logradouro (máx: 255 caracteres)
- `numero`: Número (máx: 20 caracteres)
- `cidade`: Cidade (máx: 100 caracteres)
- `uf`: UF (exatamente 2 caracteres)
- `telefone_movel`: Telefone móvel (máx: 20 caracteres)

**Campos Opcionais:**
- `complemento`: Complemento (máx: 100 caracteres)
- `telefone_fixo`: Telefone fixo (máx: 20 caracteres)
- `whatsapp`: WhatsApp (máx: 20 caracteres)

### 5. Atualizar Profile
```bash
curl -X PUT "http://localhost:8000/api/v1/profiles/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "artistic_name": "João Artista Atualizado",
    "bio": "Nova bio atualizada",
    "cidade": "Rio de Janeiro",
    "uf": "RJ"
  }'
```

**Nota:** Todos os campos são opcionais na atualização. Apenas os campos fornecidos serão atualizados.

### 6. Deletar Profile
```bash
curl -X DELETE "http://localhost:8000/api/v1/profiles/1" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI"
```

**Resposta:**
```json
{
  "message": "Profile com ID 1 foi deletado com sucesso"
}
```

## Endpoints de Artists (Protegidos)

### 1. Criar Novo Artista
```bash
curl -X POST "http://localhost:8000/api/v1/artists/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 2,
    "artist_type_id": 1,
    "dias_apresentacao": ["sexta", "sábado", "domingo"],
    "raio_atuacao": 50.0,
    "duracao_apresentacao": 2.0,
    "valor_hora": 150.0,
    "valor_couvert": 20.0,
    "requisitos_minimos": "Sistema de som básico, microfone, iluminação adequada",
    "instagram": "https://instagram.com/artista1",
    "youtube": "https://youtube.com/@artista1",
    "spotify": "https://open.spotify.com/artist/artista1"
  }'
```

**Campos Obrigatórios:**
- `profile_id`: ID do profile associado (deve existir na tabela profiles)
- `artist_type_id`: ID do tipo de artista (deve existir na tabela artist_types)

**⚠️ RESTRIÇÃO IMPORTANTE:**
- Apenas profiles com `role_id = 2` (role "ARTISTA") podem cadastrar artistas
- Se tentar usar um profile com role diferente, retornará erro 400: "Apenas perfis com role 'ARTISTA' podem cadastrar artistas"
- `dias_apresentacao`: Lista de dias da semana para apresentação
- `raio_atuacao`: Raio de atuação em km (deve ser > 0)
- `duracao_apresentacao`: Duração da apresentação em horas (deve ser > 0)
- `valor_hora`: Valor por hora em reais (deve ser >= 0)
- `valor_couvert`: Valor do couvert artístico em reais (deve ser >= 0)
- `requisitos_minimos`: Requisitos mínimos para apresentação (texto)

**Campos Opcionais:**
- `instagram`: Link do Instagram
- `tiktok`: Link do TikTok
- `youtube`: Link do YouTube
- `facebook`: Link do Facebook
- `soundcloud`: Link do SoundCloud
- `bandcamp`: Link do Bandcamp
- `spotify`: Link do Spotify
- `deezer`: Link do Deezer

**Dias válidos para apresentação:**
- `"segunda"`, `"terça"`, `"quarta"`, `"quinta"`, `"sexta"`, `"sábado"`, `"domingo"`

**Relacionamentos:**
A tabela `artists` possui relacionamentos com:
- **profiles**: Um artista pertence a um profile (1:1)
- **artist_types**: Um artista tem um tipo específico (N:1)

Para incluir os dados relacionados nas respostas, use o parâmetro `include_relations=true` nos endpoints GET.

### 2. Listar Todos os Artistas
```bash
curl -X GET "http://localhost:8000/api/v1/artists/" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/artists/?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 3. Obter Artista por ID
```bash
curl -X GET "http://localhost:8000/api/v1/artists/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/artists/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 4. Obter Artista por Profile ID
```bash
curl -X GET "http://localhost:8000/api/v1/artists/profile/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/artists/profile/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 5. Listar Artistas por Tipo
```bash
curl -X GET "http://localhost:8000/api/v1/artists/type/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/artists/type/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 6. Atualizar Artista
```bash
curl -X PUT "http://localhost:8000/api/v1/artists/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "valor_hora": 180.0,
    "dias_apresentacao": ["sexta", "sábado"],
    "instagram": "https://instagram.com/artista1_atualizado"
  }'
```

**Nota:** Todos os campos são opcionais na atualização. Apenas os campos fornecidos serão atualizados.

**⚠️ RESTRIÇÃO:** Se for alterado o `profile_id`, o novo profile deve ter `role_id = 2` (role "ARTISTA").

### 7. Deletar Artista
```bash
curl -X DELETE "http://localhost:8000/api/v1/artists/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "Artista com ID 1 foi deletado com sucesso"
}
```

## Endpoints Públicos

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Resposta:**
```json
{
    "status": "healthy",
    "architecture": "hexagonal",
    "timestamp": "2025-07-19T17:54:24.947336",
    "version": "1.0.0",
    "copyright": "© 2025 eShow. Todos os direitos reservados."
}
```

## Fluxo de Autenticação

1. **Registro/Login**: Obtenha `access_token` e `refresh_token`
2. **Usar API**: Use o `access_token` no header `Authorization: Bearer <token>`
3. **Token Expirado**: Use o `refresh_token` para obter novos tokens
4. **Logout**: Chame o endpoint de logout para invalidar o token atual

## Tratamento de Erros

### 401 Unauthorized
- Token inválido ou expirado
- Token na blacklist (após logout)
- Credenciais incorretas

### 400 Bad Request
- Dados de entrada inválidos
- Usuário inativo

### 404 Not Found
- Recurso não encontrado

### 422 Validation Error
- Dados de entrada não atendem ao schema 

## Tipos de Artistas (Artist Types)

Endpoint para gerenciar os tipos de artistas disponíveis no sistema.

### Campos
- `id`: Identificador único do tipo de artista
- `tipo`: Tipo de artista (enum: Cantor(a) solo, Dupla, Trio, Banda, Grupo)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Criar tipo de artista
```bash
curl -X POST "http://localhost:8000/api/v1/artist-types/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Cantor(a) solo"
}'
```

### Listar todos os tipos de artistas
```bash
curl -X GET "http://localhost:8000/api/v1/artist-types/" \
  -H "Authorization: Bearer <TOKEN>"
```

### Buscar tipo de artista por ID
```bash
curl -X GET "http://localhost:8000/api/v1/artist-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### Atualizar tipo de artista
```bash
curl -X PUT "http://localhost:8000/api/v1/artist-types/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Banda"
}'
```

### Deletar tipo de artista
```bash
curl -X DELETE "http://localhost:8000/api/v1/artist-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### Possíveis valores para `tipo`
- "Cantor(a) solo"
- "Dupla"
- "Trio"
- "Banda"
- "Grupo" 

## Estilos Musicais (Musical Styles)

Endpoint para gerenciar os estilos musicais disponíveis no sistema.

### Campos
- `id`: Identificador único do estilo musical
- `estyle`: Estilo musical (qualquer valor string)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Criar estilo musical
```bash
curl -X POST "http://localhost:8000/api/v1/musical-styles/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "estyle": "Samba"
}'
```

### Listar todos os estilos musicais
```bash
curl -X GET "http://localhost:8000/api/v1/musical-styles/" \
  -H "Authorization: Bearer <TOKEN>"
```

### Buscar estilo musical por ID
```bash
curl -X GET "http://localhost:8000/api/v1/musical-styles/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### Atualizar estilo musical
```bash
curl -X PUT "http://localhost:8000/api/v1/musical-styles/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "estyle": "Pagode"
}'
```

### Deletar estilo musical
```bash
curl -X DELETE "http://localhost:8000/api/v1/musical-styles/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### Observação
O campo `estyle` aceita qualquer valor string. Não há restrição de valores fixos.

## Relacionamento Artists-Musical Styles (N:N)

Endpoint para gerenciar o relacionamento N:N entre artistas e estilos musicais.

### Campos
- `artist_id`: ID do artista (relacionamento com artista)
- `musical_style_id`: ID do estilo musical (relacionamento com estilo musical)
- `created_at`: Data de criação do relacionamento

### 1. Criar Relacionamento Individual
```bash
curl -X POST "http://localhost:8000/api/v1/artist-musical-styles/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "artist_id": 1,
    "musical_style_id": 2
  }'
```

### 2. Criar Relacionamentos em Lote
```bash
curl -X POST "http://localhost:8000/api/v1/artist-musical-styles/bulk" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "artist_id": 1,
    "musical_style_ids": [1, 2, 3]
  }'
```

### 3. Obter Estilos Musicais de um Artista
```bash
curl -X GET "http://localhost:8000/api/v1/artist-musical-styles/artist/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### 4. Obter Artistas de um Estilo Musical
```bash
curl -X GET "http://localhost:8000/api/v1/artist-musical-styles/musical-style/2" \
  -H "Authorization: Bearer <TOKEN>"
```

### 5. Obter Relacionamento Específico
```bash
curl -X GET "http://localhost:8000/api/v1/artist-musical-styles/1/2" \
  -H "Authorization: Bearer <TOKEN>"
```

### 6. Atualizar Estilos Musicais de um Artista
```bash
curl -X PUT "http://localhost:8000/api/v1/artist-musical-styles/artist/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '[1, 3, 5]'
```

**Nota:** Este endpoint substitui todos os estilos musicais existentes do artista pelos novos fornecidos.

### 7. Deletar Relacionamento Específico
```bash
curl -X DELETE "http://localhost:8000/api/v1/artist-musical-styles/1/2" \
  -H "Authorization: Bearer <TOKEN>"
```

### 8. Deletar Todos os Relacionamentos de um Artista
```bash
curl -X DELETE "http://localhost:8000/api/v1/artist-musical-styles/artist/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### 9. Deletar Todos os Relacionamentos de um Estilo Musical
```bash
curl -X DELETE "http://localhost:8000/api/v1/artist-musical-styles/musical-style/2" \
  -H "Authorization: Bearer <TOKEN>"
```

### Observações Importantes

1. **Validações:**
   - O artista e o estilo musical devem existir antes de criar o relacionamento
   - Não é possível criar relacionamentos duplicados
   - IDs devem ser maiores que zero

2. **Operações em Lote:**
   - A criação em lote é mais eficiente para múltiplos relacionamentos
   - Todos os estilos musicais devem existir
   - Se qualquer relacionamento já existir, a operação falha

3. **Atualização:**
   - A atualização substitui completamente os estilos musicais do artista
   - Relacionamentos existentes são removidos e novos são criados

4. **Integração com Artists:**
   - Ao usar `include_relations=true` nos endpoints de artists, os estilos musicais serão incluídos na resposta

## Tipos de Espaço (Space Types)

Endpoint para gerenciar os tipos de espaço disponíveis no sistema.

### Campos
- `id`: Identificador único do tipo de espaço
- `tipo`: Tipo de espaço (string livre - não é enum)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Valores Iniciais Populados
O sistema já vem com os seguintes tipos de espaço pré-cadastrados:
- Bar
- Restaurante
- Clube
- Balneário
- Parque Aquático
- Resort
- Embarcação
- Boate
- Salão de Baile
- Casa de Forró
- Centro de Tradições Regionais
- Associação Social
- Salão de Recepções
- Evento
- Festival

### 1. Criar tipo de espaço
```bash
curl -X POST "http://localhost:8000/api/v1/space-types/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Teatro"
  }'
```

**Resposta:**
```json
{
  "tipo": "Teatro",
  "id": 16,
  "created_at": "2025-07-22T20:17:21",
  "updated_at": "2025-07-22T20:17:21"
}
```

### 2. Listar todos os tipos de espaço
```bash
curl -X GET "http://localhost:8000/api/v1/space-types/" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)

**Exemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/space-types/?skip=0&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

### 3. Buscar tipo de espaço por ID
```bash
curl -X GET "http://localhost:8000/api/v1/space-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "tipo": "Bar",
  "id": 1,
  "created_at": "2025-07-22T20:11:39",
  "updated_at": "2025-07-22T20:11:39"
}
```

### 4. Atualizar tipo de espaço
```bash
curl -X PUT "http://localhost:8000/api/v1/space-types/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Bar e Restaurante"
  }'
```

**Resposta:**
```json
{
  "tipo": "Bar e Restaurante",
  "id": 1,
  "created_at": "2025-07-22T20:11:39",
  "updated_at": "2025-07-22T20:17:28"
}
```

### 5. Deletar tipo de espaço
```bash
curl -X DELETE "http://localhost:8000/api/v1/space-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "SpaceType com ID 1 foi deletado com sucesso"
}
```

**Status:**
- 200 OK (sucesso)
- 404 Not Found (se o tipo não existir)

### Observações Importantes

1. **Validações:**
   - O campo `tipo` é obrigatório e deve ser uma string não vazia
   - Não é possível criar tipos duplicados (mesmo nome)
   - IDs devem ser maiores que zero

2. **Flexibilidade:**
   - Diferente dos Artist Types, os Space Types aceitam qualquer valor string
   - Não há restrição de valores fixos (não é enum)

3. **Integridade:**
   - Não é possível deletar um tipo de espaço que esteja sendo usado por outros registros
   - A atualização verifica se o novo nome já existe em outro registro

4. **Performance:**
   - O campo `tipo` possui índice único para busca eficiente
   - Paginação disponível para listagens grandes

## Tipos de Evento (Event Types)

Endpoint para gerenciar os tipos de evento disponíveis no sistema.

### Campos
- `id`: Identificador único do tipo de evento
- `type`: Tipo de evento (string livre - não é enum)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Valores Iniciais Populados
O sistema já vem com os seguintes tipos de evento pré-cadastrados:
- Aniversário
- Casamento
- Formatura
- Inauguração
- Lançamento
- Casual
- Recorrente

### 1. Criar tipo de evento
```bash
curl -X POST "http://localhost:8000/api/v1/event-types/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Conferência"
  }'
```

**Resposta:**
```json
{
  "type": "Conferência",
  "id": 8,
  "created_at": "2025-07-22T20:52:41",
  "updated_at": "2025-07-22T20:52:41"
}
```

### 2. Listar todos os tipos de evento
```bash
curl -X GET "http://localhost:8000/api/v1/event-types/" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)

**Exemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/event-types/?skip=0&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

### 3. Buscar tipo de evento por ID
```bash
curl -X GET "http://localhost:8000/api/v1/event-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "type": "Aniversário",
  "id": 1,
  "created_at": "2025-07-22T20:52:16",
  "updated_at": "2025-07-22T20:52:16"
}
```

### 4. Atualizar tipo de evento
```bash
curl -X PUT "http://localhost:8000/api/v1/event-types/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Aniversário Especial"
  }'
```

**Resposta:**
```json
{
  "type": "Aniversário Especial",
  "id": 1,
  "created_at": "2025-07-22T20:52:16",
  "updated_at": "2025-07-22T20:52:45"
}
```

### 5. Deletar tipo de evento
```bash
curl -X DELETE "http://localhost:8000/api/v1/event-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "EventType com ID 1 foi deletado com sucesso"
}
```

**Status:**
- 200 OK (sucesso)
- 404 Not Found (se o tipo não existir)

### Observações Importantes

1. **Validações:**
   - O campo `type` é obrigatório e deve ser uma string não vazia
   - Não é possível criar tipos duplicados (mesmo nome)
   - IDs devem ser maiores que zero

2. **Flexibilidade:**
   - Diferente dos Artist Types, os Event Types aceitam qualquer valor string
   - Não há restrição de valores fixos (não é enum)

3. **Integridade:**
   - Não é possível deletar um tipo de evento que esteja sendo usado por outros registros
   - A atualização verifica se o novo nome já existe em outro registro

4. **Performance:**
   - O campo `type` possui índice único para busca eficiente
   - Paginação disponível para listagens grandes

## Tipos de Festival (Festival Types)

Endpoint para gerenciar os tipos de festival disponíveis no sistema.

### Campos
- `id`: Identificador único do tipo de festival
- `type`: Tipo de festival (string livre - não é enum)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Valores Iniciais Populados
O sistema já vem com os seguintes tipos de festival pré-cadastrados:
- Aniversário de Emancipação Política
- Festa Religiosa
- Alvorada
- Vaquejada
- Micareta
- Festa Junina
- Carnaval
- Cavalgada
- Festa de Vaqueiro
- Festa de Peão
- Festa de Colono
- Festa Anual
- Comemoração Cívica
- Parada do Orgulho LGBTQIA+

### 1. Criar tipo de festival
```bash
curl -X POST "http://localhost:8000/api/v1/festival-types/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Festival de Música"
  }'
```

**Resposta:**
```json
{
  "type": "Festival de Música",
  "id": 15,
  "created_at": "2025-07-22T21:39:51",
  "updated_at": "2025-07-22T21:39:51"
}
```

### 2. Listar todos os tipos de festival
```bash
curl -X GET "http://localhost:8000/api/v1/festival-types/" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)

**Exemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/festival-types/?skip=0&limit=10" \
  -H "Authorization: Bearer <TOKEN>"
```

### 3. Buscar tipo de festival por ID
```bash
curl -X GET "http://localhost:8000/api/v1/festival-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "type": "Aniversário de Emancipação Política",
  "id": 1,
  "created_at": "2025-07-22T21:37:54",
  "updated_at": "2025-07-22T21:37:54"
}
```

### 4. Atualizar tipo de festival
```bash
curl -X PUT "http://localhost:8000/api/v1/festival-types/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Aniversário de Emancipação Política Especial"
  }'
```

**Resposta:**
```json
{
  "type": "Aniversário de Emancipação Política Especial",
  "id": 1,
  "created_at": "2025-07-22T21:37:54",
  "updated_at": "2025-07-22T21:40:45"
}
```

### 5. Deletar tipo de festival
```bash
curl -X DELETE "http://localhost:8000/api/v1/festival-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "FestivalType com ID 1 foi deletado com sucesso"
}
```

**Status:**
- 200 OK (sucesso)
- 404 Not Found (se o tipo não existir)

### Observações Importantes

1. **Validações:**
   - O campo `type` é obrigatório e deve ser uma string não vazia
   - Não é possível criar tipos duplicados (mesmo nome)
   - IDs devem ser maiores que zero

2. **Flexibilidade:**
   - Diferente dos Artist Types, os Festival Types aceitam qualquer valor string
   - Não há restrição de valores fixos (não é enum)

3. **Integridade:**
   - Não é possível deletar um tipo de festival que esteja sendo usado por outros registros
   - A atualização verifica se o novo nome já existe em outro registro

4. **Performance:**
   - O campo `type` possui índice único para busca eficiente
   - Paginação disponível para listagens grandes

## Espaços (Spaces)

Endpoint para gerenciar os espaços disponíveis no sistema. Os espaços representam locais onde artistas podem se apresentar.

### Campos
- `id`: Identificador único do espaço
- `profile_id`: ID do profile associado (relacionamento obrigatório)
- `space_type_id`: ID do tipo de espaço (relacionamento obrigatório)
- `event_type_id`: ID do tipo de evento (relacionamento opcional - apenas para eventos)
- `festival_type_id`: ID do tipo de festival (relacionamento opcional - apenas para festivais)
- `acesso`: Tipo de acesso (Enum: "Público", "Privado")
- `dias_apresentacao`: Dias da semana para apresentação (array de strings)
- `duracao_apresentacao`: Duração da apresentação em horas
- `valor_hora`: Valor por hora da apresentação em reais
- `valor_couvert`: Valor padrão do couvert artístico em reais
- `requisitos_minimos`: Requisitos mínimos para apresentação (texto livre)
- `oferecimentos`: Oferecimentos para o artista (texto livre)
- `estrutura_apresentacao`: Estrutura de apresentação (texto livre)
- `publico_estimado`: Público estimado (Enum: "<50", "51-100", "101-500", "501-1000", "1001-3000", "3001-5000", "5001-10000", "> 10000")
- `fotos_ambiente`: Array com paths das imagens salvas
- `instagram`: Link do Instagram (opcional)
- `tiktok`: Link do TikTok (opcional)
- `youtube`: Link do YouTube (opcional)
- `facebook`: Link do Facebook (opcional)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### Relacionamentos
A tabela `spaces` possui relacionamentos com:
- **profiles**: Um espaço pertence a um profile (N:1)
- **space_types**: Um espaço tem um tipo específico (N:1)
- **event_types**: Um espaço pode ter um tipo de evento (N:1, opcional)
- **festival_types**: Um espaço pode ter um tipo de festival (N:1, opcional)

Para incluir os dados relacionados nas respostas, use o parâmetro `include_relations=true` nos endpoints GET.

### 1. Criar Novo Espaço
```bash
curl -X POST "http://localhost:8000/api/v1/spaces/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": 3,
    "space_type_id": 1,
    "event_type_id": null,
    "festival_type_id": null,
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
    "facebook": "https://facebook.com/barexemplo"
  }'
```

**Campos Obrigatórios:**
- `profile_id`: ID do profile associado (deve existir na tabela profiles)
- `space_type_id`: ID do tipo de espaço (deve existir na tabela space_types)
- `acesso`: Tipo de acesso ("Público" ou "Privado")

**⚠️ RESTRIÇÃO IMPORTANTE:**
- Apenas profiles com `role_id = 3` (role "ESPACO") podem cadastrar espaços
- Se tentar usar um profile com role diferente, retornará erro 400: "Apenas perfis com role 'ESPACO' podem cadastrar espaços"
- `dias_apresentacao`: Lista de dias da semana para apresentação
- `duracao_apresentacao`: Duração da apresentação em horas (deve ser > 0)
- `valor_hora`: Valor por hora em reais (deve ser >= 0)
- `valor_couvert`: Valor do couvert artístico em reais (deve ser >= 0)
- `requisitos_minimos`: Requisitos mínimos para apresentação (texto)
- `oferecimentos`: Oferecimentos para o artista (texto)
- `estrutura_apresentacao`: Estrutura de apresentação (texto)
- `publico_estimado`: Público estimado (uma das faixas válidas)
- `fotos_ambiente`: Array de paths das imagens

**Campos Opcionais:**
- `event_type_id`: ID do tipo de evento (apenas para eventos)
- `festival_type_id`: ID do tipo de festival (apenas para festivais)
- `instagram`: Link do Instagram
- `tiktok`: Link do TikTok
- `youtube`: Link do YouTube
- `facebook`: Link do Facebook

**Valores válidos para acesso:**
- `"Público"`
- `"Privado"`

**Valores válidos para publico_estimado:**
- `"<50"`
- `"51-100"`
- `"101-500"`
- `"501-1000"`
- `"1001-3000"`
- `"3001-5000"`
- `"5001-10000"`
- `"> 10000"`

**Dias válidos para apresentação:**
- `"segunda"`, `"terça"`, `"quarta"`, `"quinta"`, `"sexta"`, `"sábado"`, `"domingo"`

### 2. Listar Todos os Espaços
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `skip`: Número de registros para pular (padrão: 0)
- `limit`: Número máximo de registros (padrão: 100)
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta com relacionamentos:**
```json
[
  {
    "profile_id": 1,
    "space_type_id": 1,
    "event_type_id": null,
    "festival_type_id": null,
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
    "created_at": "2025-07-23T00:02:19",
    "updated_at": "2025-07-23T00:02:19",
    "profile": {
      "id": 1,
      "full_name": "Alice Silva",
      "artistic_name": "Alice Artista",
      "bio": "Artista de música popular.",
      "cidade": "São Paulo",
      "uf": "SP"
    },
    "space_type": {
      "id": 1,
      "tipo": "Bar e Restaurante"
    },
    "event_type": null,
    "festival_type": null
  }
]
```

### 3. Obter Espaço por ID
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 4. Buscar Espaços por Profile ID
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/profile/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/profile/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 5. Buscar Espaços por Tipo de Espaço
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/space-type/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/space-type/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 6. Buscar Espaços por Tipo de Evento
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/event-type/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/event-type/1?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 7. Buscar Espaços por Tipo de Festival
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/festival-type/7" \
  -H "Authorization: Bearer <TOKEN>"
```

**Parâmetros:**
- `include_relations`: Incluir dados relacionados (padrão: false)

**Exemplo com relacionamentos:**
```bash
curl -X GET "http://localhost:8000/api/v1/spaces/festival-type/7?include_relations=true" \
  -H "Authorization: Bearer <TOKEN>"
```

### 8. Atualizar Espaço
```bash
curl -X PUT "http://localhost:8000/api/v1/spaces/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "valor_hora": 180.0,
    "dias_apresentacao": ["sexta", "sábado", "domingo"],
    "instagram": "https://instagram.com/bar_exemplo_atualizado"
  }'
```

**Resposta:**
```json
{
  "profile_id": 1,
  "space_type_id": 1,
  "event_type_id": null,
  "festival_type_id": null,
  "acesso": "Público",
  "dias_apresentacao": ["sexta", "sábado", "domingo"],
  "duracao_apresentacao": 3.0,
  "valor_hora": 180.0,
  "valor_couvert": 20.0,
  "requisitos_minimos": "Equipamento de som básico, microfone, instrumentos próprios",
  "oferecimentos": "Equipamento de som, iluminação, camarim, bebidas",
  "estrutura_apresentacao": "Palco de 4x3 metros, sistema de som profissional, iluminação cênica",
  "publico_estimado": "101-500",
  "fotos_ambiente": ["/fotos/bar1.jpg", "/fotos/bar2.jpg"],
  "instagram": "https://instagram.com/bar_exemplo_atualizado",
  "tiktok": "https://tiktok.com/@bar_exemplo",
  "youtube": null,
  "facebook": "https://facebook.com/barexemplo",
  "id": 1,
  "created_at": "2025-07-23T00:02:19",
  "updated_at": "2025-07-23T01:01:56"
}
```

**Atualização Parcial:** Todos os campos são opcionais na atualização. Apenas os campos fornecidos serão atualizados, os demais serão preservados com seus valores atuais.

**⚠️ RESTRIÇÃO:** Se for alterado o `profile_id`, o novo profile deve ter `role_id = 3` (role "ESPACO").

### 9. Deletar Espaço
```bash
curl -X DELETE "http://localhost:8000/api/v1/spaces/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "Space com ID 1 foi deletado com sucesso"
}
```

### Observações Importantes

1. **Validações:**
   - O profile e o space_type devem existir antes de criar o espaço
   - Os campos event_type_id e festival_type_id são opcionais e mutuamente exclusivos na prática
   - Valores numéricos devem ser maiores que zero para duração e não negativos para valores monetários
   - Arrays não podem estar vazios

2. **Relacionamentos:**
   - Um espaço sempre pertence a um profile (obrigatório)
   - Um espaço sempre tem um tipo de espaço (obrigatório)
   - Um espaço pode ter um tipo de evento OU um tipo de festival (opcionais)
   - Use `include_relations=true` para obter dados completos dos relacionamentos

3. **Flexibilidade:**
   - Os campos de texto livre permitem descrições detalhadas
   - O array de fotos suporta múltiplas imagens
   - Links de redes sociais são opcionais

4. **Performance:**
   - Paginação disponível para listagens grandes
   - Índices nos campos de relacionamento para busca eficiente
   - Use relacionamentos apenas quando necessário para otimizar performance

## Relacionamento Space-Event Types (N:N)

Endpoint para gerenciar o relacionamento N:N entre espaços e tipos de evento. Este relacionamento permite criar eventos específicos associando um espaço a um tipo de evento com informações detalhadas como tema, descrição, data, horário e banners.

### Campos
- `id`: Identificador único do relacionamento
- `space_id`: ID do espaço (relacionamento com space)
- `event_type_id`: ID do tipo de evento (relacionamento com event_type)
- `tema`: Tema do evento (string obrigatória)
- `descricao`: Descrição do evento (string obrigatória)
- `data`: Data e horário do evento (datetime obrigatório)
- `horario`: Horário do evento (string obrigatória)
- `link_divulgacao`: Link para divulgação do evento (string opcional)
- `banner`: Path local da imagem do banner (string opcional)
- `created_at`: Data de criação do relacionamento

### 1. Criar Relacionamento
```bash
curl -X POST "http://localhost:8000/api/v1/space-event-types/" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "space_id": 1,
    "event_type_id": 2,
    "tema": "Show de Rock Especial",
    "descricao": "Uma noite especial com as melhores bandas de rock da cidade",
    "data": "2025-08-15T20:00:00",
    "horario": "20:00",
    "link_divulgacao": "https://example.com/rock-show",
    "banner": "/static/banners/rock-show.jpg"
  }'
```

**Resposta:**
```json
{
  "space_id": 1,
  "event_type_id": 2,
  "tema": "Show de Rock Especial",
  "descricao": "Uma noite especial com as melhores bandas de rock da cidade",
  "link_divulgacao": "https://example.com/rock-show",
  "banner": "/static/banners/rock-show.jpg",
  "data": "2025-08-15T20:00:00",
  "horario": "20:00",
  "id": 1,
  "created_at": "2025-07-23T11:33:42"
}
```

### 2. Listar Todos os Relacionamentos
```bash
curl -X GET "http://localhost:8000/api/v1/space-event-types/" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "items": [
    {
      "space_id": 1,
      "event_type_id": 1,
      "tema": "Noite de Jazz Clássico",
      "descricao": "Uma noite especial dedicada aos grandes clássicos do jazz",
      "link_divulgacao": "https://example.com/jazz-classico",
      "banner": "/static/banners/jazz-night.jpg",
      "data": "2025-07-30T20:00:00",
      "horario": "20:00",
      "id": 1,
      "created_at": "2025-07-23T11:28:23"
    }
  ]
}
```

### 3. Obter Relacionamento por ID
```bash
curl -X GET "http://localhost:8000/api/v1/space-event-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### 4. Obter Eventos de um Espaço
```bash
curl -X GET "http://localhost:8000/api/v1/space-event-types/space/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### 5. Obter Espaços de um Tipo de Evento
```bash
curl -X GET "http://localhost:8000/api/v1/space-event-types/event-type/2" \
  -H "Authorization: Bearer <TOKEN>"
```

### 6. Obter Relacionamentos Específicos (Espaço + Tipo de Evento)
```bash
curl -X GET "http://localhost:8000/api/v1/space-event-types/space/1/event-type/2" \
  -H "Authorization: Bearer <TOKEN>"
```

### 7. Atualizar Relacionamento
```bash
curl -X PUT "http://localhost:8000/api/v1/space-event-types/1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Show de Rock Atualizado",
    "descricao": "Descrição atualizada do evento",
    "horario": "21:00"
  }'
```

**Resposta:**
```json
{
  "space_id": 1,
  "event_type_id": 2,
  "tema": "Show de Rock Atualizado",
  "descricao": "Descrição atualizada do evento",
  "link_divulgacao": "https://example.com/rock-show",
  "banner": "/static/banners/rock-show.jpg",
  "data": "2025-08-15T20:00:00",
  "horario": "21:00",
  "id": 1,
  "created_at": "2025-07-23T11:33:42"
}
```

### 8. Deletar Relacionamento Específico
```bash
curl -X DELETE "http://localhost:8000/api/v1/space-event-types/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "Relacionamento 1 foi deletado com sucesso"
}
```

### 9. Deletar Todos os Relacionamentos de um Espaço
```bash
curl -X DELETE "http://localhost:8000/api/v1/space-event-types/space/1" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "Todos os relacionamentos do espaço 1 foram deletados com sucesso"
}
```

### 10. Deletar Todos os Relacionamentos de um Tipo de Evento
```bash
curl -X DELETE "http://localhost:8000/api/v1/space-event-types/event-type/2" \
  -H "Authorization: Bearer <TOKEN>"
```

**Resposta:**
```json
{
  "message": "Todos os relacionamentos do tipo de evento 2 foram deletados com sucesso"
}
```

### Observações Importantes

1. **Validações:**
   - O espaço e o tipo de evento devem existir antes de criar o relacionamento
   - Os campos `tema`, `descricao`, `data` e `horario` são obrigatórios
   - A data deve ser um datetime válido
   - Não há restrição de relacionamentos duplicados (um espaço pode ter múltiplos eventos do mesmo tipo)

2. **Campos de Banner:**
   - O campo `banner` armazena o path local da imagem (ex: `/static/banners/evento.jpg`)
   - As imagens devem ser salvas no diretório `static/banners/` do projeto
   - O servidor está configurado para servir arquivos estáticos em `/static/`

3. **Operações em Lote:**
   - É possível deletar todos os relacionamentos de um espaço específico
   - É possível deletar todos os relacionamentos de um tipo de evento específico
   - Útil para limpeza ou alterações massivas

4. **Flexibilidade:**
   - Permite múltiplos eventos do mesmo tipo em um espaço
   - Campos opcionais para link de divulgação e banner
   - Atualização parcial de campos

5. **Casos de Uso:**
   - Criar eventos específicos para espaços
   - Gerenciar programação de eventos
   - Associar informações detalhadas a combinações espaço-evento
   - Controlar banners e divulgação por evento

---

## 🎭 Space-Festival Types (Relacionamentos N:N)

### Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/space-festival-types/` | Criar relacionamento |
| `GET` | `/api/v1/space-festival-types/` | Listar todos os relacionamentos |
| `GET` | `/api/v1/space-festival-types/{id}` | Obter por ID |
| `GET` | `/api/v1/space-festival-types/space/{space_id}` | Por espaço |
| `GET` | `/api/v1/space-festival-types/festival-type/{festival_type_id}` | Por tipo de festival |
| `GET` | `/api/v1/space-festival-types/space/{space_id}/festival-type/{festival_type_id}` | Combinação específica |
| `PUT` | `/api/v1/space-festival-types/{id}` | Atualizar relacionamento |
| `DELETE` | `/api/v1/space-festival-types/{id}` | Deletar relacionamento |
| `DELETE` | `/api/v1/space-festival-types/space/{space_id}` | Deletar por espaço |
| `DELETE` | `/api/v1/space-festival-types/festival-type/{festival_type_id}` | Deletar por tipo |

### Estrutura do Relacionamento

```json
{
  "id": 1,
  "space_id": 1,
  "festival_type_id": 1,
  "tema": "Rock Paulista dos Anos 80",
  "descricao": "Festival dedicado ao rock nacional paulista dos anos 80",
  "link_divulgacao": "https://rockpaulista80.com.br",
  "banner": "static/banners/rock_paulista_80.jpg",
  "data": "2024-07-15T20:00:00",
  "horario": "20:00-02:00",
  "created_at": "2025-07-23T12:28:59"
}
```

### Criar Relacionamento

```bash
curl -X POST "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "space_id": 1,
    "festival_type_id": 2,
    "tema": "Blues & Jazz Night",
    "descricao": "Noite especial com apresentações de blues e jazz",
    "link_divulgacao": "https://bluesjazznight.com",
    "banner": "static/banners/blues_jazz_night.jpg",
    "data": "2024-08-20T19:00:00",
    "horario": "19:00-01:00"
  }'
```

### Listar Todos os Relacionamentos

```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Buscar por Espaço

```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/space/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Buscar por Tipo de Festival

```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/festival-type/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Buscar Combinação Específica

```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/space/1/festival-type/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Atualizar Relacionamento

```bash
curl -X PUT "http://localhost:8000/api/v1/space-festival-types/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Rock Paulista Clássico - ATUALIZADO",
    "descricao": "Descrição atualizada do festival",
    "banner": "static/banners/rock_paulista_novo.jpg"
  }'
```

### Deletar Relacionamento

```bash
curl -X DELETE "http://localhost:8000/api/v1/space-festival-types/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Deletar por Espaço (Em Lote)

```bash
curl -X DELETE "http://localhost:8000/api/v1/space-festival-types/space/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Deletar por Tipo de Festival (Em Lote)

```bash
curl -X DELETE "http://localhost:8000/api/v1/space-festival-types/festival-type/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Validações

- **Campos obrigatórios**: `space_id`, `festival_type_id`, `tema`, `descricao`, `data`, `horario`
- **Campos opcionais**: `link_divulgacao`, `banner`
- **Foreign keys**: Validação de existência de espaços e tipos de festivais
- **Formato de data**: ISO 8601 (ex: "2024-07-15T20:00:00")

### Respostas de Erro

```json
// Campos obrigatórios vazios
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "tema"],
      "msg": "Value error, Tema é obrigatório",
      "input": ""
    }
  ]
}

// Foreign key inexistente
{
  "detail": "Espaço com ID 999 não encontrado"
}

// Relacionamento não encontrado
{
  "detail": "Relacionamento não encontrado"
}
```

---

## 📊 Códigos de Status HTTP