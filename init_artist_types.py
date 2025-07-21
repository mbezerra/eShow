from infrastructure.database.database import SessionLocal
from infrastructure.database.models.artist_type_model import ArtistTypeModel
from domain.entities.artist_type import ArtistTypeEnum

def main():
    db = SessionLocal()
    for tipo in ArtistTypeEnum:
        if not db.query(ArtistTypeModel).filter_by(tipo=tipo).first():
            db.add(ArtistTypeModel(tipo=tipo))
    db.commit()
    db.close()

if __name__ == "__main__":
    main() 