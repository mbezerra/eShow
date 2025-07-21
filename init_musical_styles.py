from infrastructure.database.database import SessionLocal
from infrastructure.database.models.musical_style_model import MusicalStyleModel

# Lista de estilos musicais iniciais
MUSICAL_STYLES = [
    "Arrocha",
    "Forró Estilizado", 
    "Forró Pé-de-Serra",
    "Samba",
    "Pagode",
    "Sertanejo",
    "Piseiro / Pisadinha",
    "Axé",
    "Reggae",
    "Pop/Rock",
    "MPB",
    "Voz & Violão",
    "Karaokê",
    "Flashbacks",
    "Brega",
    "Seresta",
    "Gospel Católica",
    "Gospel Evangélica"
]

def main():
    db = SessionLocal()
    for estyle in MUSICAL_STYLES:
        if not db.query(MusicalStyleModel).filter_by(estyle=estyle).first():
            db.add(MusicalStyleModel(estyle=estyle))
    db.commit()
    db.close()
    print("Estilos musicais criados com sucesso!")

if __name__ == "__main__":
    main() 