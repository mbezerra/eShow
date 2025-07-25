# Arquitetura Hexagonal - eShow API

## Visão Geral

Esta API foi construída seguindo os princípios da **Arquitetura Hexagonal** (também conhecida como Arquitetura de Portas e Adaptadores), que promove a separação de responsabilidades e facilita a manutenção e testabilidade do código.

## Estrutura da Arquitetura

### 1. Domínio (Core) - `domain/`

O domínio contém as regras de negócio e é independente de qualquer tecnologia externa.

#### Entidades (`domain/entities/`)
- **User**: Entidade que representa um usuário do sistema
- **Artist**: Entidade que representa um artista do sistema
- **Profile**: Entidade que representa um perfil de usuário com dados de localização geográfica
- **Role**: Entidade que representa um papel/função no sistema
- **ArtistType**: Entidade que representa um tipo de artista
- **MusicalStyle**: Entidade que representa um estilo musical
- **SpaceType**: Entidade que representa um tipo de espaço
- **EventType**: Entidade que representa um tipo de evento
- **FestivalType**: Entidade que representa um tipo de festival
- **Space**: Entidade que representa um espaço para apresentações
- **Booking**: Entidade que representa um agendamento/reserva
- **Review**: Entidade que representa uma avaliação/review com nota de 1-5 estrelas
- **Financial**: Entidade que representa dados financeiros/bancários com informações PIX
- **Interest**: Entidade que representa manifestações de interesse entre artistas e espaços
- **SpaceEventType**: Entidade que representa relacionamento entre espaços e tipos de eventos
- **SpaceFestivalType**: Entidade que representa relacionamento entre espaços e tipos de festivais
- **ArtistMusicalStyle**: Entidade que representa relacionamento entre artistas e estilos musicais

#### Repositórios (`domain/repositories/`)
- **UserRepository**: Interface para operações de usuários
- **ArtistRepository**: Interface para operações de artistas
- **ProfileRepository**: Interface para operações de perfis
- **RoleRepository**: Interface para operações de papéis
- **ArtistTypeRepository**: Interface para operações de tipos de artista
- **MusicalStyleRepository**: Interface para operações de estilos musicais
- **SpaceTypeRepository**: Interface para operações de tipos de espaço
- **EventTypeRepository**: Interface para operações de tipos de evento
- **FestivalTypeRepository**: Interface para operações de tipos de festival
- **SpaceRepository**: Interface para operações de espaços
- **BookingRepository**: Interface para operações de agendamentos/reservas
- **ReviewRepository**: Interface para operações de avaliações/reviews
- **FinancialRepository**: Interface para operações de dados financeiros/bancários
- **InterestRepository**: Interface para operações de manifestações de interesse
- **SpaceEventTypeRepository**: Interface para operações de relacionamentos espaço-evento
- **SpaceFestivalTypeRepository**: Interface para operações de relacionamentos espaço-festival
- **ArtistMusicalStyleRepository**: Interface para operações de relacionamentos artista-estilo

### 2. Aplicação (`app/`)

A camada de aplicação contém os casos de uso e adaptadores de entrada.

#### API (`app/api/`)
- **Endpoints**: Controllers que expõem a API REST
- **Schemas**: Modelos Pydantic para validação de dados

#### Serviços (`app/application/services/`)
- **UserService**: Orquestra as operações de usuários
- **ArtistService**: Orquestra as operações de artistas
- **ProfileService**: Orquestra as operações de perfis
- **RoleService**: Orquestra as operações de papéis
- **ArtistTypeService**: Orquestra as operações de tipos de artista
- **MusicalStyleService**: Orquestra as operações de estilos musicais
- **SpaceTypeService**: Orquestra as operações de tipos de espaço
- **EventTypeService**: Orquestra as operações de tipos de evento
- **FestivalTypeService**: Orquestra as operações de tipos de festival
- **SpaceService**: Orquestra as operações de espaços
- **BookingService**: Orquestra as operações de agendamentos/reservas
- **ReviewService**: Orquestra as operações de avaliações/reviews
- **FinancialService**: Orquestra as operações de dados financeiros/bancários
- **InterestService**: Orquestra as operações de manifestações de interesse
- **SpaceEventTypeService**: Orquestra as operações de relacionamentos espaço-evento
- **SpaceFestivalTypeService**: Orquestra as operações de relacionamentos espaço-festival
- **ArtistMusicalStyleService**: Orquestra as operações de relacionamentos artista-estilo
- **LocationSearchService**: Orquestra as operações de busca por localização geográfica

### 3. Infraestrutura (`infrastructure/`)

A camada de infraestrutura contém os adaptadores de saída.

#### Banco de Dados (`infrastructure/database/`)
- **Models**: Modelos SQLAlchemy para persistência
- **Database**: Configuração de conexão

#### Repositórios (`infrastructure/repositories/`)
- **UserRepositoryImpl**: Implementação concreta do repositório de usuários
- **ArtistRepositoryImpl**: Implementação concreta do repositório de artistas
- **ProfileRepositoryImpl**: Implementação concreta do repositório de perfis
- **RoleRepositoryImpl**: Implementação concreta do repositório de papéis
- **ArtistTypeRepositoryImpl**: Implementação concreta do repositório de tipos de artista
- **MusicalStyleRepositoryImpl**: Implementação concreta do repositório de estilos musicais
- **SpaceTypeRepositoryImpl**: Implementação concreta do repositório de tipos de espaço
- **EventTypeRepositoryImpl**: Implementação concreta do repositório de tipos de evento
- **FestivalTypeRepositoryImpl**: Implementação concreta do repositório de tipos de festival
- **SpaceRepositoryImpl**: Implementação concreta do repositório de espaços
- **BookingRepositoryImpl**: Implementação concreta do repositório de agendamentos/reservas
- **ReviewRepositoryImpl**: Implementação concreta do repositório de avaliações/reviews
- **FinancialRepositoryImpl**: Implementação concreta do repositório de dados financeiros/bancários
- **InterestRepositoryImpl**: Implementação concreta do repositório de manifestações de interesse
- **SpaceEventTypeRepositoryImpl**: Implementação concreta do repositório de relacionamentos espaço-evento
- **SpaceFestivalTypeRepositoryImpl**: Implementação concreta do repositório de relacionamentos espaço-festival
- **ArtistMusicalStyleRepositoryImpl**: Implementação concreta do repositório de relacionamentos artista-estilo

## Fluxo de Dados

```
API Endpoint → Service → Repository Interface → Repository Implementation → Database
```

### Exemplo: Criar Usuário

1. **API Endpoint** (`app/api/endpoints/users.py`)
   - Recebe requisição HTTP
   - Valida dados com Pydantic
   - Chama o serviço

2. **Service** (`app/application/services/user_service.py`)
   - Contém regras de negócio
   - Cria entidade de domínio
   - Chama repositório

3. **Repository Interface** (`domain/repositories/user_repository.py`)
   - Define contrato abstrato

4. **Repository Implementation** (`infrastructure/repositories/user_repository_impl.py`)
   - Implementa persistência no banco
   - Retorna entidade de domínio

5. **Database** (`infrastructure/database/models/user_model.py`)
   - Modelo SQLAlchemy para persistência

## Benefícios da Arquitetura

### 1. Separação de Responsabilidades
- **Domínio**: Regras de negócio puras
- **Aplicação**: Casos de uso
- **Infraestrutura**: Detalhes técnicos

### 2. Testabilidade
- Cada camada pode ser testada independentemente
- Fácil mock de dependências
- Testes unitários isolados

### 3. Flexibilidade
- Troca de banco de dados sem afetar domínio
- Múltiplas interfaces (REST, GraphQL, CLI)
- Fácil adição de novos recursos

### 4. Manutenibilidade
- Código organizado e previsível
- Mudanças localizadas
- Documentação clara

## Injeção de Dependência

O projeto utiliza injeção de dependência para conectar as camadas:

```python
# app/application/dependencies.py
async def get_user_service():
    user_repository = await get_user_repository()
    return UserService(user_repository)
```

## Testes

### Estrutura de Testes
- **Unitários**: Testam cada camada isoladamente
- **Integração**: Testam fluxo completo
- **E2E**: Testam API completa

### Executar Testes
```bash
pytest tests/
```

## Migrações

O projeto usa Alembic para gerenciar migrações do banco:

```bash
# Criar migração
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrações
alembic upgrade head
```

## Funcionalidades Especiais

### Parâmetro `include_relations`

Implementado nos endpoints GET de Artists, Spaces, Bookings e Reviews para otimizar o carregamento de dados relacionados:

#### Como Funciona
- **Sem `include_relations`**: Retorna apenas a entidade principal com IDs dos relacionamentos
- **Com `include_relations=true`**: Retorna a entidade principal + dados completos dos relacionamentos

#### Implementação Técnica
1. **Repository Layer**: Usa SQLAlchemy `joinedload` para carregar relacionamentos
2. **Service Layer**: Passa o parâmetro para o repositório
3. **API Layer**: Expõe como query parameter opcional

#### Exemplo de Uso
```bash
# Sem relacionamentos
GET /api/v1/spaces/1

# Com relacionamentos
GET /api/v1/spaces/1?include_relations=true
```

#### Relacionamentos Incluídos
- **Artists**: profile, artist_type
- **Spaces**: profile, space_type, event_type, festival_type
- **Bookings**: profile, space, artist, space_event_type, space_festival_type
- **Reviews**: profile, space_event_type, space_festival_type
- **Financials**: profile
- **Interests**: profile_interessado, profile_interesse, space_event_type, space_festival_type

#### Benefícios
- **Performance**: Evita N+1 queries
- **Flexibilidade**: Cliente decide quando carregar relacionamentos
- **Compatibilidade**: Mantém compatibilidade com versões anteriores

## Relacionamentos N:N

### Visão Geral

O sistema implementa relacionamentos N:N entre entidades para permitir associações flexíveis entre espaços e tipos de eventos/festivais.

### Relacionamentos Implementados

#### 1. Space Event Types
- **Entidade**: `SpaceEventType` - Relacionamento entre espaços e tipos de eventos
- **Campos**: space_id, event_type_id, tema, descricao, status, link_divulgacao, banner, data, horario
- **Status**: Campo `status` com valores CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
- **Endpoint específico**: `PATCH /api/v1/space-event-types/{id}/status` para atualização de status

#### 2. Space Festival Types
- **Entidade**: `SpaceFestivalType` - Relacionamento entre espaços e tipos de festivais
- **Campos**: space_id, festival_type_id, tema, descricao, status, link_divulgacao, banner, data, horario
- **Status**: Campo `status` com valores CONTRATANDO, FECHADO, SUSPENSO, CANCELADO
- **Endpoint específico**: `PATCH /api/v1/space-festival-types/{id}/status` para atualização de status

#### 3. Artist Musical Styles
- **Entidade**: `ArtistMusicalStyle` - Relacionamento entre artistas e estilos musicais
- **Campos**: artist_id, musical_style_id

### Arquitetura dos Relacionamentos

#### Entidades de Domínio
```python
# domain/entities/space_event_type.py
class SpaceEventType:
    def __init__(self, 
                 space_id: int,
                 event_type_id: int,
                 tema: str,
                 descricao: str,
                 status: StatusEventType = StatusEventType.CONTRATANDO,
                 link_divulgacao: Optional[str] = None,
                 banner: Optional[str] = None,
                 data: datetime,
                 horario: str,
                 id: Optional[int] = None):

# domain/entities/space_festival_type.py
class SpaceFestivalType:
    def __init__(self, 
                 space_id: int,
                 festival_type_id: int,
                 tema: str,
                 descricao: str,
                 status: StatusFestivalType = StatusFestivalType.CONTRATANDO,
                 link_divulgacao: Optional[str] = None,
                 banner: Optional[str] = None,
                 data: datetime,
                 horario: str,
                 id: Optional[int] = None):
```

#### Repositórios
```python
# domain/repositories/space_event_type_repository.py
class SpaceEventTypeRepository(ABC):
    @abstractmethod
    def update_status(self, space_event_type_id: int, status: StatusEventType) -> Optional[SpaceEventType]:
        """Atualizar apenas o status de um relacionamento"""
        pass

# domain/repositories/space_festival_type_repository.py
class SpaceFestivalTypeRepository(ABC):
    @abstractmethod
    def update_status(self, space_festival_type_id: int, status: StatusFestivalType) -> Optional[SpaceFestivalType]:
        """Atualizar apenas o status de um relacionamento"""
        pass
```

#### Serviços
```python
# app/application/services/space_event_type_service.py
class SpaceEventTypeService:
    def update_space_event_type_status(self, space_event_type_id: int, status: StatusEventType) -> Optional[SpaceEventType]:
        """Atualizar apenas o status de um relacionamento"""
        return self.space_event_type_repository.update_status(space_event_type_id, status)

# app/application/services/space_festival_type_service.py
class SpaceFestivalTypeService:
    def update_space_festival_type_status(self, space_festival_type_id: int, status: StatusFestivalType) -> Optional[SpaceFestivalType]:
        """Atualizar apenas o status de um relacionamento"""
        return self.space_festival_type_repository.update_status(space_festival_type_id, status)
```

#### Endpoints
```python
# app/api/endpoints/space_event_types.py
@router.patch("/{space_event_type_id}/status", response_model=SpaceEventTypeResponse)
def update_space_event_type_status(
    space_event_type_id: int,
    status_data: SpaceEventTypeStatusUpdate,
    space_event_type_service: SpaceEventTypeService = Depends(get_space_event_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar apenas o status de um relacionamento (requer autenticação)"""

# app/api/endpoints/space_festival_types.py
@router.patch("/{space_festival_type_id}/status", response_model=SpaceFestivalTypeResponse)
def update_space_festival_type_status(
    space_festival_type_id: int,
    status_data: SpaceFestivalTypeStatusUpdate,
    space_festival_type_service: SpaceFestivalTypeService = Depends(get_space_festival_type_service),
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Atualizar apenas o status de um relacionamento (requer autenticação)"""
```

### Benefícios da Arquitetura

- **Flexibilidade**: Espaços podem oferecer múltiplos tipos de eventos
- **Status Management**: Controle granular do estado dos eventos
- **Extensibilidade**: Fácil adição de novos relacionamentos
- **Consistência**: Validações e regras de negócio centralizadas
- **Performance**: Consultas otimizadas com índices apropriados

## Sistema de Controle de Acesso por Roles

### Implementação

O sistema implementa validação de roles nos serviços de domínio para garantir que apenas usuários com o papel adequado possam cadastrar determinados tipos de entidades.

#### Validação nos Serviços

**ArtistService**:
```python
def create_artist(self, artist_data: ArtistCreate) -> Artist:
    # Validar se o profile tem role_id = 2 (ARTISTA)
    profile = self.profile_repository.get_by_id(artist_data.profile_id)
    if profile.role_id != 2:
        raise ValueError("Apenas perfis com role 'ARTISTA' podem cadastrar artistas")
```

**SpaceService**:
```python
def create_space(self, space_data: dict) -> Space:
    # Validar se o profile tem role_id = 3 (ESPACO)
    profile = self.profile_repository.get_by_id(space_data["profile_id"])
    if profile.role_id != 3:
        raise ValueError("Apenas perfis com role 'ESPACO' podem cadastrar espaços")
```

#### Roles e Restrições

- **ADMIN** (`role_id = 1`): Administradores do sistema
- **ARTISTA** (`role_id = 2`): Podem cadastrar artistas
- **ESPACO** (`role_id = 3`): Podem cadastrar espaços

#### Benefícios

- **Segurança**: Controle de acesso granular
- **Integridade**: Garante que apenas entidades adequadas sejam criadas
- **Validação**: Mensagens de erro claras para tentativas inválidas
- **Flexibilidade**: Sistema extensível para novos roles

## Sistema de Manifestações de Interesse (Interests)

### Visão Geral

O sistema de **Interests** permite que artistas manifestem interesse em se apresentar em espaços específicos e vice-versa, facilitando a conexão entre profissionais e estabelecimentos.

### Arquitetura da Funcionalidade

#### Entidade Interest (`domain/entities/interest.py`)

```python
class Interest:
    def __init__(self, 
                 profile_id_interessado: int,
                 profile_id_interesse: int,
                 data_inicial: date,
                 horario_inicial: time,
                 duracao_apresentacao: float,
                 valor_hora_ofertado: float,
                 valor_couvert_ofertado: float,
                 mensagem: str,
                 status: str = "AGUARDANDO_CONFIRMACAO",
                 resposta: str = None,
                 id: int = None):
```

#### Regras de Negócio Implementadas

1. **Validação de Roles**:
   - Apenas **artistas** podem manifestar interesse em **espaços**
   - Apenas **espaços** podem manifestar interesse em **artistas**

2. **Prevenção de Duplicatas**:
   - Não é possível manifestar interesse duplicado entre os mesmos profiles
   - Validação automática no serviço

3. **Estados de Status**:
   - "AGUARDANDO_CONFIRMACAO" (padrão)
   - "ACEITO" (com resposta opcional)
- "RECUSADO" (com resposta opcional)

4. **Validações de Dados**:
   - Data inicial deve ser futura
   - Duração entre 0.5 e 8 horas
   - Valores monetários positivos
   - Mensagem obrigatória (10-1000 caracteres)

#### Endpoints Especializados

1. **Gestão de Status**:
   - `PATCH /interests/{id}/accept` - Aceitar manifestação
   - `PATCH /interests/{id}/reject` - Recusar manifestação
   - `PATCH /interests/{id}/status` - Atualizar status customizado

2. **Consultas por Profile**:
   - `GET /interests/profile/interessado/{id}` - Manifestações enviadas
   - `GET /interests/profile/interesse/{id}` - Manifestações recebidas
   - `GET /interests/profile/{id}/pending` - Manifestações pendentes
   - `GET /interests/profile/{id}/statistics` - Estatísticas detalhadas

3. **Filtros Avançados**:
   - `GET /interests/status/{status}` - Por status
   - `GET /interests/space-event-type/{id}` - Por tipo de evento
   - `GET /interests/date-range/` - Por período

#### Implementação Técnica

**Service Layer** (`app/application/services/interest_service.py`):
```python
def create_interest(self, interest_data: InterestCreate) -> Interest:
    # Validação de roles
    profile_interessado = self.profile_repository.get_by_id(interest_data.profile_id_interessado)
    profile_interesse = self.profile_repository.get_by_id(interest_data.profile_id_interesse)
    
    # Verificar se são roles compatíveis (artista ↔ espaço)
    if not self._validate_interest_roles(profile_interessado, profile_interesse):
        raise ValueError("Apenas artistas podem manifestar interesse em espaços e vice-versa")
    
    # Verificar duplicatas
    if self._check_duplicate_interest(interest_data):
        raise ValueError("Já existe uma manifestação de interesse entre estes profiles")
    
    # Criar entidade e persistir
    interest = Interest(**interest_data.dict())
    return self.interest_repository.create(interest)
```

**Repository Layer** (`infrastructure/repositories/interest_repository_impl.py`):
```python
def get_by_profile_interessado(self, profile_id: int, include_relations: bool = False) -> List[Interest]:
    query = self.db.query(InterestModel).filter(InterestModel.profile_id_interessado == profile_id)
    
    if include_relations:
        query = query.options(
            joinedload(InterestModel.profile_interessado),
            joinedload(InterestModel.profile_interesse),
            joinedload(InterestModel.space_event_type),
            joinedload(InterestModel.space_festival_type)
        )
    
    return [self._to_entity(model) for model in query.all()]
```

#### Benefícios da Implementação

1. **Flexibilidade**: Suporte a diferentes tipos de relacionamento (artista→espaço, espaço→artista)
2. **Controle**: Estados de status bem definidos com transições controladas
3. **Performance**: Consultas otimizadas com relacionamentos opcionais
4. **Segurança**: Validação de roles e prevenção de duplicatas
5. **Usabilidade**: Endpoints especializados para casos de uso comuns

## Próximos Passos

1. ✅ ~~Implementar autenticação JWT~~
2. ✅ ~~Adicionar validações de negócio~~
3. ✅ ~~Implementar sistema de manifestações de interesse~~
4. Implementar cache Redis
5. Adicionar logs estruturados
6. Configurar CI/CD
7. ✅ ~~Implementar documentação OpenAPI~~
8. ✅ ~~Implementar sistema de busca por localização~~

## Sistema de Busca por Localização

### Visão Geral

O sistema de **Location Search** permite que artistas encontrem espaços dentro do seu raio de atuação e que espaços encontrem artistas disponíveis, baseado em cálculos geográficos e disponibilidade de agenda.

### Arquitetura da Funcionalidade

#### Componentes Principais

1. **LocationUtils** (`app/core/location_utils.py`)
   - Cálculo de distância usando fórmula de Haversine
   - Integração com API ViaCEP para coordenadas geográficas
   - Sistema de fallback com coordenadas aproximadas
   - Validação de raio de atuação

2. **LocationSearchService** (`app/application/services/location_search_service.py`)
   - Orquestração da lógica de busca
   - Validação de disponibilidade de eventos/festivais
   - Verificação de conflitos de agendamento
   - Filtros por status e raio de atuação

3. **Schemas de Resposta** (`app/schemas/location_search.py`)
   - Estruturas de dados padronizadas para respostas
   - Suporte a dados completos ou apenas IDs
   - Metadados de busca (raio, origem, contagem)

#### Fluxo de Busca

**Endpoint 1: Busca de Espaços para Artista**
```
1. Validar autenticação e role (artista)
2. Obter profile e dados do artista
3. Buscar todos os profiles de espaços (role_id = 3)
4. Para cada espaço:
   - Calcular distância entre CEPs
   - Verificar se está dentro do raio de atuação
   - Verificar se tem eventos/festivais com status "CONTRATANDO"
5. Retornar resultados ordenados por distância
```

**Endpoint 2: Busca de Artistas para Espaço**
```
1. Validar autenticação e role (espaço)
2. Obter profile e dados do espaço
3. Buscar todos os profiles de artistas (role_id = 2)
4. Para cada artista:
   - Calcular distância entre CEPs
   - Verificar se está dentro do raio de atuação do artista
   - Verificar se não tem agendamentos conflitantes
5. Retornar resultados ordenados por distância
```

#### Implementação Técnica

**LocationUtils**:
```python
class LocationUtils:
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula distância entre dois pontos usando fórmula de Haversine"""
        
    @staticmethod
    def get_coordinates_from_cidade_uf(cidade: str, uf: str) -> Optional[Tuple[float, float]]:
        """Obtém coordenadas geográficas de uma cidade/UF da base local"""
        
    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normaliza texto removendo acentos e convertendo para maiúsculas"""
        
    @staticmethod
    def search_cities_by_name(cidade: str, limit: int = 10) -> list:
        """Busca cidades por nome (insensível a acentos)"""
        
    @staticmethod
    def get_nearby_cities(latitude: float, longitude: float, radius_km: float = 50) -> list:
        """Busca cidades próximas a um ponto geográfico"""
```

**LocationSearchService**:
```python
class LocationSearchService:
    def search_spaces_for_artist(
        self,
        db: Session,
        artist_profile_id: int,
        return_full_data: bool = True,
        max_results: Optional[int] = 100
    ) -> LocationSearchResponse:
        """Busca espaços para um artista baseado no seu raio de atuação"""
        
    def search_artists_for_space(
        self,
        db: Session,
        space_profile_id: int,
        return_full_data: bool = True,
        max_results: Optional[int] = 100
    ) -> LocationSearchResponse:
        """Busca artistas para um espaço baseado no raio de atuação dos artistas"""
```

#### Endpoints da API

**GET/POST `/api/v1/location-search/spaces-for-artist`**
- **Autenticação**: JWT obrigatório
- **Role**: Apenas artistas (role_id = 2)
- **Parâmetros**: `return_full_data`, `max_results`
- **Resposta**: Lista de espaços com distância calculada

**GET/POST `/api/v1/location-search/artists-for-space`**
- **Autenticação**: JWT obrigatório
- **Role**: Apenas espaços (role_id = 3)
- **Parâmetros**: `return_full_data`, `max_results`
- **Resposta**: Lista de artistas com distância calculada

#### Regras de Negócio

1. **Validação de Roles**:
   - Artistas só podem buscar espaços
   - Espaços só podem buscar artistas

2. **Cálculo de Distância**:
   - Baseado na fórmula de Haversine
   - Coordenadas obtidas da base local (5.565 municípios)
   - Dados oficiais do IBGE com 100% de cobertura

3. **Busca Insensível a Acentos**:
   - Normalização automática de nomes de cidades
   - Coluna `cidade_normalizada` para busca otimizada
   - Exemplos: "São Paulo" = "SAO PAULO" = "são paulo"

4. **Filtros de Disponibilidade**:
   - Espaços devem ter eventos/festivais com status "CONTRATANDO"
   - Artistas não devem ter agendamentos conflitantes

5. **Performance**:
   - Limite configurável de resultados
   - Opção de retornar dados completos ou apenas IDs
   - Índices otimizados na base de dados

#### Benefícios da Implementação

1. **Precisão Geográfica**: Cálculos baseados em coordenadas reais do IBGE
2. **Cobertura Completa**: 100% dos municípios brasileiros incluídos
3. **Flexibilidade**: Suporte a diferentes raios de atuação
4. **Busca Inteligente**: Insensível a acentuação ortográfica
5. **Performance**: Filtros otimizados e índices na base de dados
6. **Confiabilidade**: Dados oficiais sem dependência de APIs externas
7. **Segurança**: Validação de roles e autenticação
8. **Escalabilidade**: Arquitetura preparada para otimizações futuras 