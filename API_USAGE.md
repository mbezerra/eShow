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
    "profile_id": 1,
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