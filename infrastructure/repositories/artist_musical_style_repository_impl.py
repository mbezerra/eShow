from typing import List, Optional
from sqlalchemy.orm import Session
from domain.repositories.artist_musical_style_repository import ArtistMusicalStyleRepository
from domain.entities.artist_musical_style import ArtistMusicalStyle
from infrastructure.database.models.artist_musical_style_model import ArtistMusicalStyleModel
from infrastructure.database.models.artist_model import ArtistModel
from infrastructure.database.models.musical_style_model import MusicalStyleModel

class ArtistMusicalStyleRepositoryImpl(ArtistMusicalStyleRepository):
    """Implementação do repositório para o relacionamento N:N entre Artists e Musical Styles"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, artist_musical_style: ArtistMusicalStyle) -> ArtistMusicalStyle:
        """Criar um novo relacionamento entre artista e estilo musical"""
        # Verificar se o artista existe
        artist = self.db.query(ArtistModel).filter(ArtistModel.id == artist_musical_style.artist_id).first()
        if not artist:
            raise ValueError(f"Artista com ID {artist_musical_style.artist_id} não encontrado")
        
        # Verificar se o estilo musical existe
        musical_style = self.db.query(MusicalStyleModel).filter(MusicalStyleModel.id == artist_musical_style.musical_style_id).first()
        if not musical_style:
            raise ValueError(f"Estilo musical com ID {artist_musical_style.musical_style_id} não encontrado")
        
        # Verificar se o relacionamento já existe
        existing = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_musical_style.artist_id,
            ArtistMusicalStyleModel.musical_style_id == artist_musical_style.musical_style_id
        ).first()
        
        if existing:
            raise ValueError(f"Relacionamento entre artista {artist_musical_style.artist_id} e estilo musical {artist_musical_style.musical_style_id} já existe")
        
        # Criar o relacionamento
        db_artist_musical_style = ArtistMusicalStyleModel(
            artist_id=artist_musical_style.artist_id,
            musical_style_id=artist_musical_style.musical_style_id
        )
        
        self.db.add(db_artist_musical_style)
        self.db.commit()
        self.db.refresh(db_artist_musical_style)
        
        return ArtistMusicalStyle(
            artist_id=db_artist_musical_style.artist_id,
            musical_style_id=db_artist_musical_style.musical_style_id,
            created_at=db_artist_musical_style.created_at
        )
    
    def create_bulk(self, artist_id: int, musical_style_ids: List[int]) -> List[ArtistMusicalStyle]:
        """Criar múltiplos relacionamentos para um artista"""
        # Verificar se o artista existe
        artist = self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).first()
        if not artist:
            raise ValueError(f"Artista com ID {artist_id} não encontrado")
        
        # Verificar se todos os estilos musicais existem
        musical_styles = self.db.query(MusicalStyleModel).filter(MusicalStyleModel.id.in_(musical_style_ids)).all()
        if len(musical_styles) != len(musical_style_ids):
            existing_ids = [style.id for style in musical_styles]
            missing_ids = [style_id for style_id in musical_style_ids if style_id not in existing_ids]
            raise ValueError(f"Estilos musicais não encontrados: {missing_ids}")
        
        # Verificar relacionamentos existentes
        existing = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_id,
            ArtistMusicalStyleModel.musical_style_id.in_(musical_style_ids)
        ).all()
        
        if existing:
            existing_style_ids = [rel.musical_style_id for rel in existing]
            raise ValueError(f"Relacionamentos já existem para os estilos: {existing_style_ids}")
        
        # Criar os relacionamentos
        created_relationships = []
        for style_id in musical_style_ids:
            db_relationship = ArtistMusicalStyleModel(
                artist_id=artist_id,
                musical_style_id=style_id
            )
            self.db.add(db_relationship)
            created_relationships.append(db_relationship)
        
        self.db.commit()
        
        # Retornar as entidades criadas
        return [
            ArtistMusicalStyle(
                artist_id=rel.artist_id,
                musical_style_id=rel.musical_style_id,
                created_at=rel.created_at
            )
            for rel in created_relationships
        ]
    
    def get_by_artist_id(self, artist_id: int) -> List[ArtistMusicalStyle]:
        """Obter todos os estilos musicais de um artista"""
        relationships = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_id
        ).all()
        
        return [
            ArtistMusicalStyle(
                artist_id=rel.artist_id,
                musical_style_id=rel.musical_style_id,
                created_at=rel.created_at
            )
            for rel in relationships
        ]
    
    def get_by_musical_style_id(self, musical_style_id: int) -> List[ArtistMusicalStyle]:
        """Obter todos os artistas de um estilo musical"""
        relationships = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.musical_style_id == musical_style_id
        ).all()
        
        return [
            ArtistMusicalStyle(
                artist_id=rel.artist_id,
                musical_style_id=rel.musical_style_id,
                created_at=rel.created_at
            )
            for rel in relationships
        ]
    
    def get_by_artist_and_style(self, artist_id: int, musical_style_id: int) -> Optional[ArtistMusicalStyle]:
        """Obter um relacionamento específico"""
        relationship = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_id,
            ArtistMusicalStyleModel.musical_style_id == musical_style_id
        ).first()
        
        if not relationship:
            return None
        
        return ArtistMusicalStyle(
            artist_id=relationship.artist_id,
            musical_style_id=relationship.musical_style_id,
            created_at=relationship.created_at
        )
    
    def delete(self, artist_id: int, musical_style_id: int) -> bool:
        """Deletar um relacionamento específico"""
        relationship = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_id,
            ArtistMusicalStyleModel.musical_style_id == musical_style_id
        ).first()
        
        if not relationship:
            return False
        
        self.db.delete(relationship)
        self.db.commit()
        return True
    
    def delete_by_artist_id(self, artist_id: int) -> bool:
        """Deletar todos os relacionamentos de um artista"""
        relationships = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_id
        ).all()
        
        if not relationships:
            return False
        
        for relationship in relationships:
            self.db.delete(relationship)
        
        self.db.commit()
        return True
    
    def delete_by_musical_style_id(self, musical_style_id: int) -> bool:
        """Deletar todos os relacionamentos de um estilo musical"""
        relationships = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.musical_style_id == musical_style_id
        ).all()
        
        if not relationships:
            return False
        
        for relationship in relationships:
            self.db.delete(relationship)
        
        self.db.commit()
        return True
    
    def update_artist_styles(self, artist_id: int, musical_style_ids: List[int]) -> List[ArtistMusicalStyle]:
        """Atualizar todos os estilos musicais de um artista (substituir os existentes)"""
        # Verificar se o artista existe
        artist = self.db.query(ArtistModel).filter(ArtistModel.id == artist_id).first()
        if not artist:
            raise ValueError(f"Artista com ID {artist_id} não encontrado")
        
        # Verificar se todos os estilos musicais existem
        musical_styles = self.db.query(MusicalStyleModel).filter(MusicalStyleModel.id.in_(musical_style_ids)).all()
        if len(musical_styles) != len(musical_style_ids):
            existing_ids = [style.id for style in musical_styles]
            missing_ids = [style_id for style_id in musical_style_ids if style_id not in existing_ids]
            raise ValueError(f"Estilos musicais não encontrados: {missing_ids}")
        
        # Deletar relacionamentos existentes
        existing_relationships = self.db.query(ArtistMusicalStyleModel).filter(
            ArtistMusicalStyleModel.artist_id == artist_id
        ).all()
        
        for relationship in existing_relationships:
            self.db.delete(relationship)
        
        # Criar novos relacionamentos
        created_relationships = []
        for style_id in musical_style_ids:
            db_relationship = ArtistMusicalStyleModel(
                artist_id=artist_id,
                musical_style_id=style_id
            )
            self.db.add(db_relationship)
            created_relationships.append(db_relationship)
        
        self.db.commit()
        
        # Retornar as entidades criadas
        return [
            ArtistMusicalStyle(
                artist_id=rel.artist_id,
                musical_style_id=rel.musical_style_id,
                created_at=rel.created_at
            )
            for rel in created_relationships
        ] 