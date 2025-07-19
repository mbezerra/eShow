# Controle de Versão - eShow API

## Versão Atual
**v0.1.0** - Initial release

## Estrutura de Versionamento
Utilizamos [Semantic Versioning (SemVer)](https://semver.org/) para controle de versão:

- **MAJOR.MINOR.PATCH**
  - **MAJOR**: Mudanças incompatíveis na API
  - **MINOR**: Novas funcionalidades compatíveis
  - **PATCH**: Correções de bugs compatíveis

## Histórico de Versões

### v0.1.0 (2024-07-19)
- **Initial release**
- Arquitetura hexagonal implementada
- Sistema de autenticação JWT
- Endpoints de usuários (CRUD completo)
- Endpoints de autenticação (login, registro, logout, refresh)
- Banco de dados SQLite para desenvolvimento
- Documentação completa da API
- Sistema de blacklist de tokens
- Health check com informações da aplicação

## Como Fazer Release de Nova Versão

### 1. Atualizar a versão
```bash
# Editar app/core/config.py
APP_VERSION: str = os.getenv("APP_VERSION", "X.Y.Z")
```

### 2. Commit das mudanças
```bash
git add .
git commit -m "vX.Y.Z: Descrição das mudanças"
```

### 3. Criar tag
```bash
git tag -a vX.Y.Z -m "Version X.Y.Z - Descrição"
```

### 4. Push para repositório remoto (quando configurado)
```bash
git push origin master
git push origin vX.Y.Z
```

## Convenções de Commit

- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Documentação
- **style**: Formatação de código
- **refactor**: Refatoração
- **test**: Testes
- **chore**: Tarefas de manutenção

### Exemplo
```bash
git commit -m "feat: add user profile endpoint"
git commit -m "fix: resolve authentication token issue"
git commit -m "docs: update API documentation"
```

## Tags Git

As tags são usadas para marcar releases específicos:

```bash
# Listar tags
git tag -l

# Ver detalhes de uma tag
git show v0.1.0

# Checkout de uma versão específica
git checkout v0.1.0
```

## Próximas Versões Planejadas

### v0.2.0
- Migração para PostgreSQL
- Sistema de logs estruturado
- Testes automatizados
- Rate limiting

### v1.0.0
- API estável para produção
- Documentação completa
- Performance otimizada
- Monitoramento e métricas 