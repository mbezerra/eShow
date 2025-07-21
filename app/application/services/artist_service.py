from typing import List, Optional, Union
from domain.entities.artist import Artist
from domain.repositories.artist_repository import ArtistRepository
from app.schemas.artist import ArtistCreate, ArtistUpdate
from infrastructure.database.models.artist_model import ArtistModel

class ArtistService:
    def __init__(self, artist_repository: ArtistRepository):
        self.artist_repository = artist_repository

    def create_artist(self, artist_data: ArtistCreate) -> Artist:
        """Criar um novo artista"""
        # Verificar se já existe um artista para este profile
        existing_artist = self.artist_repository.get_by_profile_id(artist_data.profile_id)
        if existing_artist:
            raise ValueError("Já existe um artista cadastrado para este profile")

        artist = Artist(
            profile_id=artist_data.profile_id,
            artist_type_id=artist_data.artist_type_id,
            dias_apresentacao=artist_data.dias_apresentacao,
            raio_atuacao=artist_data.raio_atuacao,
            duracao_apresentacao=artist_data.duracao_apresentacao,
            valor_hora=artist_data.valor_hora,
            valor_couvert=artist_data.valor_couvert,
            requisitos_minimos=artist_data.requisitos_minimos,
            instagram=artist_data.instagram,
            tiktok=artist_data.tiktok,
            youtube=artist_data.youtube,
            facebook=artist_data.facebook,
            soundcloud=artist_data.soundcloud,
            bandcamp=artist_data.bandcamp,
            spotify=artist_data.spotify,
            deezer=artist_data.deezer
        )

        return self.artist_repository.create(artist)

    def get_artist_by_id(self, artist_id: int, include_relations: bool = False) -> Optional[Union[Artist, ArtistModel]]:
        """Obter artista por ID"""
        return self.artist_repository.get_by_id(artist_id, include_relations=include_relations)

    def get_artist_by_profile_id(self, profile_id: int, include_relations: bool = False) -> Optional[Union[Artist, ArtistModel]]:
        """Obter artista por ID do profile"""
        return self.artist_repository.get_by_profile_id(profile_id, include_relations=include_relations)

    def get_artists(self, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Artist, ArtistModel]]:
        """Listar todos os artistas"""
        return self.artist_repository.get_all(skip=skip, limit=limit, include_relations=include_relations)

    def get_artists_by_type(self, artist_type_id: int, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Artist, ArtistModel]]:
        """Listar artistas por tipo"""
        return self.artist_repository.get_by_artist_type(artist_type_id, skip=skip, limit=limit, include_relations=include_relations)

    def update_artist(self, artist_id: int, artist_data: ArtistUpdate) -> Artist:
        """Atualizar artista"""
        artist = self.artist_repository.get_by_id(artist_id)
        if not artist:
            raise ValueError("Artista não encontrado")

        # Atualizar apenas os campos fornecidos
        if artist_data.profile_id is not None:
            # Verificar se o novo profile_id já tem um artista
            existing_artist = self.artist_repository.get_by_profile_id(artist_data.profile_id)
            if existing_artist and existing_artist.id != artist_id:
                raise ValueError("Já existe um artista cadastrado para este profile")
            artist.profile_id = artist_data.profile_id

        if artist_data.artist_type_id is not None:
            artist.artist_type_id = artist_data.artist_type_id

        if artist_data.dias_apresentacao is not None:
            artist.update_dias_apresentacao(artist_data.dias_apresentacao)

        if artist_data.raio_atuacao is not None:
            artist.update_raio_atuacao(artist_data.raio_atuacao)

        if artist_data.duracao_apresentacao is not None:
            artist.update_duracao_apresentacao(artist_data.duracao_apresentacao)

        if artist_data.valor_hora is not None:
            artist.update_valor_hora(artist_data.valor_hora)

        if artist_data.valor_couvert is not None:
            artist.update_valor_couvert(artist_data.valor_couvert)

        if artist_data.requisitos_minimos is not None:
            artist.update_requisitos_minimos(artist_data.requisitos_minimos)

        # Atualizar redes sociais
        social_platforms = [
            'instagram', 'tiktok', 'youtube', 'facebook', 
            'soundcloud', 'bandcamp', 'spotify', 'deezer'
        ]
        
        for platform in social_platforms:
            value = getattr(artist_data, platform)
            if value is not None:
                artist.update_social_media(platform, value)

        return self.artist_repository.update(artist)

    def delete_artist(self, artist_id: int) -> bool:
        """Deletar artista"""
        return self.artist_repository.delete(artist_id) 