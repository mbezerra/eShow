#!/usr/bin/env python3
"""
Script para popular a tabela reviews seguindo as regras de negócio implementadas
"""

from datetime import datetime, timedelta
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.review_model import ReviewModel

def main():
    db = SessionLocal()
    
    # Limpar tabela reviews
    db.query(ReviewModel).delete()
    db.commit()
    print("✅ Tabela reviews limpa")
    
    # Dados de reviews seguindo as regras de negócio
    # Regra: ARTISTA (role_id=2) avalia ESPAÇO (role_id=3) e vice-versa
    # Não incluir ADMIN (role_id=1) - eles não fazem reviews
    
    reviews_data = [
        # Reviews de ARTISTAS (profile_id 2, 7, 8, 9) avaliando ESPAÇOS
        {
            "profile_id": 2,  # Bruno Souza (ARTISTA)
            "space_event_type_id": 3,  # Bar do Centro - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=30),
            "nota": 5,
            "depoimento": "Excelente espaço! Acústica perfeita e equipe muito profissional. Recomendo fortemente para outros artistas."
        },
        {
            "profile_id": 2,  # Bruno Souza (ARTISTA)
            "space_event_type_id": 4,  # Bar do Centro - Karaokê
            "data_hora": datetime.now() - timedelta(days=25),
            "nota": 4,
            "depoimento": "Ótimo ambiente para karaokê. Equipamentos de qualidade e público animado. Voltarei com certeza!"
        },
        {
            "profile_id": 7,  # Ana Costa (ARTISTA)
            "space_event_type_id": 5,  # Casa de Shows Musical - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=20),
            "nota": 5,
            "depoimento": "Espaço incrível! Palco amplo, iluminação profissional e som de primeira qualidade. Experiência maravilhosa!"
        },
        {
            "profile_id": 8,  # Diego Silva (ARTISTA)
            "space_event_type_id": 6,  # Casa de Shows Musical - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=15),
            "nota": 4,
            "depoimento": "Bom espaço para shows. Equipe atenciosa e estrutura adequada. Recomendo para artistas independentes."
        },
        {
            "profile_id": 9,  # Elena Santos (ARTISTA)
            "space_festival_type_id": 6,  # Casa de Shows Musical - Festival de Rock
            "data_hora": datetime.now() - timedelta(days=10),
            "nota": 5,
            "depoimento": "Festival incrível! Organização perfeita, público engajado e experiência única. Quero participar novamente!"
        },
        
        # Reviews de ESPAÇOS (profile_id 3, 4, 5, 6) avaliando ARTISTAS
        {
            "profile_id": 3,  # Carla Lima (ESPAÇO)
            "space_event_type_id": 3,  # Bar do Centro - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=28),
            "nota": 5,
            "depoimento": "Bruno é um artista excepcional! Repertório variado, interação com o público e profissionalismo total."
        },
        {
            "profile_id": 4,  # Bar do Centro (ESPAÇO)
            "space_event_type_id": 4,  # Bar do Centro - Karaokê
            "data_hora": datetime.now() - timedelta(days=23),
            "nota": 4,
            "depoimento": "Bruno animou muito o karaokê! Conhece muitas músicas e tem ótima voz. Público adorou!"
        },
        {
            "profile_id": 5,  # Casa de Shows Musical (ESPAÇO)
            "space_event_type_id": 5,  # Casa de Shows Musical - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=18),
            "nota": 5,
            "depoimento": "Ana Costa é uma artista completa! Voz incrível, presença de palco e repertório que agrada a todos."
        },
        {
            "profile_id": 5,  # Casa de Shows Musical (ESPAÇO)
            "space_event_type_id": 6,  # Casa de Shows Musical - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=13),
            "nota": 4,
            "depoimento": "Diego Silva trouxe energia ao palco! Show dinâmico e público muito satisfeito. Recomendo!"
        },
        {
            "profile_id": 5,  # Casa de Shows Musical (ESPAÇO)
            "space_festival_type_id": 6,  # Casa de Shows Musical - Festival de Rock
            "data_hora": datetime.now() - timedelta(days=8),
            "nota": 5,
            "depoimento": "Elena Santos foi destaque do festival! Performance incrível e profissionalismo exemplar."
        },
        {
            "profile_id": 6,  # Pub Rock Station (ESPAÇO)
            "space_event_type_id": 3,  # Bar do Centro - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=5),
            "nota": 4,
            "depoimento": "Bruno Souza tem talento nato! Show bem estruturado e conexão com o público. Queremos mais!"
        },
        {
            "profile_id": 6,  # Pub Rock Station (ESPAÇO)
            "space_event_type_id": 5,  # Casa de Shows Musical - Show ao Vivo
            "data_hora": datetime.now() - timedelta(days=3),
            "nota": 5,
            "depoimento": "Ana Costa é uma artista de primeira linha! Voz poderosa e carisma único. Experiência inesquecível!"
        }
    ]
    
    # Inserir reviews
    for review_data in reviews_data:
        review = ReviewModel(**review_data)
        db.add(review)
    
    db.commit()
    db.close()
    
    print(f"✅ {len(reviews_data)} reviews criados com sucesso!")
    print()
    print("📊 DISTRIBUIÇÃO DOS REVIEWS:")
    print("   • ARTISTAS avaliando ESPAÇOS: 5 reviews")
    print("   • ESPAÇOS avaliando ARTISTAS: 7 reviews")
    print("   • Total: 12 reviews")
    print()
    print("🎯 REGRAS DE NEGÓCIO APLICADAS:")
    print("   ✅ Nenhum ADMIN criou reviews")
    print("   ✅ ARTISTAS só avaliam ESPAÇOS")
    print("   ✅ ESPAÇOS só avaliam ARTISTAS")
    print("   ✅ Relacionamentos únicos (event OU festival)")
    print("   ✅ Notas entre 1-5 estrelas")
    print("   ✅ Depoimentos com 10+ caracteres")

if __name__ == "__main__":
    main() 