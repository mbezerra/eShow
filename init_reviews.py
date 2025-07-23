#!/usr/bin/env python3
"""
Script para inicializar dados de exemplo de reviews
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models.review_model import ReviewModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.space_event_type_model import SpaceEventTypeModel
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel
from infrastructure.database.database import Base

def init_reviews_data():
    """Inicializar dados de exemplo de reviews"""
    
    # Configurar banco de dados
    database_url = os.getenv("DATABASE_URL", "sqlite:///./eShow.db")
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    with SessionLocal() as db:
        try:
            # Verificar se já existem reviews
            existing_reviews = db.query(ReviewModel).first()
            if existing_reviews:
                print("Reviews já existem no banco de dados. Pulando inicialização...")
                return
            
            # Obter profiles, space_event_types e space_festival_types existentes
            profiles = db.query(ProfileModel).all()
            space_event_types = db.query(SpaceEventTypeModel).all()
            space_festival_types = db.query(SpaceFestivalTypeModel).all()
            
            if not profiles:
                print("Nenhum profile encontrado. Execute init_profiles.py primeiro.")
                return
            
            if not space_event_types and not space_festival_types:
                print("Nenhum space-event-type ou space-festival-type encontrado.")
                print("Execute init_space_event_types.py e init_space_festival_types.py primeiro.")
                return
            
            # Dados de exemplo de reviews
            reviews_data = []
            base_date = datetime.now() - timedelta(days=30)
            
            # Reviews simples para diferentes profiles com space_event_types
            if space_event_types and len(profiles) >= 3:
                reviews_data.extend([
                    {
                        "profile_id": profiles[0].id,
                        "space_event_type_id": space_event_types[0].id,
                        "data_hora": base_date + timedelta(days=1),
                        "nota": 5,
                        "depoimento": f"Excelente apresentação do {profiles[0].artistic_name}. Muito profissional e pontual."
                    },
                    {
                        "profile_id": profiles[1].id,
                        "space_event_type_id": space_event_types[0].id,
                        "data_hora": base_date + timedelta(days=5),
                        "nota": 4,
                        "depoimento": f"Ótima apresentação do {profiles[1].artistic_name}. Recomendo!"
                    }
                ])
            
            # Reviews simples para diferentes profiles com space_festival_types  
            if space_festival_types and len(profiles) >= 3:
                reviews_data.extend([
                    {
                        "profile_id": profiles[2].id,
                        "space_festival_type_id": space_festival_types[0].id,
                        "data_hora": base_date + timedelta(days=10),
                        "nota": 3,
                        "depoimento": f"Boa participação do {profiles[2].artistic_name} no festival."
                    }
                ])
            
            # Reviews adicionais com diferentes notas
            if len(profiles) >= 4:
                additional_reviews = [
                    {
                        "profile_id": profiles[0].id,
                        "space_event_type_id": space_event_types[0].id if space_event_types else None,
                        "data_hora": datetime.now() - timedelta(days=5),
                        "nota": 5,
                        "depoimento": "Apresentação impecável! Superou todas as expectativas. O público ficou encantado com a performance."
                    },
                    {
                        "profile_id": profiles[1].id,
                        "space_festival_type_id": space_festival_types[0].id if space_festival_types else None,
                        "data_hora": datetime.now() - timedelta(days=3),
                        "nota": 2,
                        "depoimento": "Infelizmente não foi o que esperávamos. Chegou atrasado e a apresentação não correspondeu ao combinado."
                    },
                    {
                        "profile_id": profiles[2].id,
                        "space_event_type_id": space_event_types[0].id if space_event_types else None,
                        "data_hora": datetime.now() - timedelta(days=1),
                        "nota": 4,
                        "depoimento": "Muito bom! Apresentação sólida e profissional. Pequenos ajustes poderiam tornar ainda melhor."
                    }
                ]
                
                # Filtrar reviews adicionais que tenham relacionamentos válidos
                for review_data in additional_reviews:
                    if review_data.get("space_event_type_id") or review_data.get("space_festival_type_id"):
                        reviews_data.append(review_data)
            
            # Criar reviews no banco
            created_count = 0
            for review_data in reviews_data:
                # Verificar se tem pelo menos um relacionamento
                if not review_data.get("space_event_type_id") and not review_data.get("space_festival_type_id"):
                    continue
                
                review = ReviewModel(
                    profile_id=review_data["profile_id"],
                    space_event_type_id=review_data.get("space_event_type_id"),
                    space_festival_type_id=review_data.get("space_festival_type_id"),
                    data_hora=review_data["data_hora"],
                    nota=review_data["nota"],
                    depoimento=review_data["depoimento"]
                )
                
                db.add(review)
                created_count += 1
            
            db.commit()
            print(f"✅ {created_count} reviews criados com sucesso!")
            
            # Mostrar estatísticas
            total_reviews = db.query(ReviewModel).count()
            print(f"📊 Total de reviews no banco: {total_reviews}")
            
            # Mostrar distribuição por nota
            for nota in range(1, 6):
                count = db.query(ReviewModel).filter(ReviewModel.nota == nota).count()
                print(f"   {nota} estrelas: {count} reviews")
                
        except Exception as e:
            print(f"❌ Erro ao criar reviews: {e}")
            db.rollback()

if __name__ == "__main__":
    print("🚀 Inicializando dados de reviews...")
    init_reviews_data()
    print("✨ Processo concluído!") 