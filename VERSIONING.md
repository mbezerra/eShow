# Controle de Versão - eShow API

## Versão Atual
**v0.6.0** - Event Types e expansão do sistema

- Implementação completa dos endpoints Event Types (CRUD)
- 7 tipos de evento pré-cadastrados (Aniversário, Casamento, Formatura, etc.)
- Validação de unicidade de tipos de evento
- Flexibilidade para adicionar novos tipos de evento
- Padrão consistente com outros endpoints
- Script de inicialização automática
- Documentação completa atualizada (API_USAGE.md)
- Migração Alembic para tabela event_types
- Dados iniciais populados automaticamente

### v0.5.0 (2024-07-22)
- **Space Types e melhorias de infraestrutura**
- Implementação completa dos endpoints Space Types (CRUD)
- 15 tipos de espaço pré-cadastrados (Bar, Restaurante, Clube, etc.)
- Resolução do problema de compatibilidade do bcrypt
- Script de inicialização `start_server.sh` para facilitar desenvolvimento
- Ambiente virtual configurado corretamente
- Padrão consistente nos endpoints DELETE (mensagens de sucesso)
- Documentação completa atualizada (API_USAGE.md)
- Migração Alembic para tabela space_types
- Dados iniciais populados automaticamente

### v0.4.0 (2024-07-22)
- **Relacionamento N:N Artists-Musical Styles, testes e limpeza**
- Implementação completa dos endpoints N:N entre Artists e Musical Styles
- Testes automatizados dos novos endpoints
- População e consulta dos relacionamentos
- Limpeza de arquivos de teste temporários
- Ajustes finais e documentação

### v0.3.0 (2024-07-19)
- **Artists endpoints with relationships**
- Endpoints de Artists (CRUD completo)
- Relacionamentos Profile e Artist Type
- Parâmetro `include_relations` para carregar dados relacionados
- Validação de dados com Pydantic
- Documentação atualizada com exemplos práticos
- Scripts de migração atualizados
- Testes automatizados para relacionamentos

### v0.2.0 (2024-07-19)
- **Enhanced user management**
- Endpoints de Profiles (CRUD completo)
- Endpoints de Roles (CRUD completo)
- Endpoints de Artist Types (CRUD completo)
- Endpoints de Musical Styles (CRUD completo)
- Sistema de relacionamentos entre entidades
- Validação avançada de dados

### v0.1.1 (2024-07-19)
- **Bug fixes and improvements**
- Correções no sistema de autenticação
- Melhorias na documentação
- Otimizações de performance

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

# Sistema de Versionamento Automático

O projeto eShow utiliza um sistema de versionamento automático baseado em tags do Git. A versão da API é automaticamente detectada a partir da tag mais recente do repositório.

## Como Funciona

1. **Detecção Automática**: A API detecta automaticamente a versão atual baseada na tag Git mais recente
2. **Fallback**: Se não houver tags, usa o hash do commit atual com prefixo `dev-`
3. **Fallback Final**: Se não conseguir acessar o Git, usa a versão padrão `0.1.0`

## Script de Versionamento

O projeto inclui um script `version.py` para facilitar o gerenciamento de versões:

### Comandos Disponíveis

```bash
# Mostrar versão atual
python version.py show

# Incrementar versão patch (0.1.0 -> 0.1.1)
python version.py patch

# Incrementar versão minor (0.1.0 -> 0.2.0)
python version.py minor

# Incrementar versão major (0.1.0 -> 1.0.0)
python version.py major
```

### Exemplo de Uso

```bash
# Verificar versão atual
$ python version.py show
Versão atual: 0.1.1

# Criar nova versão patch
$ python version.py patch
Versão atual: 0.1.1
Nova versão: 0.1.2
Deseja criar a tag e fazer push? (y/N): y
Tag criada: v0.1.2
Tag enviada para o repositório remoto: v0.1.2
✅ Versão 0.1.2 criada com sucesso!
📦 A API agora usará automaticamente a versão 0.1.2
```

## Convenções de Versionamento

O projeto segue o padrão [Semantic Versioning (SemVer)](https://semver.org/):

- **MAJOR**: Mudanças incompatíveis com versões anteriores
- **MINOR**: Novas funcionalidades compatíveis com versões anteriores
- **PATCH**: Correções de bugs compatíveis com versões anteriores

### Exemplos

- `1.0.0` - Primeira versão estável
- `1.1.0` - Nova funcionalidade adicionada
- `1.1.1` - Correção de bug
- `2.0.0` - Mudança que quebra compatibilidade

## Verificação da Versão

A versão atual pode ser verificada através do endpoint `/health`:

```bash
curl http://localhost:8000/health
```

Resposta:
```json
{
    "status": "healthy",
    "architecture": "hexagonal",
    "timestamp": "2025-07-21T13:23:40.081315",
    "version": "0.1.1",
    "copyright": "© 2025 eShow. Todos os direitos reservados."
}
```

## Configuração Manual

Se necessário, a versão pode ser definida manualmente através da variável de ambiente `APP_VERSION` no arquivo `.env`:

```env
APP_VERSION=1.0.0
```

**Nota**: A variável de ambiente tem prioridade sobre a detecção automática do Git.

## Fluxo de Trabalho Recomendado

1. **Desenvolvimento**: Trabalhe normalmente nos commits
2. **Release**: Quando estiver pronto para uma nova versão:
   ```bash
   # Faça commit de todas as mudanças
   git add .
   git commit -m "Descrição das mudanças"
   
   # Crie a nova versão
   python version.py patch  # ou minor/major
   ```
3. **Deploy**: A API automaticamente usará a nova versão após reiniciar

## Benefícios

- ✅ **Automatização**: Não precisa lembrar de atualizar versões manualmente
- ✅ **Consistência**: Versão sempre sincronizada com o Git
- ✅ **Rastreabilidade**: Cada versão tem uma tag Git correspondente
- ✅ **Flexibilidade**: Suporte a desenvolvimento e produção
- ✅ **Padrão**: Segue convenções da indústria (SemVer) 