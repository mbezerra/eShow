from typing import List, Optional, Union
from pydantic import BaseModel
from datetime import datetime

class LocationSearchResult(BaseModel):
    """Schema base para resultados de busca por localização"""
    id: int
    distance_km: Optional[float] = None

    model_config = {"from_attributes": True}

class ProfileLocationResult(BaseModel):
    """Schema para resultados de busca de profiles por localização"""
    full_name: str
    artistic_name: str
    cep: str
    cidade: str
    uf: str

    model_config = {"from_attributes": True}

class ArtistLocationResult(LocationSearchResult):
    """Schema para resultados de busca de artists por localização"""
    profile_id: int
    artist_type_id: int
    raio_atuacao: float
    valor_hora: float
    valor_couvert: float
    profile: ProfileLocationResult

    model_config = {"from_attributes": True}

class SpaceLocationResult(LocationSearchResult):
    """Schema para resultados de busca de spaces por localização"""
    profile_id: int
    space_type_id: int
    acesso: str
    valor_hora: float
    valor_couvert: float
    publico_estimado: str
    profile: ProfileLocationResult

    model_config = {"from_attributes": True}

class SpaceEventTypeLocationResult(LocationSearchResult):
    """Schema para resultados de busca de space_event_types por localização"""
    space_id: int
    event_type_id: int
    tema: str
    descricao: str
    data: datetime
    horario: str
    status: str
    space: SpaceLocationResult

    model_config = {"from_attributes": True}

class SpaceFestivalTypeLocationResult(LocationSearchResult):
    """Schema para resultados de busca de space_festival_types por localização"""
    space_id: int
    festival_type_id: int
    tema: str
    descricao: str
    data: datetime
    horario: str
    status: str
    space: SpaceLocationResult

    model_config = {"from_attributes": True}

class LocationSearchResponse(BaseModel):
    """Schema para resposta de busca por localização"""
    results: List[Union[
        ProfileLocationResult,
        ArtistLocationResult,
        SpaceLocationResult,
        SpaceEventTypeLocationResult,
        SpaceFestivalTypeLocationResult
    ]]
    total_count: int
    search_radius_km: float
    origin_cep: str

    model_config = {"from_attributes": True}

class LocationSearchRequest(BaseModel):
    """Schema para requisição de busca por localização"""
    return_full_data: bool = True  # True para dados completos, False para apenas IDs
    max_results: Optional[int] = 100  # Limite máximo de resultados

    model_config = {"from_attributes": True} 