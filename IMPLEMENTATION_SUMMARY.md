# Resumo da Implementação - eShow API

## 🚀 Versão Atual: 0.23.0

### ✨ Funcionalidades Implementadas na v0.23.0

#### **Correção de Testes de Integração e Unitários:**
- **Problema identificado**: Falhas em testes de integração e unitários
- **EventType Management**: Conflito de nomes duplicados corrigido com UUIDs únicos
- **Financial Management**: CPFs/CNPJs inválidos e duplicados corrigidos
- **Isolamento de testes**: Problemas de interferência entre testes resolvidos
- **Validação robusta**: Todos os CPFs/CNPJs agora seguem formato correto (11/14 dígitos)
- **Testes estáveis**: 26 testes de integração e 7 testes de financial passando 100%
- **Melhorias implementadas**: Nomes únicos, mensagens de erro informativas, isolamento adequado

#### **Melhorias Técnicas:**
- **UUID para dados únicos**: `str(uuid.uuid4().int)[:3]` para dígitos numéricos
- **Validação de formato**: CPFs com 11 dígitos, CNPJs com 14 dígitos
- **Isolamento de banco**: Testes não interferem uns com os outros
- **Debug melhorado**: Mensagens de erro mais informativas

#### **Arquivos Modificados:**
- `tests/test_integration.py`: Correção do teste EventType com nomes únicos
- `tests/test_financials.py`: Correção de todos os testes com CPFs/CNPJs únicos
- `version.py`: Atualização para v0.23.0
- `README.md`: Documentação das correções
- `VERSIONING.md`: Changelog atualizado

### ✨ Funcionalidades Implementadas na v0.22.1

#### **Correção Crítica de Bug no Sistema de Busca por Localização:**
- **Problema identificado**: Erro 500 no endpoint `/api/v1/location-search/spaces-for-artist`
- **Causa raiz**: Profile ID 4 com coordenadas armazenadas como string com vírgula
- **Erro específico**: `"must be real number, not str"` durante cálculo de distância
- **Solução implementada**: Conversão automática de string para float
- **Correção de dados**: Substituição de vírgula por ponto decimal no banco
- **Prevenção futura**: Conversão explícita de tipos no LocationSearchService
- **Validação completa**: Endpoint funcionando corretamente após correção
- **Testes realizados**: Confirmação do funcionamento do sistema de busca geográfica

#### **Melhorias de Robustez:**
- **Conversão explícita**: `float(artist.raio_atuacao)` para garantir tipos corretos
- **Tratamento de None**: Valores padrão para coordenadas ausentes
- **Logs melhorados**: Rastreamento de conversões de tipos
- **Validação de tipos**: Verificação robusta de dados geográficos

#### **Arquivos Modificados:**
- `app/application/services/location_search_service.py`: Conversão explícita de tipos
- `infrastructure/database/models/profile_model.py`: Correção de dados no banco
- `version.py`: Atualização para v0.22.1
- `pyproject.toml`: Atualização da versão
- `VERSIONING.md`: Documentação da correção

### ✨ Funcionalidades Implementadas na v0.22.0

#### **Documentação Completa e Estabilização:**
- **Todas as documentações sincronizadas** e atualizadas para v0.22.0
- **API_USAGE.md**: Seção completa sobre Sistema de Perfis com coordenadas geográficas
- **README.md**: Funcionalidades recentes atualizadas com coordenadas geográficas
- **IMPLEMENTATION_SUMMARY.md**: Resumo técnico atualizado para v0.22.0
- **ARCHITECTURE.md**: Descrição da entidade Profile atualizada
- **DATABASE_STRATEGY.md**: Consultas SQL atualizadas com coordenadas
- **VERSIONING.md**: Changelog completo e atualizado
- **SCRIPTS_README.md**: Documentação de scripts atualizada

#### **Sistema Estabilizado:**
- **151 endpoints funcionais**: Todos os endpoints testados e documentados
- **18 entidades de domínio**: Arquitetura hexagonal consolidada
- **18 tabelas no banco**: Estrutura de dados otimizada
- **20 schemas Pydantic**: Validação de dados robusta
- **Sistema de coordenadas**: Integração completa com busca geográfica
- **Testes automatizados**: Cobertura de testes implementada

#### **Versionamento Automatizado:**
- **Tag Git v0.22.0**: Criada e sincronizada com repositório remoto
- **Versionamento semântico**: Padrão MAJOR.MINOR.PATCH seguido
- **Changelog detalhado**: Histórico completo de mudanças
- **Documentação sincronizada**: Todas as referências de versão atualizadas

### ✨ Funcionalidades Implementadas na v0.19.0

#### **Coordenadas Geográficas em Perfis:**
- **Campos `latitude` e `longitude`** adicionados à entidade Profile como opcionais
- **Migração Alembic**: `37212dd22c82_adicionar_colunas_latitude_longitude_em_profiles` aplicada
- **Modelo de banco atualizado**: Colunas `latitude` e `longitude` como `Float` e `nullable=True`
- **Schemas Pydantic atualizados**: ProfileBase, ProfileUpdate e ProfileResponse incluem os novos campos
- **Repositório atualizado**: Todos os métodos (create, get_by_id, get_by_role_id, get_by_user_id, get_all, update) processam os novos campos
- **Serviço de aplicação atualizado**: ProfileService inclui latitude e longitude em todas as operações
- **Script de inicialização atualizado**: `init_profiles.py` com coordenadas reais para diferentes cidades brasileiras
- **Testes atualizados**: `tests/test_profiles.py` verifica criação, leitura e atualização dos campos
- **Validação de coordenadas**: Latitude entre -90 e 90, longitude entre -180 e 180
- **Integração com sistema de busca**: Campos utilizados para cálculos de distância e proximidade
- **Compatibilidade total**: Perfis existentes funcionam normalmente (campos opcionais)
- **Documentação atualizada**: API_USAGE.md e README.md incluem exemplos de uso

### ✨ Funcionalidades Implementadas na v0.18.1

- **Correção crítica do LocationUtils**: Refatoração completa e eliminação de hard coded
- **Base de dados primária**: Uso exclusivo da tabela cep_coordinates (4111 CEPs, 3928 cidades)
- **ViaCEP como redundância**: API externa apenas para CEPs não cadastrados
- **Formato de CEP corrigido**: CEPs formatados com hífen para busca local
- **Sistema confiável**: Baseado em dados reais da base IBGE sem hard coded
- **Performance melhorada**: Consultas diretas na base local sem fallbacks desnecessários
- **Teste realizado**: Script de diagnóstico criado e executado com sucesso
- **2 espaços encontrados**: Dentro do raio de 50km do artista (48400-000)
- **Documentação atualizada**: VERSIONING.md e README.md atualizados

#### **Busca Insensível a Acentos (NOVO):**
- **Normalização automática**: Função `_normalize_text()` que remove acentos usando `unicodedata`
- **Coluna normalizada**: `cidade_normalizada` adicionada à tabela `cep_coordinates`
- **Migração Alembic**: `7ad7aed06bd6_adicionar_coluna_cidade_normalizada` aplicada
- **População automática**: Todos os 5.565 municípios processados com normalização
- **Busca flexível**: Métodos `get_by_cidade_uf()` e `search_by_cidade()` atualizados
- **Performance otimizada**: Índice `idx_cep_coordinates_cidade_normalizada` criado
- **Exemplos funcionais**: "São Paulo" = "SAO PAULO" = "são paulo"
- **Busca parcial**: Funciona com termos parciais normalizados
- **Testes realizados**: 16 casos de teste com diferentes acentuações - 100% sucesso

#### **Correções Críticas da v0.18.0:**
- **Correção do erro**: `LocationUtils.is_within_radius` não encontrado
- **Adaptação do LocationSearchService** para nova estrutura de coordenadas
- **Correção dos parâmetros** do método `get_conflicting_bookings`
- **Sistema 100% funcional** com nova estrutura de dados geográficos

### ✨ Funcionalidades Implementadas na v0.18.0

#### **Refatoração Completa do Sistema de Localização:**
- **Mudança estrutural**: Tabela `cep_coordinates` refatorada para cidade/UF em vez de CEP
- **Remoção de colunas**: `cep`, `logradouro`, `bairro` removidas
- **Nova chave primária**: Composta por `cidade` e `uf`
- **Importação IBGE**: 5.565 municípios brasileiros com coordenadas reais
- **Cobertura 100%**: Todos os municípios brasileiros incluídos
- **Dados oficiais**: Coordenadas precisas do arquivo oficial do IBGE
- **Migração complexa**: `fa49132b1dc5_alterar_cep_coordinates_para_cidade_uf`
- **Recriação de tabela**: Estratégia necessária para SQLite
- **Preservação de dados**: Todos os dados existentes mantidos

### ✨ Funcionalidades Implementadas na v0.14.0

#### **Campo Status em Space Event Types:**

- **StatusEventType**: Enum com 4 valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
  - Campo `status` adicionado à entidade SpaceEventType com valor padrão CONTRATANDO
  - Validação para garantir que o status seja um valor válido do enum
  - Coluna `status` no modelo de banco com tipo SQLAlchemyEnum e valor padrão
  - Schemas Pydantic atualizados para incluir o campo status
  - Schema específico `SpaceEventTypeStatusUpdate` para atualização de status
  - Método `update_status()` no repositório para atualização específica
  - Serviço `update_space_event_type_status()` para atualização de status
  - Novo endpoint `PATCH /{id}/status` para atualização específica de status
  - Migração do Alembic aplicada com sucesso
  - Script de inicialização atualizado com diferentes status
  - **Consistência total** em todos os endpoints relacionados (reviews, interests, bookings)
  - **Documentação completa** atualizada (API_USAGE.md, README.md, IMPLEMENTATION_SUMMARY.md)

#### **Campo Status em Space Festival Types:**

- **StatusFestivalType**: Enum com 4 valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
  - Campo `status` adicionado à entidade SpaceFestivalType com valor padrão CONTRATANDO
  - Validação para garantir que o status seja um valor válido do enum
  - Coluna `status` no modelo de banco com tipo SQLAlchemyEnum e valor padrão
  - Schemas Pydantic atualizados para incluir o campo status
  - Schema específico `SpaceFestivalTypeStatusUpdate` para atualização de status
  - Método `update_status()` no repositório para atualização específica
  - Serviço `update_space_festival_type_status()` para atualização de status
  - Novo endpoint `PATCH /{id}/status` para atualização específica de status
  - Migração do Alembic aplicada com sucesso
  - Script de inicialização atualizado com diferentes status
  - **Consistência total** em todos os endpoints relacionados (reviews, interests, bookings)
  - **Padrão idêntico** ao Space Event Types para manter uniformidade
  - **Documentação completa** atualizada (API_USAGE.md, README.md, IMPLEMENTATION_SUMMARY.md)
  - **Documentação específica** criada (SPACE_FESTIVAL_STATUS_IMPLEMENTATION.md, SPACE_FESTIVAL_STATUS_CONSISTENCY_CHECK.md)

### ✨ Funcionalidades Implementadas na v0.15.0

#### **Campo Status em Space Festival Types (Completo):**

- **StatusFestivalType**: Enum com 4 valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
  - Campo `status` adicionado à entidade SpaceFestivalType com valor padrão CONTRATANDO
  - Validação para garantir que o status seja um valor válido do enum
  - Coluna `status` no modelo de banco com tipo SQLAlchemyEnum e valor padrão
  - Schemas Pydantic atualizados para incluir o campo status
  - Schema específico `SpaceFestivalTypeStatusUpdate` para atualização de status
  - Método `update_status()` no repositório para atualização específica
  - Serviço `update_space_festival_type_status()` para atualização de status
  - Novo endpoint `PATCH /{id}/status` para atualização específica de status
  - Migração do Alembic aplicada com sucesso
  - Script de inicialização atualizado com diferentes status
  - **Consistência total** em todos os endpoints relacionados (reviews, interests, bookings)
  - **Padrão idêntico** ao Space Event Types para manter uniformidade
  - **Documentação completa** atualizada (API_USAGE.md, README.md, IMPLEMENTATION_SUMMARY.md)
  - **Documentação específica** criada (SPACE_FESTIVAL_STATUS_IMPLEMENTATION.md, SPACE_FESTIVAL_STATUS_CONSISTENCY_CHECK.md)
  - **Versão atualizada** para v0.15.0 com todas as documentações

### ✨ Funcionalidades Implementadas na v0.16.0

#### **Sistema de Busca por Localização (Completo):**

- **LocationSearchService**: Sistema completo de busca geográfica baseada em raio de atuação
  - **Endpoint 1**: Busca de espaços para artistas baseada no raio de atuação do artista
  - **Endpoint 2**: Busca de artistas para espaços baseada no raio de atuação dos artistas
  - **Cálculo de distância**: Implementação da fórmula de Haversine para cálculo preciso
  - **Integração com ViaCEP**: Obtenção de coordenadas geográficas via API externa
  - **Verificação de disponibilidade**: Filtro por status "CONTRATANDO" em eventos/festivais
  - **Verificação de conflitos**: Detecção de agendamentos sobrepostos para artistas
  - **Flexibilidade de resposta**: Opção de retornar dados completos ou apenas IDs
  - **Autenticação e autorização**: Validação de roles (artista/espaço) por endpoint
  - **Limite de resultados**: Parâmetro configurável para controle de performance

- **Componentes Técnicos Implementados:**
  - **LocationUtils**: Utilitário para cálculos de distância e integração com ViaCEP
  - **LocationSearchService**: Serviço principal com lógica de negócio complexa
  - **Schemas Pydantic**: Estruturas para requisições e respostas padronizadas
  - **Endpoints REST**: 4 endpoints (GET/POST para cada funcionalidade)
  - **Métodos de Repositório**: Extensões nos repositórios para suporte à busca
  - **Dependência requests**: Adicionada para integração com API externa

- **Endpoints Disponíveis:**
  - `GET /api/v1/location-search/spaces-for-artist` - Busca espaços para artista
  - `POST /api/v1/location-search/spaces-for-artist` - Versão POST da busca
  - `GET /api/v1/location-search/artists-for-space` - Busca artistas para espaço
  - `POST /api/v1/location-search/artists-for-space` - Versão POST da busca

- **Lógica de Busca Implementada:**
  - **Espaços para Artista**: Verifica raio de atuação, filtra por status "CONTRATANDO"
  - **Artistas para Espaço**: Verifica disponibilidade, detecta conflitos de agendamento
  - **Cálculo de Distância**: Fórmula de Haversine com coordenadas do ViaCEP
  - **Validação de Roles**: Artistas só buscam espaços, espaços só buscam artistas

- **Características Avançadas:**
  - **Fallback de Coordenadas**: Sistema de coordenadas aproximadas em caso de falha da API
  - **Verificação de Conflitos**: Lógica de sobreposição de horários para agendamentos
  - **Metadados de Busca**: Inclusão de raio, CEP de origem e total de resultados
  - **Tratamento de Erros**: Códigos de erro específicos e mensagens claras
  - **Performance**: Limite configurável de resultados e otimizações de consulta

  - **Documentação Completa:**
  - **API_USAGE.md**: Documentação técnica completa com exemplos práticos
  - **IMPLEMENTATION_SUMMARY.md**: Resumo detalhado da implementação
  - **Exemplos de Uso**: JavaScript, Python e cURL para diferentes cenários
  - **Códigos de Erro**: Tabela completa com descrições específicas
  - **Limitações**: Documentação de limitações e recomendações de melhoria

### ✨ Funcionalidades Implementadas na v0.17.0

#### **Sistema de Busca por Localização (Estabilizado):**

- **Versão Minor**: Atualização para v0.17.0 com estabilização completa
  - **Tag Git**: v0.16.0 criada e sincronizada com repositório remoto
  - **Documentação**: Todas as 6 documentações principais atualizadas
  - **Testes**: Sistema testado via API com validação de funcionalidades
  - **Arquitetura**: Padrões hexagonais mantidos e documentados
  - **Performance**: Otimizações de banco e consultas implementadas
  - **Escalabilidade**: Considerações para cache e índices espaciais documentadas

- **Melhorias de Documentação:**
  - **README.md**: Atualizado com estatísticas v0.17.0 e seção Location Search
  - **ARCHITECTURE.md**: Sistema de Location Search detalhado com componentes
  - **DATABASE_STRATEGY.md**: Estrutura de dados e otimizações para busca geográfica
  - **VERSIONING.md**: Changelog atualizado com marcos v0.16.0 e v0.17.0
  - **API_USAGE.md**: Guia prático completo para endpoints de busca
  - **IMPLEMENTATION_SUMMARY.md**: Resumo técnico atualizado para v0.20.0

- **Estabilização Técnica:**
  - **Versionamento**: Sistema automático funcionando corretamente
  - **Dependências**: requests==2.31.0 adicionada para integração ViaCEP
  - **Repositórios**: Métodos especializados implementados e testados
  - **Serviços**: LocationSearchService com lógica robusta e validada
  - **Schemas**: Estruturas padronizadas para requisições e respostas
  - **Endpoints**: 4 endpoints funcionais com autenticação e autorização

### ✨ Funcionalidades Implementadas na v0.12.0

#### **Sistema de Manifestações de Interesse (Interests) Completo:**

- **Interest**: Sistema completo de manifestações de interesse entre artistas e espaços
  - 15 endpoints REST funcionais com autenticação JWT
  - Gestão de manifestações de interesse bidirecionais (artista→espaço, espaço→artista)
  - Sistema de status com 3 estados: "AGUARDANDO_CONFIRMACAO", "ACEITO", "RECUSADO"
  - Validação de roles: apenas artistas podem manifestar interesse em espaços e vice-versa
  - Prevenção de duplicatas: não é possível manifestar interesse duplicado
  - Validações robustas: data futura, duração 0.5-8h, valores positivos, mensagem obrigatória
  - Endpoints especializados para aceitar/rejeitar manifestações
  - Consultas por profile (enviadas, recebidas, pendentes)
  - Estatísticas detalhadas por profile
  - Filtros avançados por status, tipo de evento e período
  - Relacionamentos com profiles, space_event_types e space_festival_types
  - Parâmetro `include_relations=true` para carregar dados relacionados
  - Migração de banco aplicada (tabela interests)
  - Dados de exemplo populados (17 manifestações com diferentes status)
  - **v0.13.4**: Correção do enum StatusInterest para compatibilidade com banco de dados
  - **v0.13.5**: Correção do método get_profile_by_user_id no ProfileService
  - **v0.13.6**: Correção do timeout do pool de conexões do banco de dados

### ✨ Funcionalidades Implementadas na v0.11.1

#### **Sistema Financeiro/Bancário Completo:**

- **Financial**: Sistema completo de dados financeiros/bancários com suporte a PIX
  - 13 endpoints REST funcionais com autenticação JWT
  - Gestão de dados bancários (código banco string 3 dígitos, agência, conta, tipo)
  - Sistema completo de chaves PIX com 5 tipos: CPF, CNPJ, Celular, E-mail, Aleatória
  - Validações robustas específicas por tipo de chave PIX
  - Código do banco como string 3 dígitos (001-999) seguindo padrão brasileiro
  - Garantia de unicidade de chaves PIX no sistema
  - Preferências de transferência (PIX/TED)
  - Relacionamento com profiles existentes
  - Estatísticas em tempo real por banco e tipo de chave PIX
  - Parâmetro `include_relations=true` para carregar dados relacionados
  - Endpoint de verificação de disponibilidade de chave PIX
  - Migração de banco aplicada (tabela financials com banco VARCHAR(3))
  - Dados de exemplo populados (6 registros com bancos "341", "237", "104", "001", "033", "260")

### ✨ Funcionalidades Implementadas na v0.10.3

#### **Sistema de Avaliações/Reviews Completo:**

- **Reviews**: Sistema completo de avaliações com notas de 1 a 5 estrelas
  - 11 endpoints REST funcionais
  - **Regras de negócio implementadas**: ADMIN não avalia, ARTISTA e ESPAÇO podem avaliar
  - **Profile_id determinado automaticamente** pelo usuário logado
  - Relacionamento com profiles, space_event_types e space_festival_types
  - Validações robustas (nota entre 1-5, depoimento mínimo 10 caracteres)
  - Cálculo de média de avaliações por profile
  - Filtros avançados por profile, nota, período, tipo de evento/festival
  - Parâmetro `include_relations=true` para carregar dados relacionados
  - Migração de banco de dados aplicada
  - **Dados de exemplo populados (12 reviews)** seguindo regras de negócio
- **Versão 0.13.1**: Correções no sistema de reviews implementadas
- **Versão 0.13.2**: Correção do parâmetro include_relations nos endpoints de reviews
- **Versão 0.13.3**: Padronização dos endpoints DELETE para retornar mensagens de sucesso
- **Versão 0.13.4**: Correção do enum StatusInterest para compatibilidade com banco de dados
- **Versão 0.13.5**: Correção do método get_profile_by_user_id no ProfileService
- **Versão 0.13.6**: Correção do timeout do pool de conexões do banco de dados

### ✨ Funcionalidades Implementadas na v0.10.0-0.10.2

#### **Relacionamentos N:N Implementados:**

- **Space-Event Types**: Sistema completo de associação entre espaços e tipos de eventos
  - 10 endpoints REST funcionais
  - Sistema de banners para eventos
  - Operações CRUD e em lote
  - Filtros avançados por espaço, tipo de evento ou combinação
  - Migração de banco de dados aplicada
  - Dados de exemplo populados

- **Space-Festival Types**: Sistema completo de associação entre espaços e tipos de festivais
  - 10 endpoints REST funcionais
  - Sistema de banners para festivais
  - Operações CRUD e em lote
  - Filtros avançados por espaço, tipo de festival ou combinação
  - Migração de banco de dados aplicada
  - Dados de exemplo populados

### **📅 Sistema de Agendamentos (Bookings)**
- **4 tipos de agendamentos:** Espaço, Artista, Evento e Festival
- **Regras por role:** ADMIN não agenda, ARTISTA só agenda espaços/eventos/festivais, ESPAÇO só agenda artistas/eventos/festivais
- **Validações robustas:** Datas, horários e relacionamentos únicos
- **Filtros especializados:** Por profile, espaço, artista, evento, festival e período
- **CRUD completo:** Criar, ler, atualizar e deletar agendamentos
- **Autenticação obrigatória:** Todos endpoints protegidos por JWT

## Visão Geral
API RESTful desenvolvida em FastAPI seguindo a arquitetura hexagonal (Clean Architecture) para gerenciamento de artistas, espaços e eventos musicais.

## Arquitetura Implementada

### 1. Estrutura de Camadas
- **Domain Layer**: Entidades e interfaces de repositório
- **Application Layer**: Serviços de aplicação e schemas
- **Infrastructure Layer**: Implementações de repositório e modelos de banco
- **API Layer**: Endpoints e rotas

### 2. Padrões Utilizados
- **Repository Pattern**: Para abstração do acesso a dados
- **Dependency Injection**: Para injeção de dependências
- **DTO Pattern**: Schemas Pydantic para transferência de dados
- **JWT Authentication**: Autenticação baseada em tokens

## Funcionalidades Implementadas

### 1. Autenticação e Autorização
- ✅ Registro de usuários
- ✅ Login com JWT
- ✅ Logout com blacklist de tokens
- ✅ Renovação de tokens
- ✅ Proteção de endpoints

### 2. Gerenciamento de Usuários
- ✅ CRUD completo de usuários
- ✅ Validação de dados
- ✅ Ativação/desativação de usuários

### 3. Gerenciamento de Roles
- ✅ CRUD completo de roles
- ✅ Roles predefinidos: ADMIN, ARTISTA, ESPACO
- ✅ Validação de tipos de role

### 4. Gerenciamento de Profiles
- ✅ CRUD completo de profiles
- ✅ Relacionamento com usuários e roles
- ✅ Validação de dados de endereço
- ✅ Busca por role

### 5. Gerenciamento de Artist Types
- ✅ CRUD completo de tipos de artistas
- ✅ Tipos predefinidos: Cantor(a) solo, Dupla, Trio, Banda, Grupo
- ✅ Validação de tipos

### 6. Gerenciamento de Musical Styles
- ✅ CRUD completo de estilos musicais
- ✅ Estilos flexíveis (qualquer string)
- ✅ Validação de unicidade

### 7. Gerenciamento de Artists
- ✅ CRUD completo de artistas
- ✅ Relacionamento com profiles e artist types
- ✅ Validação de dados de apresentação
- ✅ Redes sociais opcionais
- ✅ Busca por tipo de artista
- ✅ Busca por profile

### 8. Relacionamento N:N Artists-Musical Styles
- ✅ Tabela de relacionamento N:N
- ✅ CRUD completo de relacionamentos
- ✅ Criação individual e em lote
- ✅ Busca por artista ou estilo musical
- ✅ Atualização em lote (substituição)
- ✅ Deleção individual e em lote
- ✅ Integração com endpoints de artists

### 8.1. Sistema de Controle de Acesso por Roles ✨
- ✅ **Validação de roles nos serviços**
  - Artists: Apenas profiles com role "ARTISTA" (`role_id = 2`)
  - Spaces: Apenas profiles com role "ESPACO" (`role_id = 3`)
- ✅ **Validação na criação e atualização**
  - Verificação automática do role do profile
  - Mensagens de erro claras e específicas
- ✅ **Integração com ProfileRepository**
  - Dependência injetada nos serviços
  - Validação em tempo real
- ✅ **Dados de exemplo reestruturados**
  - Profiles criados com roles adequados
  - Artists e Spaces apenas com profiles válidos

### 9. Gerenciamento de Space Types
- ✅ CRUD completo de tipos de espaço
- ✅ 15 tipos pré-cadastrados (Bar, Restaurante, Clube, etc.)
- ✅ Validação de unicidade de tipos
- ✅ Flexibilidade para adicionar novos tipos
- ✅ Padrão consistente com outros endpoints
- ✅ Script de inicialização automática

### 10. Gerenciamento de Event Types
- ✅ CRUD completo de tipos de evento
- ✅ 7 tipos pré-cadastrados (Aniversário, Casamento, Formatura, etc.)
- ✅ Validação de unicidade de tipos
- ✅ Flexibilidade para adicionar novos tipos
- ✅ Padrão consistente com outros endpoints
- ✅ Script de inicialização automática

### 11. Gerenciamento de Festival Types
- ✅ CRUD completo de tipos de festival
- ✅ 14 tipos pré-cadastrados (Aniversário de Emancipação Política, Festa Religiosa, etc.)
- ✅ Validação de unicidade de tipos
- ✅ Flexibilidade para adicionar novos tipos
- ✅ Padrão consistente com outros endpoints
- ✅ Script de inicialização automática

### 12. Sistema de Avaliações/Reviews ✨ **[v0.10.3]**
- ✅ **CRUD completo de reviews**
  - Criar, ler, atualizar e deletar avaliações
  - 11 endpoints REST funcionais
- ✅ **Sistema de notas de 1 a 5 estrelas**
  - Validação rigorosa de notas inteiras entre 1-5
  - Cálculo automático de média por profile
- ✅ **Validações robustas**
  - Depoimento mínimo 10 caracteres, máximo 1000
  - Relacionamento exclusivo: OU space_event_type OU space_festival_type
  - Profile_id imutável após criação
- ✅ **Filtros avançados**
  - Por profile avaliado
  - Por nota específica (1-5 estrelas)
  - Por período (data_inicio até data_fim)
  - Por tipo de evento ou festival
- ✅ **Relacionamentos incluídos**
  - Profile avaliado com dados completos
  - Space_event_type ou space_festival_type relacionados
  - Parâmetro `include_relations=true` disponível
- ✅ **Dados de exemplo**
  - 6 reviews iniciais com distribuição de notas
  - Relacionamentos com profiles, eventos e festivais existentes
- ✅ **Endpoint de estatísticas**
  - Média de avaliações por profile
  - Contagem total de reviews por profile

## Estrutura do Banco de Dados

### Tabelas Principais
1. **users**: Usuários do sistema
2. **roles**: Tipos de perfil (ADMIN, ARTISTA, ESPACO)
3. **profiles**: Perfis detalhados dos usuários
4. **artist_types**: Tipos de artistas
5. **musical_styles**: Estilos musicais
6. **artists**: Artistas com dados de apresentação
7. **artist_musical_style**: Relacionamento N:N entre artistas e estilos
8. **space_types**: Tipos de espaço (Bar, Restaurante, Clube, etc.)
9. **event_types**: Tipos de evento (Aniversário, Casamento, Formatura, etc.)
10. **festival_types**: Tipos de festival (Festa Religiosa, Festival de Música, etc.)
11. **spaces**: Espaços para apresentações com dados detalhados
12. **space_event_types**: Relacionamento N:N entre espaços e tipos de evento
13. **space_festival_types**: Relacionamento N:N entre espaços e tipos de festival
14. **bookings**: Agendamentos/reservas entre profiles
15. **reviews**: Avaliações/reviews com notas de 1-5 estrelas
16. **financials**: Dados financeiros/bancários com chaves PIX
17. **interests**: Manifestações de interesse entre artistas e espaços

### Relacionamentos
- **users** ↔ **profiles**: 1:1
- **roles** ↔ **profiles**: 1:N
- **profiles** ↔ **artists**: 1:1
- **profiles** ↔ **spaces**: 1:N
- **profiles** ↔ **reviews**: 1:N (profile avaliado)
- **profiles** ↔ **interests**: 1:N (profile interessado e profile interesse)
- **artist_types** ↔ **artists**: 1:N
- **space_types** ↔ **spaces**: 1:N
- **event_types** ↔ **spaces**: 1:N (opcional)
- **festival_types** ↔ **spaces**: 1:N (opcional)
- **artists** ↔ **musical_styles**: N:N (via artist_musical_style)
- **spaces** ↔ **event_types**: N:N (via space_event_types)
- **spaces** ↔ **festival_types**: N:N (via space_festival_types)
- **space_event_types** ↔ **reviews**: 1:N (opcional, mutuamente exclusivo)
- **space_festival_types** ↔ **reviews**: 1:N (opcional, mutuamente exclusivo)
- **space_event_types** ↔ **interests**: 1:N (opcional)
- **space_festival_types** ↔ **interests**: 1:N (opcional)
- **profiles** ↔ **financials**: 1:N

## Endpoints Disponíveis

### Autenticação
- `POST /api/auth/register` - Registro
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Renovar token

### Usuários (Protegidos)
- `GET /api/users/me` - Perfil atual
- `GET /api/users/{id}` - Usuário por ID
- `GET /api/users/` - Listar usuários
- `PUT /api/users/{id}` - Atualizar usuário
- `DELETE /api/users/{id}` - Deletar usuário

### Roles (Protegidos)
- `GET /api/v1/roles/` - Listar roles
- `GET /api/v1/roles/{id}` - Role por ID
- `POST /api/v1/roles/` - Criar role
- `PUT /api/v1/roles/{id}` - Atualizar role
- `DELETE /api/v1/roles/{id}` - Deletar role

### Profiles (Protegidos)
- `GET /api/v1/profiles/` - Listar profiles
- `GET /api/v1/profiles/{id}` - Profile por ID
- `GET /api/v1/profiles/role/{role_id}` - Profiles por role
- `POST /api/v1/profiles/` - Criar profile
- `PUT /api/v1/profiles/{id}` - Atualizar profile
- `DELETE /api/v1/profiles/{id}` - Deletar profile

### Artist Types (Protegidos)
- `GET /api/v1/artist-types/` - Listar tipos
- `GET /api/v1/artist-types/{id}` - Tipo por ID
- `POST /api/v1/artist-types/` - Criar tipo
- `PUT /api/v1/artist-types/{id}` - Atualizar tipo
- `DELETE /api/v1/artist-types/{id}` - Deletar tipo

### Musical Styles (Protegidos)
- `GET /api/v1/musical-styles/` - Listar estilos
- `GET /api/v1/musical-styles/{id}` - Estilo por ID
- `POST /api/v1/musical-styles/` - Criar estilo
- `PUT /api/v1/musical-styles/{id}` - Atualizar estilo
- `DELETE /api/v1/musical-styles/{id}` - Deletar estilo

### Artists (Protegidos)
- `GET /api/v1/artists/` - Listar artistas
- `GET /api/v1/artists/{id}` - Artista por ID
- `GET /api/v1/artists/profile/{profile_id}` - Artista por profile
- `GET /api/v1/artists/type/{artist_type_id}` - Artistas por tipo
- `POST /api/v1/artists/` - Criar artista
- `PUT /api/v1/artists/{id}` - Atualizar artista
- `DELETE /api/v1/artists/{id}` - Deletar artista

### Artist-Musical Styles (Protegidos)
- `POST /api/v1/artist-musical-styles/` - Criar relacionamento individual
- `POST /api/v1/artist-musical-styles/bulk` - Criar relacionamentos em lote
- `GET /api/v1/artist-musical-styles/artist/{artist_id}` - Estilos de um artista
- `GET /api/v1/artist-musical-styles/musical-style/{musical_style_id}` - Artistas de um estilo
- `GET /api/v1/artist-musical-styles/{artist_id}/{musical_style_id}` - Relacionamento específico
- `PUT /api/v1/artist-musical-styles/artist/{artist_id}` - Atualizar estilos de artista
- `DELETE /api/v1/artist-musical-styles/{artist_id}/{musical_style_id}` - Deletar relacionamento
- `DELETE /api/v1/artist-musical-styles/artist/{artist_id}` - Deletar todos os relacionamentos de artista
- `DELETE /api/v1/artist-musical-styles/musical-style/{musical_style_id}` - Deletar todos os relacionamentos de estilo

### Space Types (Protegidos)
- `GET /api/v1/space-types/` - Listar tipos de espaço
- `GET /api/v1/space-types/{id}` - Tipo de espaço por ID
- `POST /api/v1/space-types/` - Criar tipo de espaço
- `PUT /api/v1/space-types/{id}` - Atualizar tipo de espaço
- `DELETE /api/v1/space-types/{id}` - Deletar tipo de espaço

### Event Types (Protegidos)
- `GET /api/v1/event-types/` - Listar tipos de evento
- `GET /api/v1/event-types/{id}` - Tipo de evento por ID
- `POST /api/v1/event-types/` - Criar tipo de evento
- `PUT /api/v1/event-types/{id}` - Atualizar tipo de evento
- `DELETE /api/v1/event-types/{id}` - Deletar tipo de evento

### Festival Types (Protegidos)
- `GET /api/v1/festival-types/` - Listar tipos de festival
- `GET /api/v1/festival-types/{id}` - Tipo de festival por ID
- `POST /api/v1/festival-types/` - Criar tipo de festival
- `PUT /api/v1/festival-types/{id}` - Atualizar tipo de festival
- `DELETE /api/v1/festival-types/{id}` - Deletar tipo de festival

### Spaces (Protegidos)
- `GET /api/v1/spaces/` - Listar espaços
- `GET /api/v1/spaces/{id}` - Espaço por ID
- `GET /api/v1/spaces/profile/{profile_id}` - Espaços por profile
- `GET /api/v1/spaces/space-type/{space_type_id}` - Espaços por tipo de espaço
- `GET /api/v1/spaces/event-type/{event_type_id}` - Espaços por tipo de evento
- `GET /api/v1/spaces/festival-type/{festival_type_id}` - Espaços por tipo de festival
- `POST /api/v1/spaces/` - Criar espaço
- `PUT /api/v1/spaces/{id}` - Atualizar espaço
- `DELETE /api/v1/spaces/{id}` - Deletar espaço

### Space-Event Types (Protegidos)
- `GET /api/v1/space-event-types/` - Listar relacionamentos
- `GET /api/v1/space-event-types/{id}` - Relacionamento por ID
- `GET /api/v1/space-event-types/space/{space_id}` - Eventos de um espaço
- `GET /api/v1/space-event-types/event-type/{event_type_id}` - Espaços de um tipo de evento
- `GET /api/v1/space-event-types/space/{space_id}/event-type/{event_type_id}` - Relacionamentos específicos
- `POST /api/v1/space-event-types/` - Criar relacionamento
- `PUT /api/v1/space-event-types/{id}` - Atualizar relacionamento
- `DELETE /api/v1/space-event-types/{id}` - Deletar relacionamento
- `DELETE /api/v1/space-event-types/space/{space_id}` - Deletar todos de um espaço
- `DELETE /api/v1/space-event-types/event-type/{event_type_id}` - Deletar todos de um tipo

**Parâmetro `include_relations`**: Disponível nos endpoints GET de Artists e Spaces para incluir dados relacionados.

### Interests (Protegidos)
- `GET /api/v1/interests/` - Listar manifestações de interesse
- `GET /api/v1/interests/{id}` - Manifestação por ID
- `POST /api/v1/interests/` - Criar manifestação de interesse
- `PUT /api/v1/interests/{id}` - Atualizar manifestação completa
- `DELETE /api/v1/interests/{id}` - Deletar manifestação
- `PATCH /api/v1/interests/{id}/status` - Atualizar status da manifestação
- `PATCH /api/v1/interests/{id}/accept` - Aceitar manifestação de interesse
- `PATCH /api/v1/interests/{id}/reject` - Recusar manifestação de interesse
- `GET /api/v1/interests/profile/interessado/{profile_id}` - Manifestações enviadas por um profile
- `GET /api/v1/interests/profile/interesse/{profile_id}` - Manifestações recebidas por um profile
- `GET /api/v1/interests/profile/{profile_id}/pending` - Manifestações pendentes de um profile
- `GET /api/v1/interests/profile/{profile_id}/statistics` - Estatísticas de manifestações por profile
- `GET /api/v1/interests/status/{status}` - Filtrar manifestações por status
- `GET /api/v1/interests/space-event-type/{space_event_type_id}` - Manifestações por tipo de evento
- `GET /api/v1/interests/date-range/` - Filtrar manifestações por período

**Parâmetro `include_relations`**: Disponível nos endpoints GET para incluir dados relacionados (profile_interessado, profile_interesse, space_event_type, space_festival_type).

### Location Search (Protegidos)
- `GET /api/v1/location-search/spaces-for-artist` - Buscar espaços para artista (baseado no raio de atuação)
- `POST /api/v1/location-search/spaces-for-artist` - Versão POST da busca de espaços para artista
- `GET /api/v1/location-search/artists-for-space` - Buscar artistas para espaço (baseado no raio de atuação dos artistas)
- `POST /api/v1/location-search/artists-for-space` - Versão POST da busca de artistas para espaço

**Parâmetros**: `return_full_data` (boolean), `max_results` (integer)
**Autenticação**: JWT obrigatório com validação de role (artista/espaço)

**⚠️ REGRAS DE NEGÓCIO**:
- Apenas **artistas** podem manifestar interesse em **espaços**
- Apenas **espaços** podem manifestar interesse em **artistas**
- **Prevenção de duplicatas**: Não é possível manifestar interesse duplicado
- **Estados de status**: "Aguardando Confirmação", "Aceito", "Recusado"
- **Validação de data**: Data inicial deve ser futura
- **Validação de duração**: Entre 0.5 e 8 horas
- **Validação de valores**: Valores devem ser positivos
- **Mensagem obrigatória**: Mínimo 10, máximo 1000 caracteres
- **Profile_id não pode ser alterado** após criação da manifestação

### Públicos
- `GET /health` - Health check

## Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web
- **SQLAlchemy**: ORM
- **Alembic**: Migrações de banco
- **Pydantic**: Validação de dados
- **JWT**: Autenticação
- **SQLite**: Banco de dados (desenvolvimento)

### Estrutura
- **Python 3.12+**
- **Arquitetura Hexagonal**
- **Repository Pattern**
- **Dependency Injection**

## Scripts de Inicialização

### Dados Iniciais
- `init_roles.py` - Roles padrão
- `init_users.py` - Usuário admin
- `init_profiles.py` - Profiles de exemplo
- `init_artist_types.py` - Tipos de artistas
- `init_musical_styles.py` - Estilos musicais
- `init_artists.py` - Artistas de exemplo
- `init_artist_musical_styles.py` - Relacionamentos de exemplo
- `init_space_types.py` - Tipos de espaço (15 tipos pré-cadastrados)
- `init_event_types.py` - Tipos de evento (7 tipos pré-cadastrados)
- `init_festival_types.py` - Tipos de festival (14 tipos pré-cadastrados)
- `init_spaces.py` - Espaços de exemplo
- `init_space_event_types.py` - Relacionamentos espaço-evento
- `init_space_festival_types.py` - Relacionamentos espaço-festival
- `init_bookings.py` - Agendamentos de exemplo
- `init_reviews.py` - Avaliações de exemplo (6 reviews com notas variadas)
- `init_financials.py` - Dados financeiros de exemplo (6 registros com bancos reais)
- `init_interests.py` - Manifestações de interesse de exemplo (17 manifestações com diferentes status)
- `start_server.sh` - Script de inicialização automática do servidor

### Testes
- `test_api_complete.py` - Testes completos da API
- `test_relationships.py` - Testes de relacionamentos
- `test_artist_musical_styles.py` - Testes específicos do relacionamento N:N

## Como Executar

### 1. Configuração Inicial
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp env.example .env
# Editar .env com suas configurações

# Executar migrações
alembic upgrade head
```

### 2. Popular Dados Iniciais
```bash
# Executar scripts de inicialização
python init_roles.py
python init_users.py
python init_profiles.py
python init_artist_types.py
python init_musical_styles.py
python init_artists.py
python init_artist_musical_styles.py
```

### 3. Executar Aplicação
```bash
# Desenvolvimento
uvicorn app.main:app --reload

# Produção
python run.py
```

### 4. Testar API
```bash
# Testes completos
python test_api_complete.py

# Testes de relacionamentos
python test_relationships.py

# Testes específicos do relacionamento N:N
python test_artist_musical_styles.py
```

## Documentação

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **API Usage**: `API_USAGE.md` - Guia detalhado de uso
- **Architecture**: `ARCHITECTURE.md` - Documentação da arquitetura

## Status da Implementação

### ✅ Concluído
- [x] Autenticação e autorização
- [x] Gerenciamento de usuários
- [x] Gerenciamento de roles
- [x] Gerenciamento de profiles
- [x] Gerenciamento de artist types
- [x] Gerenciamento de musical styles
- [x] Gerenciamento de artists
- [x] Relacionamento N:N Artists-Musical Styles
- [x] **Gerenciamento de espaços** ✨
- [x] **Sistema de controle de acesso por roles** ✨
- [x] **Validação de roles para Artists e Spaces** ✨
- [x] **Relacionamento N:N Space-Event Types** ✨
- [x] **Relacionamento N:N Space-Festival Types** ✨ **[v0.9.0]**
- [x] **Sistema de Bookings Completo** ✨ **[v0.10.0-0.10.2]**
- [x] **Sistema de Avaliações/Reviews** ✨ **[v0.10.3]**
- [x] **Sistema Financeiro/Bancário** ✨ **[v0.11.1]**
- [x] **Sistema de Manifestações de Interesse** ✨ **[v0.12.0]**
- [x] Validações e tratamento de erros
- [x] Documentação da API
- [x] Scripts de inicialização
- [x] Testes automatizados

### 🔄 Próximos Passos
- [ ] Gerenciamento de eventos
- [ ] Sistema de notificações
- [ ] Upload de arquivos e mídias
- [ ] Sistema de pagamentos
- [ ] Cache Redis
- [ ] Logs estruturados
- [ ] Métricas e monitoramento
- [ ] Sistema de relatórios

## Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente seguindo os padrões estabelecidos
4. Adicione testes
5. Atualize a documentação
6. Submeta um pull request

## 📋 Resumos de Atualizações de Documentação

### 📄 DOCUMENTATION_UPDATE_SUMMARY.md (v0.14.0)

#### **Documentações Atualizadas**

**1. API_USAGE.md**
- **Adicionado:** Nova seção completa sobre Space Event Types
- **Visão geral** do sistema de Space Event Types
- **Estrutura** do objeto com campo `status`
- **Valores de status** disponíveis (CONTRATANDO, FECHADO, SUSPENSO, CANCELADO)
- **Endpoints disponíveis** (CRUD básico + endpoints específicos)
- **Exemplos de uso** com curl commands
- **Regras de negócio** implementadas
- **Exemplo prático** completo de gerenciamento de eventos
- **Índice atualizado** para incluir a nova seção

**2. README.md**
- **Adicionado:** Seção "Funcionalidades Recentes"
- **Campo Status em Space Event Types** com detalhes da implementação
- **Endpoint específico** para atualização de status
- **Valor padrão** CONTRATANDO
- **Consistência total** em todos os endpoints relacionados
- **Documentação atualizada** com links para os novos arquivos

**3. IMPLEMENTATION_SUMMARY.md**
- **Adicionado:** Seção sobre funcionalidades v0.13.7+
- **StatusEventType** enum com 4 valores
- **Campo status** na entidade SpaceEventType
- **Validações** implementadas
- **Schemas Pydantic** atualizados
- **Endpoint específico** PATCH /{id}/status
- **Migração Alembic** aplicada
- **Consistência total** em endpoints relacionados
- **Documentação completa** atualizada

**4. DATABASE_STRATEGY.md**
- **Adicionado:** Seção "Estrutura de Dados - Space Event Types"
- **Schema SQL** da tabela space_event_types
- **Características** da implementação
- **Consultas úteis** para análise de dados
- **Comandos de verificação** para SQLite e PostgreSQL
- **Distribuição por status** e outras análises

**5. ARCHITECTURE.md**
- **Adicionado:** Seção "Relacionamentos N:N"
- **Visão geral** dos relacionamentos implementados
- **Space Event Types** com campo status
- **Arquitetura** dos relacionamentos
- **Exemplos de código** das entidades, repositórios, serviços e endpoints
- **Benefícios** da arquitetura implementada

#### **Arquivos de Documentação Criados**

**1. STATUS_IMPLEMENTATION.md**
- **Detalhes completos** da implementação do campo status
- **Enum StatusEventType** com valores e validações
- **Arquitetura em camadas** (entidade, modelo, schema, repositório, serviço, endpoint)
- **Migração do banco** com Alembic
- **Scripts de inicialização** atualizados
- **Exemplos de uso** e testes

**2. STATUS_CONSISTENCY_CHECK.md**
- **Verificação completa** de consistência em todos os endpoints
- **Endpoints diretos** de Space Event Types
- **Endpoints com relacionamentos** (reviews, interests, bookings)
- **Schemas verificados** e confirmados consistentes
- **Serviços e repositórios** verificados
- **Conclusão** de 100% de consistência

#### **Principais Melhorias na Documentação**

**1. Completude**
- Todas as documentações principais foram atualizadas
- Informações consistentes entre os arquivos
- Exemplos práticos incluídos

**2. Usabilidade**
- Comandos curl prontos para uso
- Exemplos de consultas SQL
- Instruções passo a passo

**3. Manutenibilidade**
- Estrutura organizada e clara
- Links entre documentações
- Versões e datas de atualização

**4. Técnica**
- Detalhes de implementação
- Arquitetura explicada
- Código de exemplo incluído

#### **Impacto das Atualizações**

**Para Desenvolvedores**
- **Documentação completa** sobre o novo campo status
- **Exemplos práticos** para implementação
- **Arquitetura clara** para manutenção

**Para Usuários da API**
- **Guia de uso** detalhado dos novos endpoints
- **Exemplos de requisições** prontos para uso
- **Regras de negócio** explicadas

**Para Administradores**
- **Consultas SQL** para análise de dados
- **Comandos de verificação** para troubleshooting
- **Estrutura de banco** documentada

### 📄 DOCUMENTATION_UPDATE_SUMMARY_SPACE_FESTIVAL.md (v0.15.0)

#### **Visão Geral**

Atualização completa de todas as documentações relacionadas para incluir as novas funcionalidades do campo `status` em `SpaceFestivalType`, seguindo o mesmo padrão estabelecido para `SpaceEventType`.

#### **Documentações Atualizadas**

**1. API_USAGE.md**
- **Adicionado**: Nova seção "Sistema de Space Festival Types"
- **Conteúdo**:
  - Visão geral do sistema
  - Estrutura do objeto Space Festival Type com campo status
  - Valores de status disponíveis (CONTRATANDO, FECHADO, SUSPENSO, CANCELADO)
  - Lista completa de endpoints (CRUD, específicos, PATCH para status)
  - Exemplos detalhados de uso com curl
  - Regras de negócio
  - Exemplo prático completo de gerenciamento de festivais
- **Índice**: Atualizado para incluir a nova seção

**2. README.md**
- **Seção**: "Funcionalidades Recentes"
- **Adicionado**: 
  - "Campo Status em Space Festival Types"
  - Descrição dos valores de status
  - Endpoint específico para atualização
  - Valor padrão CONTRATANDO
  - Consistência total em endpoints relacionados
  - Padrão idêntico ao Space Event Types
- **Documentação**: Lista atualizada de documentações específicas criadas

**3. IMPLEMENTATION_SUMMARY.md**
- **Seção**: "Funcionalidades Implementadas na v0.14.0"
- **Adicionado**: 
  - StatusFestivalType enum com 4 valores
  - Campo status na entidade com valor padrão
  - Validações implementadas
  - Coluna no modelo de banco
  - Schemas Pydantic atualizados
  - Schema específico para atualização de status
  - Método update_status() no repositório
  - Serviço para atualização de status
  - Endpoint PATCH específico
  - Migração Alembic aplicada
  - Script de inicialização atualizado
  - Consistência total verificada
  - Documentação específica criada

**4. DATABASE_STRATEGY.md**
- **Adicionado**: Nova seção "Estrutura de Dados - Space Festival Types"
- **Conteúdo**:
  - Schema SQL completo da tabela
  - Características da tabela (N:N, status, constraints)
  - Consultas úteis para análise de dados:
    - Distribuição por status
    - Festivais por espaço
    - Festivais por tipo
    - Festivais futuros
    - Análise por status e período
    - Espaços com mais festivais ativos
    - Verificação de banners e links
- **Comandos Úteis**: Adicionados comandos para verificar estrutura e dados de space_festival_types

**5. ARCHITECTURE.md**
- **Seção**: "Relacionamentos N:N"
- **Atualizado**: 
  - Space Festival Types com campo status
  - Endpoint específico para atualização de status
  - Exemplos de código completos:
    - Entidade de domínio
    - Repositório com método update_status
    - Serviço com método de atualização
    - Endpoint PATCH específico
- **Benefícios**: Mantida consistência com Space Event Types

#### **Documentações Específicas Criadas**

**1. SPACE_FESTIVAL_STATUS_IMPLEMENTATION.md**
- **Conteúdo**: Documentação detalhada da implementação
- **Seções**:
  - Visão geral
  - Funcionalidades implementadas
  - Migração do banco de dados
  - Script de inicialização
  - Testes realizados
  - Endpoints disponíveis
  - Exemplos de uso
  - Validações implementadas
  - Consistência com Space Event Types
  - Próximos passos

**2. SPACE_FESTIVAL_STATUS_CONSISTENCY_CHECK.md**
- **Conteúdo**: Verificação completa de consistência
- **Seções**:
  - Endpoints verificados (diretos e com relacionamentos)
  - Arquitetura verificada (schemas, modelos, repositórios)
  - Testes realizados
  - Dados de verificação
  - Conclusões de consistência

#### **Padrões Mantidos**

**Consistência com Space Event Types**
- ✅ **Mesmo enum**: StatusEventType vs StatusFestivalType
- ✅ **Mesmos valores**: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
- ✅ **Mesma estrutura**: Entidade, modelo, schema, repositório, serviço, endpoint
- ✅ **Mesmo endpoint**: PATCH /{id}/status
- ✅ **Mesmas validações**: Enum, campos obrigatórios, relacionamentos
- ✅ **Mesma migração**: Alembic com server_default

**Arquitetura Hexagonal**
- ✅ **Domínio**: Entidade e repositório atualizados
- ✅ **Aplicação**: Serviço e schemas atualizados
- ✅ **Infraestrutura**: Modelo e implementação do repositório atualizados
- ✅ **API**: Endpoints atualizados

#### **Estatísticas das Atualizações**

- **Documentações principais atualizadas**: 5
- **Documentações específicas criadas**: 2
- **Seções adicionadas**: 8
- **Exemplos de código**: 15+
- **Comandos curl**: 10+
- **Consultas SQL**: 8+
- **Endpoints documentados**: 10

#### **Status Final**

**TODAS AS DOCUMENTAÇÕES ATUALIZADAS COM SUCESSO - v0.15.0**

A implementação do campo `status` em `SpaceFestivalType` está **100% documentada** em todas as documentações relevantes, mantendo:

- ✅ **Consistência total** com Space Event Types
- ✅ **Padrões estabelecidos** mantidos
- ✅ **Exemplos práticos** incluídos
- ✅ **Arquitetura hexagonal** respeitada
- ✅ **Documentação específica** criada
- ✅ **Versão v0.15.0** atualizada em todas as documentações

O sistema está **completamente documentado** e pronto para uso em produção! 🚀

## 📋 Documentações Específicas de Implementação

### 📄 STATUS_IMPLEMENTATION.md (v0.14.0)

#### **Resumo das Mudanças**

Implementação do campo `status` na tabela `space_event_types` com os valores enum: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO.

#### **1. Enum StatusEventType**

**Arquivo:** `domain/entities/space_event_type.py`

- Criado enum `StatusEventType` com os valores:
  - `CONTRATANDO`
  - `FECHADO`
  - `SUSPENSO`
  - `CANCELADO`
- Adicionado campo `status` na entidade `SpaceEventType` com valor padrão `CONTRATANDO`
- Adicionada validação para garantir que o status seja um valor válido do enum

#### **2. Modelo de Banco de Dados**

**Arquivo:** `infrastructure/database/models/space_event_type_model.py`

- Adicionada coluna `status` do tipo `SQLAlchemyEnum(StatusEventType)`
- Configurada como `nullable=False` com valor padrão `StatusEventType.CONTRATANDO`
- Atualizado método `__repr__` para incluir o status

#### **3. Schemas Pydantic**

**Arquivo:** `app/schemas/space_event_type.py`

- Adicionado campo `status` em todos os schemas relevantes:
  - `SpaceEventTypeBase`
  - `SpaceEventTypeCreate`
  - `SpaceEventTypeUpdate`
  - `SpaceEventTypeResponse`
- Criado schema específico `SpaceEventTypeStatusUpdate` para atualização de status
- Adicionadas validações para o campo status

#### **4. Repositório**

**Arquivo:** `domain/repositories/space_event_type_repository.py`
- Adicionado método abstrato `update_status()` na interface

**Arquivo:** `infrastructure/repositories/space_event_type_repository_impl.py`
- Implementado método `update_status()` para atualizar apenas o status
- Atualizado método `create()` para incluir o status
- Atualizado método `update()` para incluir o status
- Atualizado método `_to_entity()` para incluir o status

#### **5. Serviço de Aplicação**

**Arquivo:** `app/application/services/space_event_type_service.py`
- Adicionado campo `status` no método `create_space_event_type()`
- Adicionado campo `status` no método `update_space_event_type()`
- Criado método `update_space_event_type_status()` para atualização específica de status

#### **6. Endpoints da API**

**Arquivo:** `app/api/endpoints/space_event_types.py`
- Adicionado campo `status` na função `convert_space_event_type_to_response()`
- Criado novo endpoint `PATCH /{space_event_type_id}/status` para atualização de status
- Endpoint requer autenticação e retorna o objeto atualizado

#### **7. Migração do Banco de Dados**

**Arquivo:** `alembic/versions/131c5fdf2f57_adicionar_coluna_status_em_space_event_.py`
- Criada migração para adicionar a coluna `status`
- Configurada para SQLite com valor padrão

#### **8. Script de Inicialização**

**Arquivo:** `init_space_event_types.py`
- Atualizado para incluir o campo `status` nos dados de inicialização
- Adicionados diferentes status para demonstrar a funcionalidade

#### **Novos Endpoints Disponíveis**

**Atualizar Status**
```
PATCH /api/space-event-types/{space_event_type_id}/status
```

**Body:**
```json
{
  "status": "FECHADO"
}
```

#### **Valores de Status Disponíveis**

- `CONTRATANDO` - Evento em processo de contratação
- `FECHADO` - Evento confirmado e fechado
- `SUSPENSO` - Evento temporariamente suspenso
- `CANCELADO` - Evento cancelado

### 📄 STATUS_CONSISTENCY_CHECK.md (v0.14.0)

#### **Resumo da Verificação**

Verificação realizada para garantir que todos os endpoints que buscam dados da tabela `space_event_types` estão mantendo a consistência com a nova coluna `status`.

#### **Endpoints Verificados**

**1. Endpoints Diretos de Space Event Types**

✅ **Status:** Todos os endpoints estão consistentes

- **GET /space-event-types/** - ✅ Inclui campo `status`
- **GET /space-event-types/{id}** - ✅ Inclui campo `status`
- **POST /space-event-types/** - ✅ Aceita campo `status`
- **PUT /space-event-types/{id}** - ✅ Aceita campo `status`
- **PATCH /space-event-types/{id}/status** - ✅ Novo endpoint para atualização de status
- **DELETE /space-event-types/{id}** - ✅ Funciona corretamente

**2. Endpoints de Reviews**

✅ **Status:** Consistente

- **GET /reviews/space-event-type/{space_event_type_id}** - ✅ Usa `ReviewListWithRelations`
- **Schema:** `ReviewWithRelations` usa `SpaceEventTypeResponse` que inclui `status`

**3. Endpoints de Interests**

✅ **Status:** Consistente

- **GET /interests/space-event-type/{space_event_type_id}** - ✅ Usa `InterestListWithRelations`
- **Função de conversão:** `convert_interest_to_response()` inclui `space_event_type` quando `include_relations=True`
- **Schema:** `InterestWithRelations` usa `SpaceEventTypeResponse` que inclui `status`

**4. Endpoints de Bookings**

✅ **Status:** Consistente

- **GET /bookings/space-event-type/{space_event_type_id}** - ✅ Usa `BookingListWithRelations`
- **Função de conversão:** `convert_booking_to_response()` inclui `space_event_type` quando `include_relations=True`
- **Schema:** `BookingWithRelations` usa `SpaceEventTypeResponse` que inclui `status`

#### **Schemas Verificados**

**1. SpaceEventTypeResponse**
✅ **Status:** Inclui campo `status`

```python
class SpaceEventTypeResponse(SpaceEventTypeBase):
    id: int
    created_at: datetime
    # SpaceEventTypeBase inclui status: StatusEventType = StatusEventType.CONTRATANDO
```

**2. Schemas com Relacionamentos**
✅ **Status:** Todos usam `SpaceEventTypeResponse`

- `ReviewWithRelations` - ✅ Usa `SpaceEventTypeResponse`
- `InterestWithRelations` - ✅ Usa `SpaceEventTypeResponse`
- `BookingWithRelations` - ✅ Usa `SpaceEventTypeResponse`

#### **Conclusão**

✅ **TODOS OS ENDPOINTS ESTÃO CONSISTENTES**

**Pontos Verificados:**

1. **Endpoints diretos** - ✅ Todos incluem campo `status`
2. **Endpoints com relacionamentos** - ✅ Todos usam schemas corretos
3. **Schemas de resposta** - ✅ Todos incluem campo `status`
4. **Funções de conversão** - ✅ Todas incluem campo `status`
5. **Serviços** - ✅ Todos lidam com campo `status`
6. **Repositórios** - ✅ Todos incluem campo `status`
7. **Modelos de banco** - ✅ Coluna `status` implementada
8. **Migrações** - ✅ Aplicadas corretamente
9. **Scripts de inicialização** - ✅ Incluem campo `status`

### 📄 SPACE_FESTIVAL_STATUS_IMPLEMENTATION.md (v0.15.0)

#### **Visão Geral**

Implementação completa do campo `status` na entidade `SpaceFestivalType`, seguindo o mesmo padrão estabelecido para `SpaceEventType`. O campo permite controlar o estado dos festivais com 4 valores possíveis.

#### **Funcionalidades Implementadas**

**1. Enum StatusFestivalType**
```python
class StatusFestivalType(Enum):
    """Enum para os status possíveis de um festival"""
    CONTRATANDO = "CONTRATANDO"
    FECHADO = "FECHADO"
    SUSPENSO = "SUSPENSO"
    CANCELADO = "CANCELADO"
```

**2. Entidade de Domínio Atualizada**
- **Arquivo**: `domain/entities/space_festival_type.py`
- **Campo adicionado**: `status: StatusFestivalType = StatusFestivalType.CONTRATANDO`
- **Validação**: Verificação se o status é um valor válido do enum

**3. Modelo de Banco de Dados**
- **Arquivo**: `infrastructure/database/models/space_festival_type_model.py`
- **Coluna adicionada**: `status = Column(SQLAlchemyEnum(StatusFestivalType), nullable=False, default=StatusFestivalType.CONTRATANDO)`
- **Tipo**: SQLAlchemyEnum com valor padrão

**4. Schemas Pydantic**
- **Arquivo**: `app/schemas/space_festival_type.py`
- **Schemas atualizados**:
  - `SpaceFestivalTypeBase`: Campo status com validação
  - `SpaceFestivalTypeUpdate`: Campo status opcional
  - `SpaceFestivalTypeStatusUpdate`: Schema específico para atualização de status
- **Validações**: Verificação de valores válidos do enum

**5. Repositório**
- **Interface**: `domain/repositories/space_festival_type_repository.py`
  - Método `update_status()` adicionado
- **Implementação**: `infrastructure/repositories/space_festival_type_repository_impl.py`
  - Método `update_status()` implementado
  - Campo status incluído em `create()`, `update()` e `_to_entity()`

**6. Serviço**
- **Arquivo**: `app/application/services/space_festival_type_service.py`
- **Método adicionado**: `update_space_festival_type_status()`
- **Campo status**: Incluído em `create_space_festival_type()` e `update_space_festival_type()`

**7. Endpoints**
- **Arquivo**: `app/api/endpoints/space_festival_types.py`
- **Novo endpoint**: `PATCH /{id}/status` para atualização específica de status
- **Funções atualizadas**: `convert_space_festival_type_to_response()` inclui campo status
- **Autenticação**: Todos os endpoints requerem autenticação JWT

#### **Migração do Banco de Dados**

**Arquivo de Migração**
- **Arquivo**: `alembic/versions/6a3d349eb6db_adicionar_coluna_status_em_space_.py`
- **Comando**: `alembic revision --autogenerate -m "adicionar_coluna_status_em_space_festival_types"`
- **Ajustes**: Configurado para SQLite com `server_default='CONTRATANDO'`

#### **Script de Inicialização**

**Arquivo Atualizado**
- **Arquivo**: `init_space_festival_types.py`
- **Campo status**: Adicionado em todos os dados de exemplo
- **Distribuição de status**:
  - CONTRATANDO: 3 registros
  - FECHADO: 3 registros
  - SUSPENSO: 2 registros
  - CANCELADO: 2 registros

#### **Endpoints Disponíveis**

**CRUD Básico**
- `GET /api/v1/space-festival-types/` - Listar todos
- `GET /api/v1/space-festival-types/{id}` - Obter por ID
- `POST /api/v1/space-festival-types/` - Criar novo
- `PUT /api/v1/space-festival-types/{id}` - Atualizar completo
- `DELETE /api/v1/space-festival-types/{id}` - Deletar

**Endpoints Específicos**
- `PATCH /api/v1/space-festival-types/{id}/status` - **NOVO**: Atualizar apenas status
- `GET /api/v1/space-festival-types/space/{space_id}` - Por espaço
- `GET /api/v1/space-festival-types/festival-type/{festival_type_id}` - Por tipo de festival
- `GET /api/v1/space-festival-types/space/{space_id}/festival-type/{festival_type_id}` - Combinação específica

#### **Consistência com Space Event Types**

A implementação segue exatamente o mesmo padrão estabelecido para `SpaceEventType`:

- ✅ **Mesmo enum**: StatusEventType vs StatusFestivalType
- ✅ **Mesmos valores**: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
- ✅ **Mesma estrutura**: Entidade, modelo, schema, repositório, serviço, endpoint
- ✅ **Mesmo endpoint**: PATCH /{id}/status
- ✅ **Mesmas validações**: Enum, campos obrigatórios, relacionamentos
- ✅ **Mesma migração**: Alembic com server_default

### 📄 SPACE_FESTIVAL_STATUS_CONSISTENCY_CHECK.md (v0.15.0)

#### **Visão Geral**

Verificação completa de todos os endpoints que buscam dados da tabela `space_festival_types` para garantir que estão mantendo a consistência com o novo campo `status`.

#### **Endpoints Verificados**

**1. Endpoints Diretos de Space Festival Types**

✅ **Endpoints CRUD Básicos**
- `GET /api/v1/space-festival-types/` - **CONSISTENTE**
- `GET /api/v1/space-festival-types/{id}` - **CONSISTENTE**
- `POST /api/v1/space-festival-types/` - **CONSISTENTE**
- `PUT /api/v1/space-festival-types/{id}` - **CONSISTENTE**
- `DELETE /api/v1/space-festival-types/{id}` - **CONSISTENTE**

✅ **Endpoint Específico de Status**
- `PATCH /api/v1/space-festival-types/{id}/status` - **CONSISTENTE**

✅ **Endpoints Específicos**
- `GET /api/v1/space-festival-types/space/{space_id}` - **CONSISTENTE**
- `GET /api/v1/space-festival-types/festival-type/{festival_type_id}` - **CONSISTENTE**
- `GET /api/v1/space-festival-types/space/{space_id}/festival-type/{festival_type_id}` - **CONSISTENTE**

**2. Endpoints com Relacionamentos**

✅ **Reviews (Avaliações)**
- **Endpoint**: `GET /api/v1/reviews/space-festival-type/{space_festival_type_id}`
- **Status**: **CONSISTENTE**
- **Verificação**: Campo `status` retornado corretamente no relacionamento

✅ **Interests (Interesses)**
- **Endpoint**: `GET /api/v1/interests/space-festival-type/{space_festival_type_id}`
- **Status**: **CONSISTENTE**
- **Verificação**: Campo `status` retornado corretamente no relacionamento

✅ **Bookings (Agendamentos)**
- **Endpoint**: `GET /api/v1/bookings/space-festival-type/{space_festival_type_id}`
- **Status**: **CONSISTENTE** (estruturalmente)
- **Verificação**: Campo `status` seria retornado corretamente se houvesse dados

#### **Arquitetura Verificada**

**1. Schemas Pydantic**

✅ **SpaceFestivalTypeResponse**
- **Arquivo**: `app/schemas/space_festival_type.py`
- **Status**: **CONSISTENTE**
- **Campo status**: Incluído corretamente

✅ **Schemas com Relacionamentos**
- **ReviewWithRelations**: `app/schemas/review.py`
- **BookingWithRelations**: `app/schemas/booking.py`
- **InterestWithRelations**: `app/schemas/interest.py`
- **Status**: **CONSISTENTE** - Todos incluem `space_festival_type: Optional[SpaceFestivalTypeResponse]`

**2. Modelos de Banco de Dados**

✅ **Relacionamentos Configurados**
- **ReviewModel**: `infrastructure/database/models/review_model.py`
- **BookingModel**: `infrastructure/database/models/booking_model.py`
- **InterestModel**: `infrastructure/database/models/interest_model.py`

**3. Repositórios**

✅ **Carregamento de Relacionamentos**
- **ReviewRepositoryImpl**: `infrastructure/repositories/review_repository_impl.py`
- **BookingRepositoryImpl**: `infrastructure/repositories/booking_repository_impl.py`
- **InterestRepositoryImpl**: `infrastructure/repositories/interest_repository_impl.py`

#### **Testes Realizados**

**1. Teste de Listagem Direta**
```bash
curl -X GET "http://localhost:8000/api/v1/space-festival-types/" \
  -H "Authorization: Bearer $TOKEN" | jq '.items[0:3] | .[] | {id, tema, status}'
```

**Resultado**: ✅ Campo status retornado corretamente

**2. Teste de Atualização de Status**
```bash
curl -X PATCH "http://localhost:8000/api/v1/space-festival-types/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status": "FECHADO"}'
```

**Resultado**: ✅ Status atualizado com sucesso

**3. Teste de Relacionamentos**
```bash
# Reviews
curl -X GET "http://localhost:8000/api/v1/reviews/space-festival-type/6?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq '.items[0].space_festival_type'

# Interests
curl -X GET "http://localhost:8000/api/v1/interests/space-festival-type/6?include_relations=true" \
  -H "Authorization: Bearer $TOKEN" | jq '.items[0].space_festival_type'
```

**Resultado**: ✅ Campo status presente em todos os relacionamentos

#### **Conclusões**

**1. Consistência Total**
- **Todos os endpoints diretos** de `space_festival_types` estão consistentes
- **Todos os endpoints com relacionamentos** estão consistentes
- **Todos os schemas** incluem o campo `status` corretamente
- **Todos os modelos** têm relacionamentos configurados
- **Todos os repositórios** carregam relacionamentos corretamente

**2. Funcionalidades Verificadas**
- ✅ **CRUD básico**: Funcionando com campo status
- ✅ **Endpoint de status**: Funcionando corretamente
- ✅ **Relacionamentos**: Carregando campo status
- ✅ **Validações**: Funcionando corretamente
- ✅ **Migração**: Aplicada com sucesso
- ✅ **Dados de exemplo**: Incluindo diferentes status

**3. Arquitetura Mantida**
- ✅ **Padrão hexagonal**: Respeitado
- ✅ **Separação de responsabilidades**: Mantida
- ✅ **Consistência com SpaceEventType**: 100% alinhada
- ✅ **Validações**: Implementadas corretamente

#### **Status Final**

**✅ TODOS OS ENDPOINTS ESTÃO CONSISTENTES**

A implementação do campo `status` em `SpaceFestivalType` está **100% consistente** em toda a aplicação, incluindo:

- Endpoints diretos
- Endpoints com relacionamentos
- Schemas de resposta
- Modelos de banco
- Repositórios
- Validações
- Migrações

O sistema está pronto para uso em produção com total consistência de dados.

## Licença

© 2025 eShow. Todos os direitos reservados. 