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
    "telefone_fixo": "(11) 3333-4444",
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