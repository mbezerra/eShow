# eShow API

Versão: 0.22.0

Sistema de gerenciamento para artistas e espaços de entretenimento, desenvolvido com **FastAPI** e arquitetura hexagonal.

## 🎯 **Funcionalidades Principais**

- **Gestão de Usuários** com autenticação JWT
- **Sistema de Perfis** (Artists e Spaces) com coordenadas geográficas
- **Gerenciamento de Artistas** e estilos musicais
- **Administração de Espaços** e tipos de evento
- **Sistema de Agendamentos/Reservas** (Bookings)
- **Sistema de Avaliações/Reviews** com notas de 1 a 5 estrelas
- **Sistema Financeiro/Bancário** com dados PIX e transferências
- **Sistema de Manifestações de Interesse** (Interests) entre artistas e espaços
- **Sistema de Busca por Localização** com cálculo de distância geográfica
- **Relacionamentos N:N** entre entidades
- **API REST** completa com documentação automática
- **Arquitetura Hexagonal** para facilitar manutenção

## 📊 **Estatísticas do Projeto**

- **Total de Endpoints:** 151
- **Entidades de Domínio:** 18
- **Tabelas no Banco:** 18
- **Schemas Pydantic:** 20 arquivos principais
- **Cobertura de Testes:** Em desenvolvimento
- **Versão Atual:** v0.22.0

## 🆕 **Funcionalidades Recentes**

### Busca Insensível a Acentos ✅ **NOVO**
- **Busca por cidade ignora acentuação ortográfica** completamente
- **Normalização automática** de todos os 5.565 municípios brasileiros
- **Exemplos funcionais**: "São Paulo" = "SAO PAULO" = "são paulo"
- **Busca parcial** funciona com termos normalizados
- **Performance otimizada** com índice na coluna normalizada
- **Flexibilidade total** para cadastros com ou sem acentos

### Campo Status em Space Event Types e Space Festival Types
- **Novo campo `status`** com valores: CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
- **Endpoint específico** para atualização de status: `PATCH /api/v1/space-event-types/{id}/status` e `PATCH /api/v1/space-festival-types/{id}/status`
- **Valor padrão:** CONTRATANDO para novos registros
- **Consistência total** em todos os endpoints relacionados

### Sistema de Busca por Localização Otimizado ✅ **v0.22.0 - NOVO**
- **4 novos endpoints** para busca geográfica baseada em raio de atuação
- **Cálculo de distância** usando fórmula de Haversine com dados reais
- **Base de dados primária** com 5.565 municípios brasileiros (100% cobertura)
- **Dados oficiais do IBGE** com coordenadas reais e precisas
- **Validação de disponibilidade** baseada em status de eventos/festivais
- **Verificação de conflitos** de agendamento para artistas
- **Autenticação e autorização** por role (artista/espaço)
- **Sistema confiável** baseado em dados reais da base IBGE
- **Nova hierarquia de coordenadas**: Prioridade para coordenadas do Profile, fallback para base local e ViaCEP
- **Performance otimizada**: 50-80% mais rápido com coordenadas diretas
- **Cache inteligente**: Redução de consultas repetidas
- **Testes abrangentes**: 12 testes unitários e de integração

### Coordenadas Geográficas em Perfis ✅ **NOVO**
- **Campos `latitude` e `longitude`** opcionais em todos os perfis
- **Integração com sistema de busca** por localização
- **Cálculo de distâncias** otimizado para proximidade
- **Validação de coordenadas** (latitude: -90 a 90, longitude: -180 a 180)
- **Compatibilidade total** com perfis existentes
- **Migração automática** aplicada ao banco de dados

### Documentação Completa ✅ **NOVO**
- **Todas as documentações sincronizadas** e atualizadas para v0.20.0
- **API_USAGE.md** - Exemplos de uso detalhados incluindo coordenadas geográficas
- **IMPLEMENTATION_SUMMARY.md** - Resumo técnico completo atualizado
- **ARCHITECTURE.md** - Arquitetura detalhada com entidades atualizadas
- **DATABASE_STRATEGY.md** - Estratégia de banco com consultas otimizadas
- **VERSIONING.md** - Changelog completo e versionamento automatizado
- **SCRIPTS_README.md** - Documentação de scripts atualizada

### Sistema Estabilizado ✅ **NOVO**
- **151 endpoints funcionais** testados e documentados
- **18 entidades de domínio** com arquitetura hexagonal consolidada
- **18 tabelas no banco** com estrutura otimizada
- **20 schemas Pydantic** com validação robusta
- **Sistema de coordenadas** integrado com busca geográfica
- **Testes automatizados** com cobertura implementada

## 📁 **Estrutura do Projeto**

```
eShow/
├── app/                   # Camada de aplicação
│   ├── api/              # Endpoints da API
│   ├── core/             # Configurações e autenticação
│   ├── schemas/          # Modelos Pydantic
│   └── application/      # Serviços e casos de uso
├── domain/               # Camada de domínio
│   ├── entities/         # Entidades de negócio
│   └── repositories/     # Interfaces dos repositórios
├── infrastructure/       # Camada de infraestrutura
│   ├── database/         # Modelos e configuração do banco
│   ├── repositories/     # Implementação dos repositórios
├── tests/                # Testes unitários e de integração
├── alembic/              # Migrações do banco de dados
├── *.md                  # Documentação principal
├── *.py                  # Scripts utilitários e inicialização
```

## Princípios da Arquitetura Hexagonal

1. **Domínio (Core)**: Contém as regras de negócio e entidades
2. **Aplicação**: Contém os casos de uso e adaptadores de entrada
3. **Infraestrutura**: Contém adaptadores de saída (banco de dados, APIs externas)

## Como Executar

### Versionamento Automático
O projeto utiliza versionamento automático baseado em tags Git. Veja [VERSIONING.md](VERSIONING.md) para detalhes.

```bash
# Verificar versão atual
python version.py show

# Criar nova versão
python version.py patch  # ou minor/major
```

### Desenvolvimento (SQLite)

**Opção 1: Usando script de inicialização (Recomendado)**
```bash
./start_server.sh
```

**Opção 2: Configuração manual**
1. Criar e ativar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. Instalar dependências:
```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:
```bash
cp env.example .env
# Editar o arquivo .env e configurar SECRET_KEY
```

4. Inicializar banco de dados:
```bash
python init_db.py
```

5. Iniciar o servidor:
```bash
python run.py
```

### Produção (PostgreSQL)

1. Instalar PostgreSQL e criar banco:
```bash
sudo apt-get install postgresql postgresql-contrib

# Criar banco e usuário
sudo -u postgres psql
CREATE DATABASE eshow;
CREATE USER eshow_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE eshow TO eshow_user;
\q
```

2. Configurar DATABASE_URL no .env:
```bash
DATABASE_URL=postgresql://eshow_user:your_password@localhost/eshow
```

3. Migrar dados do SQLite para PostgreSQL:
```bash
python migrate_to_postgres.py
```

4. Executar migrações:
```bash
alembic upgrade head
```

## Sistema de Roles

O sistema implementa controle de acesso baseado em roles para garantir que apenas usuários adequados possam cadastrar determinados tipos de entidades:

### Roles Disponíveis
- **ADMIN** (`role_id = 1`): Administradores do sistema
- **ARTISTA** (`role_id = 2`): Artistas e músicos
- **ESPACO** (`role_id = 3`): Estabelecimentos e espaços de eventos

### Restrições por Role
- **Artists**: Apenas profiles com role "ARTISTA" podem cadastrar artistas
- **Spaces**: Apenas profiles com role "ESPACO" podem cadastrar espaços
- **Profiles**: Cada usuário deve ter um profile associado a um role específico

## Endpoints

A API possui 151 endpoints RESTful cobrindo autenticação, usuários, perfis, artistas, espaços, tipos, agendamentos, avaliações, interesses, busca por localização, entre outros. Veja [API_USAGE.md](API_USAGE.md) para exemplos detalhados de uso e respostas.

## Scripts de Inicialização e Utilitários

- **start_server.sh**: Inicializa o ambiente virtual, instala dependências e executa o servidor.
- **init_db.py**: Inicializa o banco de dados.
- **migrate_to_postgres.py**: Migra dados do SQLite para PostgreSQL.
- **init_*.py**: Scripts para popular tabelas com dados iniciais (roles, tipos, artistas, etc).
- **version.py**: Gerencia versionamento automático via Git tags.

## Documentação

- [API_USAGE.md](API_USAGE.md): Exemplos de uso dos endpoints
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md): Resumo técnico e histórico de versões
- [ARCHITECTURE.md](ARCHITECTURE.md): Detalhes da arquitetura hexagonal
- [DATABASE_STRATEGY.md](DATABASE_STRATEGY.md): Estratégia e estrutura do banco de dados
- [VERSIONING.md](VERSIONING.md): Estratégia e comandos de versionamento

## Observações

- O projeto está em desenvolvimento ativo.
- Para dúvidas sobre uso da API, consulte a documentação automática em `http://localhost:8000/docs`.
- Para detalhes de implementação, consulte os arquivos `.md` na raiz do projeto.
- Scripts de inicialização populam as tabelas com valores esperados (roles, tipos, etc).

---

A API estará disponível em `http://localhost:8000`
A documentação automática estará em `http://localhost:8000/docs` 