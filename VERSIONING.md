# Controle de Versão - eShow API

## Versão Atual
**v0.13.5** (2025-01-23) - Correção do ProfileService

> **Atualização Recente:** Versão patch incrementada para v0.13.5 com correção do método get_profile_by_user_id no ProfileService.

- **SISTEMA DE INTERESTS COMPLETO**: Sistema de manifestações de interesse implementado
  - ✅ 15 endpoints REST funcionais com autenticação JWT
  - ✅ Gestão de manifestações bidirecionais (artista→espaço, espaço→artista)
  - ✅ Sistema de status com 3 estados: "AGUARDANDO_CONFIRMACAO", "ACEITO", "RECUSADO"
  - ✅ Validação de roles: apenas artistas podem manifestar interesse em espaços e vice-versa
  - ✅ Prevenção de duplicatas: constraint UNIQUE para evitar manifestações duplicadas
  - ✅ Validações robustas: data futura, duração 0.5-8h, valores positivos, mensagem obrigatória
  - ✅ Endpoints especializados para aceitar/rejeitar manifestações
  - ✅ Consultas por profile (enviadas, recebidas, pendentes)
  - ✅ Estatísticas detalhadas por profile
  - ✅ Filtros avançados por status, tipo de evento e período
  - ✅ Relacionamentos com profiles, space_event_types e space_festival_types
  - ✅ Parâmetro `include_relations=true` para dados relacionados
  - ✅ Migração de banco aplicada (tabela interests)
  - ✅ 17 manifestações de exemplo com diferentes status
- **DOCUMENTAÇÃO ATUALIZADA**: Todos os 6 arquivos .md sincronizados
  - README.md: Seção Interests completa com 15 endpoints e regras de negócio
  - ARCHITECTURE.md: Entidade Interest, repositórios e relacionamentos incluídos
  - IMPLEMENTATION_SUMMARY.md: Seção v0.12.0 detalhada com sistema Interests
  - DATABASE_STRATEGY.md: DDL da tabela interests, consultas SQL e validações
  - API_USAGE.md: Guia prático completo com exemplos curl para Interests
  - VERSIONING.md: Changelog atualizado com marcos v0.12.0
  - Estatísticas atualizadas: **134 endpoints**, **17 entidades**, **75+ schemas**
- **ARQUITETURA HEXAGONAL MADURA**: Padrões estabelecidos seguidos fielmente
  - Separação clara de responsabilidades (Domain, Application, Infrastructure)
  - Validações de negócio robustas na camada de domínio
  - Repository Pattern com suporte a `include_relations`
  - Service Layer com lógica de aplicação bem estruturada
  - Schemas Pydantic com validações específicas por contexto
  - Tratamento de erros padronizado e informativo

> **Marco de Desenvolvimento:** A v0.13.5 marca a versão patch atualizada com correção do método get_profile_by_user_id no ProfileService. O projeto agora possui 134 endpoints funcionais, 17 entidades de domínio e documentação técnica totalmente sincronizada.

### v0.13.4 (2025-01-23) - Correção do Enum StatusInterest

- **CORREÇÃO CRÍTICA**: Resolvido problema de incompatibilidade entre enum e banco de dados
  - ✅ Corrigido enum StatusInterest para usar valores sem acentos
  - ✅ Atualizado valores de "Aguardando Confirmação" para "AGUARDANDO_CONFIRMACAO"
  - ✅ Atualizado valores de "Aceito" para "ACEITO" e "Recusado" para "RECUSADO"
  - ✅ Corrigidas mensagens de erro para usar os novos valores
  - ✅ Atualizada documentação da API com os valores corretos
  - ✅ Resolvido erro LookupError no sistema de interests
  - ✅ Garantida compatibilidade entre código e banco de dados
- **DADOS RECRIADOS**: Limpeza e recriação dos dados de exemplo
  - ✅ Removidos dados antigos com valores incorretos
  - ✅ Recriados 17 registros de exemplo com os novos valores
  - ✅ Sistema de interests 100% funcional
- **TESTES REALIZADOS**: Validação completa da correção
  - ✅ Consulta direta ao banco funcionando
  - ✅ API endpoints operacionais
  - ✅ Parâmetro include_relations funcionando corretamente

> **Correção Técnica:** A v0.13.4 resolve um problema crítico de compatibilidade entre o enum StatusInterest e o banco de dados, garantindo que o sistema de interests funcione corretamente com o parâmetro include_relations.

### v0.13.5 (2025-01-23) - Correção do ProfileService

- **CORREÇÃO CRÍTICA**: Resolvido erro AttributeError no endpoint DELETE de interests
  - ✅ Adicionado método get_by_user_id ao ProfileRepository interface
  - ✅ Implementado método get_by_user_id no ProfileRepositoryImpl
  - ✅ Adicionado método get_profile_by_user_id ao ProfileService
  - ✅ Corrigido erro AttributeError: 'ProfileService' object has no attribute 'get_profile_by_user_id'
  - ✅ Garantido que endpoints de interests possam obter profile do usuário logado
  - ✅ Mantida compatibilidade com arquitetura hexagonal existente
- **TESTES REALIZADOS**: Validação completa da correção
  - ✅ Endpoint DELETE de interests funcionando corretamente
  - ✅ Validação de autorização (apenas quem criou pode deletar)
  - ✅ Validação de status (apenas AGUARDANDO_CONFIRMACAO pode ser deletado)
  - ✅ Mensagens de erro apropriadas retornadas

> **Correção Técnica:** A v0.13.5 resolve um erro crítico no endpoint DELETE do sistema de interests, adicionando o método get_profile_by_user_id ao ProfileService para permitir que os endpoints obtenham o profile do usuário logado.

### v0.11.1 (2025-01-23) - Refinamentos no Sistema de Bookings e Documentação Atualizada

- **MELHORIAS NO SISTEMA DE BOOKINGS**: Refinamentos e otimizações implementadas
  - ✅ Aprimoramentos no serviço de bookings (booking_service.py)
  - ✅ Otimizações nas dependências da aplicação (dependencies.py)
  - ✅ Script de inicialização de bookings atualizado (init_bookings.py)
- **DOCUMENTAÇÃO SINCRONIZADA**: Arquivos de documentação atualizados
  - API_USAGE.md: Exemplos e guias práticos atualizados
  - IMPLEMENTATION_SUMMARY.md: Resumo técnico sincronizado com v0.11.1
  - VERSIONING.md: Changelog atualizado com marcos v0.11.1
- **VERSIONAMENTO AUTOMATIZADO**: Sistema de tags Git implementado
  - Tag v0.11.1 criada e sincronizada com repositório remoto
  - Processo automatizado de incremento de versão patch
  - Controle de versão padronizado seguindo semver

> **Atualização Técnica:** A v0.11.1 foca em refinamentos e melhorias de qualidade no sistema de bookings, mantendo a estabilidade de 119 endpoints e 16 entidades de domínio.

### v0.11.0 (2025-07-23) - Sistema Financial Implementado e Documentação Atualizada [MARCO ANTERIOR]

### v0.10.3 (2025-07-23) - Sistema de Avaliações/Reviews Completo

- **SISTEMA DE REVIEWS**: Implementação completa do sistema de avaliações
  - 11 endpoints REST: CRUD completo + filtros avançados + estatísticas
  - Avaliações com notas de 1-5 estrelas e depoimento obrigatório (10-1000 caracteres)
  - Relacionamentos com profiles, space_event_types e space_festival_types
  - Regra de negócio: relacionamento exclusivo (OU evento OU festival, nunca ambos)
  - Cálculo automático de média de avaliações por profile
  - Filtros por profile, nota, período, tipo de evento/festival
  - Parâmetro `include_relations=true` para dados relacionados
  - Migração do banco aplicada (tabela reviews criada)
  - Dados de exemplo: 6 reviews com distribuição de notas variadas
- **ARQUITETURA HEXAGONAL**: Seguindo os padrões estabelecidos
  - Entidade Review com validações de domínio
  - ReviewRepository interface + ReviewRepositoryImpl
  - ReviewService com regras de negócio
  - Schemas Pydantic robustos com validações
  - Endpoints com tratamento completo de erros

### v0.10.1 (2025-07-23) - Sistema de Bookings Completo e Testes da API

- **SISTEMA DE BOOKINGS**: Implementação completa do sistema de agendamentos
  - 4 tipos de booking: Artista→Espaço, Espaço→Artista, Evento Específico, Festival Específico
  - Validações de regras de negócio por role: ADMIN não pode agendar, ARTISTA só agenda espaços, ESPAÇO só agenda artistas
  - Filtros especializados: por profile, espaço, artista, evento, festival, período de datas
  - CRUD completo com endpoints otimizados
- **TESTES COMPLETOS**: Validação exaustiva de todos os endpoints da API
  - Autenticação JWT: registro, login, refresh token - 100% funcional
  - Sistema de bookings: 15+ endpoints testados com sucesso
  - Validações de negócio: mensagens de erro corretas implementadas
  - Filtros e consultas: todos os endpoints de consulta funcionando
- **DOCUMENTAÇÃO**: API_USAGE.md atualizada com prefixos corretos (/api/v1/)
- **VERSIONAMENTO**: Sistema automático de versionamento via Git tags implementado
- **ARQUITETURA**: API executando perfeitamente com arquitetura hexagonal

> **Nota sobre Versionamento:** A partir da v0.10.1, o projeto adotou um sistema de versionamento automático baseado em Git tags. As versões intermediárias (v0.8.x, v0.9.x, v0.10.0) foram incrementos de desenvolvimento que culminaram na implementação completa do sistema de bookings e testes exaustivos da API. O salto de versão reflete a maturidade alcançada pelo sistema.

### v0.7.4 (2025-07-23)
- **Sistema de Controle de Acesso por Roles**
- **NOVA FUNCIONALIDADE**: Sistema de validação de roles implementado
- **Artists**: Apenas profiles com `role_id = 2` (role "ARTISTA") podem cadastrar artistas
- **Spaces**: Apenas profiles com `role_id = 3` (role "ESPACO") podem cadastrar espaços
- Validação implementada nos serviços ArtistService e SpaceService
- Integração com ProfileRepository para verificação de roles
- Mensagens de erro claras: "Apenas perfis com role 'X' podem cadastrar Y"
- Dados de exemplo reestruturados com profiles válidos por role
- Novos usuários e profiles criados: 4 ARTISTA + 4 ESPACO
- Documentação atualizada com novas restrições
- Validação aplicada tanto na criação quanto na atualização

### v0.7.3 (2025-07-23)
- **Correção do endpoint PUT de Spaces**
- Implementação de atualização parcial para Spaces
- Todos os campos do SpaceUpdate agora são opcionais
- Uso de `model_dump(exclude_none=True)` para filtrar campos None
- Correção de validação de atualização parcial no SpaceService
- Documentação atualizada com exemplo de resposta
- Funcionalidade de atualização parcial totalmente operacional

### v0.7.2 (2025-07-23)
- **Correção do parâmetro include_relations**
- `include_relations=false`: Retorna apenas campos básicos (21 campos)
- `include_relations=true`: Retorna campos básicos + relacionamentos (25 campos)
- Removidos response_models fixos dos endpoints GET de Spaces
- Entidade Space limpa sem atributos de relacionamento desnecessários
- Performance otimizada: relacionamentos só são carregados quando solicitados
- Correção aplicada a todos os endpoints GET de Spaces

### v0.7.1 (2025-07-23)
- **Spaces e parâmetro include_relations**
- Implementação completa dos endpoints Spaces (CRUD)
- Entidade Space com relacionamentos para profiles, space_types, event_types e festival_types
- Parâmetro `include_relations=true` para Artists e Spaces
- Carregamento otimizado de relacionamentos usando SQLAlchemy joinedload
- Schemas específicos para relacionamentos (ProfileRelation, SpaceTypeRelation, etc.)
- Validação de enums para acesso (Público/Privado) e público estimado
- Suporte a arrays JSON para dias de apresentação e fotos
- Script de inicialização com dados de exemplo
- Migração Alembic para tabela spaces
- Documentação completa atualizada em todos os arquivos
- Performance otimizada evitando N+1 queries

### v0.7.0 (2025-07-22)
- **Festival Types e expansão completa do sistema**
- Implementação completa dos endpoints Festival Types (CRUD)
- 14 tipos de festival pré-cadastrados (Aniversário de Emancipação Política, Festa Religiosa, etc.)
- Validação de unicidade de tipos de festival
- Flexibilidade para adicionar novos tipos de festival
- Padrão consistente com outros endpoints
- Script de inicialização automática
- Documentação completa atualizada (API_USAGE.md)
- Migração Alembic para tabela festival_types
- Dados iniciais populados automaticamente

### v0.6.0 (2025-07-22)
- **Event Types e expansão do sistema**
- Implementação completa dos endpoints Event Types (CRUD)
- 7 tipos de evento pré-cadastrados (Aniversário, Casamento, Formatura, etc.)
- Validação de unicidade de tipos de evento
- Flexibilidade para adicionar novos tipos de evento
- Padrão consistente com outros endpoints
- Script de inicialização automática
- Documentação completa atualizada (API_USAGE.md)
- Migração Alembic para tabela event_types
- Dados iniciais populados automaticamente

### v0.5.0 (2025-07-22)
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

### v0.4.0 (2025-07-22)
- **Relacionamento N:N Artists-Musical Styles, testes e limpeza**
- Implementação completa dos endpoints N:N entre Artists e Musical Styles
- Testes automatizados dos novos endpoints
- População e consulta dos relacionamentos
- Limpeza de arquivos de teste temporários
- Ajustes finais e documentação

### v0.3.0 (2025-07-19)
- **Artists endpoints with relationships**
- Endpoints de Artists (CRUD completo)
- Relacionamentos Profile e Artist Type
- Parâmetro `include_relations` para carregar dados relacionados
- Validação de dados com Pydantic
- Documentação atualizada com exemplos práticos
- Scripts de migração atualizados
- Testes automatizados para relacionamentos

### v0.2.0 (2025-07-19)
- **Enhanced user management**
- Endpoints de Profiles (CRUD completo)
- Endpoints de Roles (CRUD completo)
- Endpoints de Artist Types (CRUD completo)
- Endpoints de Musical Styles (CRUD completo)
- Sistema de relacionamentos entre entidades
- Validação avançada de dados

### v0.1.1 (2025-07-19)
- **Bug fixes and improvements**
- Correções no sistema de autenticação
- Melhorias na documentação
- Otimizações de performance

### v0.1.0 (2025-07-19)
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

### v0.12.0 ✅ **CONCLUÍDA**
- Sistema de manifestações de interesse (Interests)
- Conexão entre artistas e espaços
- Gestão de status e respostas
- Filtros e estatísticas avançadas

### v0.13.0 ✅ **CONCLUÍDA**
- Versão minor atualizada
- Sistema de manifestações de interesse totalmente implementado
- Documentação completa sincronizada
- Versionamento automático funcionando

### v0.13.1 ✅ **CONCLUÍDA**
- Correções no sistema de reviews implementadas
- Regras de negócio: ADMIN não pode criar reviews
- Profile_id determinado automaticamente pelo usuário logado
- Tabela reviews limpa e populada com 12 reviews corretos
- Documentação atualizada em todos os arquivos .md

### v0.13.3 ✅ **CONCLUÍDA**
- Padronização dos endpoints DELETE para retornar mensagens de sucesso
- Correção dos endpoints DELETE de reviews, interests e financials
- Status code padronizado para 200 OK com mensagem informativa
- Melhoria na experiência do usuário com feedback claro sobre operações de exclusão
- Todos os endpoints DELETE agora seguem o mesmo padrão de resposta

### v0.13.2 ✅ **CONCLUÍDA**
- Correção do parâmetro include_relations nos endpoints de reviews
- Remoção de Union de response_model que causava problemas de serialização
- Dados relacionados (profile, space_event_type, space_festival_type) agora funcionam corretamente
- Todos os endpoints de reviews testados e funcionando

### v0.14.0
- Sistema de notificações em tempo real
- Upload de arquivos e mídias
- Sistema de pagamentos integrado
- Cache Redis para performance

### v0.14.0
- Interface web de administração
- Relatórios avançados
- Sistema de métricas e analytics
- Backup automático de dados

### v1.0.0
- API estável para produção
- Documentação completa
- Performance otimizada
- Monitoramento e métricas 
- Certificação de qualidade para produção 

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
Versão atual: 0.13.3

# Criar nova versão patch
$ python version.py patch
Versão atual: 0.13.3
Nova versão: 0.13.4
Deseja criar a tag e fazer push? (y/N): y
Tag criada: v0.13.1
Tag enviada para o repositório remoto: v0.13.1
✅ Versão 0.13.1 criada com sucesso!
📦 A API agora usará automaticamente a versão 0.13.1
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
    "timestamp": "2025-07-23T13:21:51.256633",
    "version": "0.13.3",
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