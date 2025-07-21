from typing import List, Optional, Union
from sqlalchemy.orm import Session, joinedload
from domain.entities.artist import Artist
from domain.repositories.artist_repository import ArtistRepository
from infrastructure.database.models.artist_model import ArtistModel
import json

class ArtistRepositoryImpl(ArtistRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, artist: Artist) -> Artist:
        """Criar um novo artista"""
        db_artist = ArtistModel(
            profile_id=artist.profile_id,
            artist_type_id=artist.artist_type_id,
            dias_apresentacao=json.dumps(artist.dias_apresentacao),
            raio_atuacao=artist.raio_atuacao,
            duracao_apresentacao=artist.duracao_apresentacao,
            valor_hora=artist.valor_hora,
            valor_couvert=artist.valor_couvert,
            requisitos_minimos=artist.requisitos_minimos,
            instagram=artist.instagram,
            tiktok=artist.tiktok,
            youtube=artist.youtube,
            facebook=artist.facebook,
            soundcloud=artist.soundcloud,
            bandcamp=artist.bandcamp,
            spotify=artist.spotify,
            deezer=artist.deezer
        )
        
        self.db.add(db_artist)
        self.db.commit()
        self.db.refresh(db_artist)
        
        return self._to_entity(db_artist)

    def get_by_id(self, artist_id: int, include_relations: bool = False) -> Optional[Union[Artist, ArtistModel]]:
        """Obter artista por ID"""
        query = self.db.query(ArtistModel)
        if include_relations:
            query = query.options(
                joinedload(ArtistModel.profile),
                joinedload(ArtistModel.artist_type)
            )
        db_artist = query.filter(ArtistModel.id == artist_id).first()
        if not db_artist:
            return None
        
        # Se include_relations=True, retornar o modelo do banco diretamente
        if include_relations:
            return db_artist
        else:
            return self._to_entity(db_artist)

    def get_by_profile_id(self, profile_id: int, include_relations: bool = False) -> Optional[Union[Artist, ArtistModel]]:
        """Obter artista por ID do profile"""
        query = self.db.query(ArtistModel)
        if include_relations:
            query = query.options(
                joinedload(ArtistModel.profile),
                joinedload(ArtistModel.artist_type)
            )
        db_artist = query.filter(ArtistModel.profile_id == profile_id).first()
        if not db_artist:
            return None
        
        # Se include_relations=True, retornar o modelo do banco diretamente
        if include_relations:
            return db_artist
        else:
            return self._to_entity(db_artist)

    def get_all(self, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Artist, ArtistModel]]:
        """Listar todos os artistas"""
        query = self.db.query(ArtistModel)
        if include_relations:
            query = query.options(
                joinedload(ArtistModel.profile),
                joinedload(ArtistModel.artist_type)
            )
        db_artists = query.offset(skip).limit(limit).all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_artists
        else:
            return [self._to_entity(db_artist) for db_artist in db_artists]

    def get_by_artist_type(self, artist_type_id: int, skip: int = 0, limit: int = 100, include_relations: bool = False) -> List[Union[Artist, ArtistModel]]:
        """Listar artistas por tipo"""
        query = self.db.query(ArtistModel)
        if include_relations:
            query = query.options(
                joinedload(ArtistModel.profile),
                joinedload(ArtistModel.artist_type)
            )
        db_artists = query.filter(
            ArtistModel.artist_type_id == artist_type_id
        ).offset(skip).limit(limit).all()
        
        # Se include_relations=True, retornar os modelos do banco diretamente
        if include_relations:
            return db_artists
        else:
            return [self._to_entity(db_artist) for db_artist in db_artists]

    def update(self, artist: Artist) -> Artist:
        """Atualizar artista"""
        db_artist = self.db.query(ArtistModel).filter(ArtistModel.id == artist.id).first()
        if not db_artist:
            raise ValueError("Artista não encontrado")
        
        db_artist.profile_id = artist.profile_id
        db_artist.artist_type_id = artist.artist_type_id
        db_artist.dias_apresentacao = json.dumps(artist.dias_apresentacao)
        db_artist.raio_atuacao = artist.raio_atuacao
        db_artist.duracao_apresentacao = artist.duracao_apresentacao
        db_artist.valor_hora = artist.valor_hora
        db_artist.valor_couvert = artist.valor_couvert
        db_artist.requisitos_minimos = artist.requisitos_minimos
        db_artist.instagram = artist.instagram
        db_artist.tiktok = artist.tiktok
        db_artist.youtube = artist.youtube
        db_artist.facebook = artist.facebook
        db_artist.soundcloud = artist.soundcloud
        db_artist.bandcamp = artist.bandcamp
        db_artist.spotify = artist.spotify
        db_artist.deezer = artist.deezer
        
        self.db.commit()
        self.db.refresh(db_artist)
        
        return self._to_entity(db_artist)

    def delete(self, artist_id: int) -> bool:
        """Deletar artista"""
        db_artist = self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).first()
        if not db_artist:
            return False
        
        self.db.delete(db_artist)
        self.db.commit()
        return True

    def _to_entity(self, db_artist: ArtistModel) -> Artist:
        """Converter modelo do banco para entidade de domínio"""
        return Artist(
            id=db_artist.id,
            profile_id=db_artist.profile_id,
            artist_type_id=db_artist.artist_type_id,
            dias_apresentacao=json.loads(db_artist.dias_apresentacao),
            raio_atuacao=db_artist.raio_atuacao,
            duracao_apresentacao=db_artist.duracao_apresentacao,
            valor_hora=db_artist.valor_hora,
            valor_couvert=db_artist.valor_couvert,
            requisitos_minimos=db_artist.requisitos_minimos,
            instagram=db_artist.instagram,
            tiktok=db_artist.tiktok,
            youtube=db_artist.youtube,
            facebook=db_artist.facebook,
            soundcloud=db_artist.soundcloud,
            bandcamp=db_artist.bandcamp,
            spotify=db_artist.spotify,
            deezer=db_artist.deezer,
            created_at=db_artist.created_at,
            updated_at=db_artist.updated_at
        ) 