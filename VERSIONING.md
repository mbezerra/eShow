# Controle de Versão - eShow API

## Versão Atual
**v0.18.1** (2025-01-25) - Correção do LocationUtils e Refatoração Completa

> **Atualização Recente:** Versão patch incrementada para v0.18.1 com correção crítica do LocationUtils e refatoração completa.

- **REFATORAÇÃO COMPLETA DO LOCATIONUTILS**: Correção crítica e eliminação de hard coded
  - ✅ **Eliminação de hard coded**: Removidos todos os mapeamentos manuais de CEPs
  - ✅ **Base de dados primária**: Uso exclusivo da tabela cep_coordinates (4111 CEPs, 3928 cidades)
  - ✅ **ViaCEP como redundância**: API externa apenas para CEPs não cadastrados
  - ✅ **Correção de formato**: CEPs formatados corretamente com hífen para busca local
  - ✅ **Cache otimizado**: Sistema de cache para evitar consultas repetidas
  - ✅ **Salvamento automático**: CEPs obtidos via ViaCEP são salvos na base local
  - ✅ **Tratamento robusto**: Validações e tratamento de erros aprimorados
  - ✅ **Performance melhorada**: Consultas diretas na base local sem fallbacks desnecessários
  - ✅ **Confiabilidade**: Sistema baseado em dados reais da base IBGE
  - ✅ **Manutenibilidade**: Código limpo e sem dependências de dados hard coded
- **SISTEMA DE BUSCA POR LOCALIZAÇÃO FUNCIONAL**: Endpoints operacionais após correção
  - ✅ **4 endpoints REST funcionais**: Busca de espaços e artistas por localização
  - ✅ **Cálculo de distância preciso**: Fórmula de Haversine com dados reais
  - ✅ **Validação de disponibilidade**: Status CONTRATANDO para eventos/festivais
  - ✅ **Verificação de conflitos**: Agendamentos conflitantes para artistas
  - ✅ **Autenticação e autorização**: Por role (artista/espaço) com JWT
  - ✅ **Parâmetros configuráveis**: return_full_data, max_results
  - ✅ **Respostas estruturadas**: Metadados de busca e resultados organizados
  - ✅ **Arquitetura hexagonal**: Padrões mantidos em todas as camadas
- **ARQUITETURA HEXAGONAL MADURA**: Padrões estabelecidos seguidos fielmente
  - LocationUtils refatorado com base de dados primária e ViaCEP como redundância
  - LocationSearchService com lógica de negócio robusta e validada
  - Schemas Pydantic com validações específicas para busca geográfica
  - Repository Pattern com métodos especializados para coordenadas
  - Service Layer com orquestração de múltiplos repositórios
  - Tratamento de exceções padronizado e informativo

> **Marco de Correção:** A v0.18.1 marca a versão patch com correção crítica do LocationUtils. O sistema agora usa primariamente a base de dados local (4111 CEPs) com ViaCEP como redundância, eliminando todos os hard coded e garantindo confiabilidade e manutenibilidade.

### v0.18.1 (2025-01-25) - Correção do LocationUtils e Refatoração Completa

- **CORREÇÃO CRÍTICA DO LOCATIONUTILS**: Refatoração completa e eliminação de hard coded
  - ✅ **Problema identificado**: Formato de CEP incorreto na busca local
  - ✅ **Hard coded removidos**: Eliminados todos os mapeamentos manuais de CEPs
  - ✅ **Base de dados primária**: Uso exclusivo da tabela cep_coordinates (4111 CEPs, 3928 cidades)
  - ✅ **ViaCEP como redundância**: API externa apenas para CEPs não cadastrados
  - ✅ **Formato corrigido**: CEPs formatados com hífen para busca local
  - ✅ **Cache otimizado**: Sistema de cache para evitar consultas repetidas
  - ✅ **Salvamento automático**: CEPs obtidos via ViaCEP são salvos na base local
  - ✅ **Performance melhorada**: Consultas diretas sem fallbacks desnecessários
  - ✅ **Confiabilidade**: Sistema baseado em dados reais da base IBGE
  - ✅ **Manutenibilidade**: Código limpo sem dependências de dados hard coded

- **SISTEMA DE BUSCA FUNCIONAL**: Endpoints operacionais após correção
  - ✅ **Teste realizado**: Script de diagnóstico criado e executado com sucesso
  - ✅ **2 espaços encontrados**: Dentro do raio de 50km do artista (48400-000)
  - ✅ **Distâncias calculadas**: 30.68km para espaços em Cícero Dantas (48100-000)
  - ✅ **Validação completa**: Eventos CONTRATANDO verificados corretamente
  - ✅ **Arquitetura mantida**: Padrões hexagonais preservados em todas as camadas

- **DOCUMENTAÇÃO ATUALIZADA**: VERSIONING.md atualizado com correção
  - ✅ **Changelog atualizado**: Versão 0.18.1 documentada com detalhes técnicos
  - ✅ **Problemas identificados**: Formato de CEP e hard coded documentados
  - ✅ **Soluções implementadas**: Refatoração e correção detalhadas
  - ✅ **Resultados validados**: Sistema testado e funcionando corretamente

> **Marco de Correção:** A v0.18.1 resolveu problemas críticos no LocationUtils, eliminando hard coded e corrigindo formato de CEP. O sistema agora é confiável, baseado em dados reais e mantém a arquitetura hexagonal.

### v0.17.0 (2025-01-24) - Estabilização e Documentação Completa

- **ESTABILIZAÇÃO COMPLETA**: Versão minor com foco em estabilização e documentação
  - ✅ **Tag Git v0.16.0**: Criada e sincronizada com repositório remoto
  - ✅ **Documentação Atualizada**: Todas as 6 documentações principais sincronizadas
  - ✅ **Testes Realizados**: Sistema testado via API com validação completa
  - ✅ **Arquitetura Documentada**: Padrões hexagonais mantidos e documentados
  - ✅ **Performance Otimizada**: Otimizações de banco e consultas implementadas
  - ✅ **Escalabilidade**: Considerações para cache e índices espaciais documentadas

- **MELHORIAS DE DOCUMENTAÇÃO**:
  - **README.md**: Atualizado com estatísticas v0.17.0 e seção Location Search
  - **ARCHITECTURE.md**: Sistema de Location Search detalhado com componentes
  - **DATABASE_STRATEGY.md**: Estrutura de dados e otimizações para busca geográfica
  - **VERSIONING.md**: Changelog atualizado com marcos v0.16.0 e v0.17.0
  - **API_USAGE.md**: Guia prático completo para endpoints de busca
  - **IMPLEMENTATION_SUMMARY.md**: Resumo técnico atualizado para v0.17.0

- **ESTABILIZAÇÃO TÉCNICA**:
  - **Versionamento**: Sistema automático funcionando corretamente
  - **Dependências**: requests==2.31.0 adicionada para integração ViaCEP
  - **Repositórios**: Métodos especializados implementados e testados
  - **Serviços**: LocationSearchService com lógica robusta e validada
  - **Schemas**: Estruturas padronizadas para requisições e respostas
  - **Endpoints**: 4 endpoints funcionais com autenticação e autorização

> **Marco de Estabilização:** A v0.17.0 marca a versão minor com foco em estabilização e documentação completa. O sistema de busca por localização está totalmente funcional, testado e documentado, com todas as 6 documentações principais sincronizadas e atualizadas.

### v0.15.0 (2025-01-24) - Campo Status em Space Festival Types

> **Atualização Recente:** Versão minor incrementada para v0.15.0 com implementação do campo status em Space Festival Types e documentação completa.

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

> **Marco de Desenvolvimento:** A v0.14.0 marca a versão minor com implementação do campo status em Space Event Types. O projeto agora possui 134 endpoints funcionais, 17 entidades de domínio e documentação técnica totalmente sincronizada.

### v0.14.0 (2025-01-24) - Campo Status em Space Event Types

- **NOVO CAMPO STATUS**: Implementação completa do campo status em Space Event Types
  - ✅ Enum StatusEventType com 4 valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
  - ✅ Campo status adicionado à entidade SpaceEventType com valor padrão CONTRATANDO
  - ✅ Validação para garantir que o status seja um valor válido do enum
  - ✅ Coluna status no modelo de banco com tipo SQLAlchemyEnum e valor padrão
  - ✅ Schemas Pydantic atualizados para incluir o campo status
  - ✅ Schema específico SpaceEventTypeStatusUpdate para atualização de status
  - ✅ Método update_status() no repositório para atualização específica
  - ✅ Serviço update_space_event_type_status() para atualização de status
  - ✅ Novo endpoint PATCH /{id}/status para atualização específica de status
  - ✅ Migração do Alembic aplicada com sucesso
  - ✅ Script de inicialização atualizado com diferentes status
- **CONSISTÊNCIA TOTAL**: Verificação completa em todos os endpoints relacionados
  - ✅ Endpoints diretos de Space Event Types atualizados
  - ✅ Endpoints de Reviews com relacionamentos verificados
  - ✅ Endpoints de Interests com relacionamentos verificados
  - ✅ Endpoints de Bookings com relacionamentos verificados
  - ✅ Schemas, serviços e repositórios consistentes
  - ✅ 100% de compatibilidade mantida
- **DOCUMENTAÇÃO COMPLETA**: Todas as documentações atualizadas
  - ✅ API_USAGE.md: Nova seção completa sobre Space Event Types
  - ✅ README.md: Seção "Funcionalidades Recentes" adicionada
  - ✅ IMPLEMENTATION_SUMMARY.md: Seção v0.14.0 detalhada
  - ✅ DATABASE_STRATEGY.md: Estrutura de dados e consultas SQL
  - ✅ ARCHITECTURE.md: Seção "Relacionamentos N:N" adicionada
  - ✅ STATUS_IMPLEMENTATION.md: Documentação específica da implementação
  - ✅ STATUS_CONSISTENCY_CHECK.md: Verificação de consistência
  - ✅ DOCUMENTATION_UPDATE_SUMMARY.md: Resumo das atualizações
- **ARQUITETURA ROBUSTA**: Implementação seguindo padrões estabelecidos
  - ✅ Separação clara de responsabilidades (Domain, Application, Infrastructure)
  - ✅ Validações de negócio na camada de domínio
  - ✅ Repository Pattern com método específico para status
  - ✅ Service Layer com lógica de aplicação bem estruturada
  - ✅ Schemas Pydantic com validações específicas
  - ✅ Endpoint RESTful seguindo convenções estabelecidas

> **Marco de Funcionalidade:** A v0.14.0 implementa o campo status em Space Event Types com controle granular do estado dos eventos. O sistema agora permite gerenciar eventos com 4 estados diferentes, mantendo consistência total em todos os endpoints relacionados e documentação completa atualizada.

### v0.15.0 (2025-01-24) - Campo Status em Space Festival Types

- **NOVO CAMPO STATUS**: Implementação completa do campo status em Space Festival Types
  - ✅ Enum StatusFestivalType com 4 valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
  - ✅ Campo status adicionado à entidade SpaceFestivalType com valor padrão CONTRATANDO
  - ✅ Validação para garantir que o status seja um valor válido do enum
  - ✅ Coluna status no modelo de banco com tipo SQLAlchemyEnum e valor padrão
  - ✅ Schemas Pydantic atualizados para incluir o campo status
  - ✅ Schema específico SpaceFestivalTypeStatusUpdate para atualização de status
  - ✅ Método update_status() no repositório para atualização específica
  - ✅ Serviço update_space_festival_type_status() para atualização de status
  - ✅ Novo endpoint PATCH /{id}/status para atualização específica de status
  - ✅ Migração do Alembic aplicada com sucesso
  - ✅ Script de inicialização atualizado com diferentes status
- **CONSISTÊNCIA TOTAL**: Verificação completa em todos os endpoints relacionados
  - ✅ Endpoints diretos de Space Festival Types atualizados
  - ✅ Endpoints de Reviews com relacionamentos verificados
  - ✅ Endpoints de Interests com relacionamentos verificados
  - ✅ Endpoints de Bookings com relacionamentos verificados
  - ✅ Schemas, serviços e repositórios consistentes
  - ✅ 100% de compatibilidade mantida
- **PADRÃO IDÊNTICO**: Mantida consistência total com Space Event Types
  - ✅ Mesmo enum com mesmos valores (CONTRATANDO, FECHADO, SUSPENSO, CANCELADO)
  - ✅ Mesma estrutura em todas as camadas (Domain, Application, Infrastructure)
  - ✅ Mesmo endpoint PATCH /{id}/status para atualização de status
  - ✅ Mesmas validações e regras de negócio
  - ✅ Mesma migração Alembic com server_default
  - ✅ Arquitetura hexagonal respeitada
- **DOCUMENTAÇÃO COMPLETA**: Todas as documentações atualizadas
  - ✅ API_USAGE.md: Nova seção completa sobre Space Festival Types
  - ✅ README.md: Seção "Funcionalidades Recentes" atualizada
  - ✅ IMPLEMENTATION_SUMMARY.md: Seção v0.15.0 detalhada
  - ✅ DATABASE_STRATEGY.md: Estrutura de dados e consultas SQL
  - ✅ ARCHITECTURE.md: Seção "Relacionamentos N:N" atualizada
  - ✅ SPACE_FESTIVAL_STATUS_IMPLEMENTATION.md: Documentação específica da implementação
  - ✅ SPACE_FESTIVAL_STATUS_CONSISTENCY_CHECK.md: Verificação de consistência
  - ✅ DOCUMENTATION_UPDATE_SUMMARY_SPACE_FESTIVAL.md: Resumo das atualizações
- **ARQUITETURA ROBUSTA**: Implementação seguindo padrões estabelecidos
  - ✅ Separação clara de responsabilidades (Domain, Application, Infrastructure)
  - ✅ Validações de negócio na camada de domínio
  - ✅ Repository Pattern com método específico para status
  - ✅ Service Layer com lógica de aplicação bem estruturada
  - ✅ Schemas Pydantic com validações específicas
  - ✅ Endpoint RESTful seguindo convenções estabelecidas

> **Marco de Funcionalidade:** A v0.15.0 implementa o campo status em Space Festival Types com controle granular do estado dos festivais. O sistema agora permite gerenciar festivais com 4 estados diferentes, mantendo consistência total com Space Event Types e documentação completa atualizada.

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

### v0.13.6 (2025-01-23) - Correção do Pool de Conexões

- **CORREÇÃO CRÍTICA**: Resolvido timeout do pool de conexões do banco de dados
  - ✅ Aumentado pool_size de 5 para 20 conexões
  - ✅ Aumentado max_overflow de 10 para 30 conexões
  - ✅ Aumentado pool_timeout de 30 para 60 segundos
  - ✅ Adicionado pool_recycle de 3600 segundos
  - ✅ Corrigido gerenciamento de dependências para usar Depends consistentemente
  - ✅ Adicionado rollback em caso de exceção no get_database_session
  - ✅ Resolvido erro: QueuePool limit of size 5 overflow 10 reached, connection timed out
  - ✅ Garantido que sessões sejam fechadas corretamente
- **TESTES REALIZADOS**: Validação completa da correção
  - ✅ Endpoint PATCH de interests funcionando corretamente
  - ✅ Validação de autorização (apenas pessoa de interesse pode aceitar/recusar)
  - ✅ Validação de status (apenas AGUARDANDO_CONFIRMACAO pode ser alterado)
  - ✅ Mensagens de erro apropriadas retornadas
  - ✅ Pool de conexões funcionando sem timeout

> **Correção Técnica:** A v0.13.6 resolve um problema crítico de timeout no pool de conexões do SQLAlchemy, aumentando os limites de conexões e corrigindo o gerenciamento de dependências para garantir que as sessões sejam fechadas corretamente.

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

### v0.17.0 ✅ **CONCLUÍDA**
- Estabilização e documentação completa
- Tag Git v0.16.0 criada e sincronizada
- Todas as 6 documentações principais atualizadas
- Sistema testado via API com validação completa
- Arquitetura documentada e otimizada
- Performance e escalabilidade documentadas

### v0.16.0 ✅ **CONCLUÍDA**
- Sistema de busca por localização geográfica
- Cálculo de distância usando fórmula de Haversine
- Integração com API ViaCEP para coordenadas
- Validação de disponibilidade baseada em status
- Verificação de conflitos de agendamento
- Autenticação e autorização por role
- 4 endpoints REST funcionais
- Documentação completa atualizada

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

### v0.18.0
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

## 📋 Resumos de Atualizações de Versão

### 📄 VERSION_UPDATE_SUMMARY_v0.15.0.md

#### **🚀 Versão Atualizada: v0.15.0**

**Data:** 2025-01-24  
**Tipo:** Minor Version  
**Funcionalidade:** Campo Status em Space Festival Types

#### **📋 Processo de Atualização**

**1. Commit das Funcionalidades** ✅
```bash
git commit -m "feat: adicionar campo status em Space Festival Types com documentação completa"
```
- **17 arquivos alterados**
- **1.056 inserções, 15 deleções**
- **4 novos arquivos criados**:
  - DOCUMENTATION_UPDATE_SUMMARY_SPACE_FESTIVAL.md
  - SPACE_FESTIVAL_STATUS_CONSISTENCY_CHECK.md
  - SPACE_FESTIVAL_STATUS_IMPLEMENTATION.md
  - alembic/versions/6a3d349eb6db_adicionar_coluna_status_em_space_.py

**2. Atualização de Versão** ✅
```bash
python version.py minor
```
- **Versão anterior:** v0.14.0
- **Nova versão:** v0.15.0
- **Tag criada:** v0.15.0
- **Push realizado:** Tag enviada para repositório remoto

**3. Atualização de Documentações** ✅
```bash
git commit -m "docs: atualizar versão para v0.15.0 em todas as documentações"
```
- **4 arquivos atualizados**
- **75 inserções, 6 deleções**

#### **📚 Documentações Atualizadas para v0.15.0**

**1. README.md** ✅
- **Versão atual:** v0.14.0 → v0.15.0
- **Seção atualizada:** "Funcionalidades Recentes"

**2. IMPLEMENTATION_SUMMARY.md** ✅
- **Versão atual:** 0.14.0+ → 0.15.0+
- **Nova seção:** "Funcionalidades Implementadas na v0.15.0"
- **Conteúdo:** Campo Status em Space Festival Types (Completo)

**3. VERSIONING.md** ✅
- **Versão atual:** v0.14.0 → v0.15.0
- **Nova seção:** "v0.15.0 (2025-01-24) - Campo Status em Space Festival Types"
- **Conteúdo detalhado:** Implementação completa, consistência, padrões, documentação

**4. DOCUMENTATION_UPDATE_SUMMARY_SPACE_FESTIVAL.md** ✅
- **Título atualizado:** Incluindo "(v0.15.0)"
- **Status final:** Atualizado para refletir v0.15.0

#### **🎯 Funcionalidades da v0.15.0**

**Campo Status em Space Festival Types (Completo)**

**Implementação Técnica:**
- ✅ **StatusFestivalType**: Enum com 4 valores (CONTRATANDO, FECHADO, SUSPENSO, CANCELADO)
- ✅ **Entidade**: Campo status adicionado com valor padrão CONTRATANDO
- ✅ **Modelo**: Coluna status no banco com SQLAlchemyEnum
- ✅ **Schemas**: Pydantic atualizados com validações
- ✅ **Repositório**: Método update_status() implementado
- ✅ **Serviço**: update_space_festival_type_status() criado
- ✅ **Endpoint**: PATCH /{id}/status para atualização específica
- ✅ **Migração**: Alembic aplicada com sucesso
- ✅ **Dados**: Script de inicialização atualizado

**Consistência e Padrões:**
- ✅ **Padrão idêntico** ao Space Event Types
- ✅ **Mesmo enum** com mesmos valores
- ✅ **Mesma estrutura** em todas as camadas
- ✅ **Mesmo endpoint** PATCH para status
- ✅ **Mesmas validações** e regras de negócio
- ✅ **Arquitetura hexagonal** respeitada

**Verificação de Consistência:**
- ✅ **Endpoints diretos** de Space Festival Types
- ✅ **Endpoints de Reviews** com relacionamentos
- ✅ **Endpoints de Interests** com relacionamentos
- ✅ **Endpoints de Bookings** com relacionamentos
- ✅ **100% de compatibilidade** mantida

#### **📊 Estatísticas da v0.15.0**

**Arquivos Modificados:**
- **Código:** 13 arquivos
- **Documentação:** 4 arquivos
- **Migração:** 1 arquivo
- **Scripts:** 1 arquivo

**Documentações Atualizadas:**
- **Principais:** 4 arquivos (.md)
- **Específicas:** 3 arquivos criados
- **Total:** 7 documentações

**Funcionalidades:**
- **Novo campo:** status em SpaceFestivalType
- **Novo endpoint:** PATCH para atualização de status
- **Novo enum:** StatusFestivalType
- **Novos schemas:** SpaceFestivalTypeStatusUpdate
- **Novos métodos:** update_status() em repositório e serviço

#### **🚀 Status Final**

**✅ VERSÃO v0.15.0 CRIADA COM SUCESSO**

**Resumo das Atividades:**
1. ✅ **Funcionalidades implementadas** e commitadas
2. ✅ **Versão minor incrementada** (v0.14.0 → v0.15.0)
3. ✅ **Tag Git criada** e enviada para repositório remoto
4. ✅ **Todas as documentações atualizadas** para v0.15.0
5. ✅ **Push final realizado** com atualizações de documentação

**🎯 Próximos Passos Disponíveis:**

- **Desenvolvimento:** Continuar implementando novas funcionalidades
- **Testes:** Implementar testes automatizados para os novos endpoints
- **Documentação:** Manter documentação sempre atualizada
- **Deploy:** Preparar para produção quando necessário

**📈 Impacto da v0.15.0:**

- **Sistema mais robusto:** Controle granular de status em festivais
- **Consistência mantida:** Padrão idêntico ao Space Event Types
- **Documentação completa:** 100% das funcionalidades documentadas
- **Arquitetura sólida:** Padrões estabelecidos seguidos fielmente

**A API eShow está na versão v0.15.0 e pronta para uso! 🎉** 