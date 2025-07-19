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

## Endpoints Públicos

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
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