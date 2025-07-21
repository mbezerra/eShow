from typing import List, Optional
from domain.entities.artist_type import ArtistType, ArtistTypeEnum
from domain.repositories.artist_type_repository import ArtistTypeRepository
from app.schemas.artist_type import ArtistTypeCreate, ArtistTypeUpdate, ArtistTypeResponse

class ArtistTypeService:
    def __init__(self, artist_type_repository: ArtistTypeRepository):
        self.artist_type_repository = artist_type_repository

    def create_artist_type(self, artist_type_data: ArtistTypeCreate) -> ArtistTypeResponse:
        existing = self.artist_type_repository.get_by_tipo(artist_type_data.tipo)
        if existing:
            raise ValueError("Tipo de artista já existe")
        artist_type = ArtistType(tipo=artist_type_data.tipo)
        created = self.artist_type_repository.create(artist_type)
        return ArtistTypeResponse(
            id=created.id,
            tipo=created.tipo,
            created_at=created.created_at,
            updated_at=created.updated_at
        )

    def get_artist_types(self, skip: int = 0, limit: int = 100) -> List[ArtistTypeResponse]:
        artist_types = self.artist_type_repository.get_all(skip=skip, limit=limit)
        return [
            ArtistTypeResponse(
                id=at.id,
                tipo=at.tipo,
                created_at=at.created_at,
                updated_at=at.updated_at
            ) for at in artist_types
        ]

    def get_artist_type_by_id(self, artist_type_id: int) -> Optional[ArtistTypeResponse]:
        at = self.artist_type_repository.get_by_id(artist_type_id)
        if not at:
            return None
        return ArtistTypeResponse(
            id=at.id,
            tipo=at.tipo,
            created_at=at.created_at,
            updated_at=at.updated_at
        )

    def update_artist_type(self, artist_type_id: int, artist_type_data: ArtistTypeUpdate) -> Optional[ArtistTypeResponse]:
        at = self.artist_type_repository.get_by_id(artist_type_id)
        if not at:
            return None
        if artist_type_data.tipo is not None:
            existing = self.artist_type_repository.get_by_tipo(artist_type_data.tipo)
            if existing and existing.id != artist_type_id:
                raise ValueError("Tipo de artista já existe")
            at.tipo = artist_type_data.tipo
        at.updated_at = at.updated_at
        updated = self.artist_type_repository.update(at)
        return ArtistTypeResponse(
            id=updated.id,
            tipo=updated.tipo,
            created_at=updated.created_at,
            updated_at=updated.updated_at
        )

    def delete_artist_type(self, artist_type_id: int) -> bool:
        return self.artist_type_repository.delete(artist_type_id) 