#!/usr/bin/env python3
"""
Script para inicializar a tabela space_festival_types com dados de exemplo
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import SessionLocal
from infrastructure.database.models.space_festival_type_model import SpaceFestivalTypeModel
from infrastructure.database.models.space_model import SpaceModel
from infrastructure.database.models.festival_type_model import FestivalTypeModel

def init_space_festival_types():
    """Inicializar dados de exemplo para space_festival_types"""
    db: Session = SessionLocal()
    
    try:
        # Verificar se já existem dados
        existing_count = db.query(SpaceFestivalTypeModel).count()
        if existing_count > 0:
            print(f"✅ Tabela space_festival_types já possui {existing_count} registros")
            return
        
        # Obter espaços e tipos de festivais existentes
        spaces = db.query(SpaceModel).limit(5).all()
        festival_types = db.query(FestivalTypeModel).limit(3).all()
        
        if not spaces:
            print("❌ Erro: Não há espaços cadastrados. Execute primeiro: python init_spaces.py")
            return
        
        if not festival_types:
            print("❌ Erro: Não há tipos de festivais cadastrados. Execute primeiro: python init_festival_types.py")
            return
        
        # Dados de exemplo para relacionamentos espaço-festival
        space_festival_data = [
            {
                "space_id": spaces[0].id,
                "festival_type_id": festival_types[0].id,
                "tema": "Rock Paulista dos Anos 80",
                "descricao": "Festival dedicado ao rock nacional paulista dos anos 80, com shows de bandas clássicas e cover.",
                "link_divulgacao": "https://rockpaulista80.com.br",
                "banner": "static/banners/rock_paulista_80.jpg",
                "data": datetime(2024, 7, 15, 20, 0),
                "horario": "20:00-02:00"
            },
            {
                "space_id": spaces[0].id,
                "festival_type_id": festival_types[1].id,
                "tema": "Blues & Jazz Night",
                "descricao": "Noite especial com apresentações de blues e jazz, drinks especiais e ambiente intimista.",
                "link_divulgacao": "https://bluesjazznight.com",
                "banner": "static/banners/blues_jazz_night.jpg",
                "data": datetime(2024, 8, 20, 19, 0),
                "horario": "19:00-01:00"
            },
            {
                "space_id": spaces[0].id,
                "festival_type_id": festival_types[2].id if len(festival_types) > 2 else festival_types[0].id,
                "tema": "Eletrônica Underground",
                "descricao": "Festival de música eletrônica underground com DJs nacionais e internacionais.",
                "link_divulgacao": "https://eletronica-underground.net",
                "banner": "static/banners/eletronica_underground.jpg",
                "data": datetime(2024, 9, 5, 22, 0),
                "horario": "22:00-06:00"
            },
            {
                "space_id": spaces[1].id if len(spaces) > 1 else spaces[0].id,
                "festival_type_id": festival_types[0].id,
                "tema": "Samba de Raiz Carioca",
                "descricao": "Festival de samba tradicional carioca com roda de samba e apresentações especiais.",
                "link_divulgacao": "https://sambaderaiz.rio",
                "banner": "static/banners/samba_raiz_carioca.jpg",
                "data": datetime(2024, 10, 12, 18, 0),
                "horario": "18:00-00:00"
            },
            {
                "space_id": spaces[1].id if len(spaces) > 1 else spaces[0].id,
                "festival_type_id": festival_types[1].id,
                "tema": "MPB Contemporânea",
                "descricao": "Festival de MPB contemporânea com artistas emergentes e consagrados da música popular brasileira.",
                "link_divulgacao": "https://mpbcontemporanea.com.br",
                "banner": "static/banners/mpb_contemporanea.jpg",
                "data": datetime(2024, 11, 8, 20, 30),
                "horario": "20:30-01:30"
            },
            {
                "space_id": spaces[2].id if len(spaces) > 2 else spaces[0].id,
                "festival_type_id": festival_types[2].id if len(festival_types) > 2 else festival_types[0].id,
                "tema": "Reggae & World Music",
                "descricao": "Festival multicultural com reggae, world music e fusões de ritmos globais.",
                "link_divulgacao": "https://reggaeworldmusic.com",
                "banner": "static/banners/reggae_world_music.jpg",
                "data": datetime(2024, 12, 20, 19, 30),
                "horario": "19:30-02:00"
            },
            {
                "space_id": spaces[2].id if len(spaces) > 2 else spaces[0].id,
                "festival_type_id": festival_types[0].id,
                "tema": "Indie Rock Festival",
                "descricao": "Festival de rock independente com bandas emergentes e alternativas do cenário nacional.",
                "link_divulgacao": "https://indierockfest.com.br",
                "banner": "static/banners/indie_rock_festival.jpg",
                "data": datetime(2025, 1, 25, 21, 0),
                "horario": "21:00-03:00"
            },
            {
                "space_id": spaces[3].id if len(spaces) > 3 else spaces[0].id,
                "festival_type_id": festival_types[1].id,
                "tema": "Bossa Nova Experience",
                "descricao": "Experiência única de bossa nova com músicos renomados em ambiente sofisticado.",
                "link_divulgacao": "https://bossanovaexp.com",
                "banner": "static/banners/bossa_nova_experience.jpg",
                "data": datetime(2025, 2, 14, 20, 0),
                "horario": "20:00-01:00"
            },
            {
                "space_id": spaces[3].id if len(spaces) > 3 else spaces[0].id,
                "festival_type_id": festival_types[2].id if len(festival_types) > 2 else festival_types[1].id,
                "tema": "Forró Universitário",
                "descricao": "Festival de forró universitário com bandas jovens e muita animação para dançar.",
                "link_divulgacao": "https://forrouniversitario.com.br",
                "banner": "static/banners/forro_universitario.jpg",
                "data": datetime(2025, 3, 22, 19, 0),
                "horario": "19:00-02:00"
            },
            {
                "space_id": spaces[4].id if len(spaces) > 4 else spaces[0].id,
                "festival_type_id": festival_types[0].id,
                "tema": "Metal Extremo Brasil",
                "descricao": "Festival de metal extremo com bandas nacionais de death, black e thrash metal.",
                "link_divulgacao": "https://metalextremobrasil.com",
                "banner": "static/banners/metal_extremo_brasil.jpg",
                "data": datetime(2025, 4, 10, 21, 30),
                "horario": "21:30-04:00"
            }
        ]
        
        # Criar os relacionamentos
        space_festival_types = []
        for data in space_festival_data:
            space_festival_type = SpaceFestivalTypeModel(**data)
            space_festival_types.append(space_festival_type)
        
        # Adicionar todos de uma vez
        db.add_all(space_festival_types)
        db.commit()
        
        print(f"✅ Inseridos {len(space_festival_types)} relacionamentos space_festival_types com sucesso!")
        
        # Mostrar alguns exemplos inseridos
        print("\n📋 EXEMPLOS DE RELACIONAMENTOS CRIADOS:")
        for i, space_festival_type in enumerate(space_festival_types[:3], 1):
            space_name = db.query(SpaceModel).filter(SpaceModel.id == space_festival_type.space_id).first().name
            festival_type_name = db.query(FestivalTypeModel).filter(FestivalTypeModel.id == space_festival_type.festival_type_id).first().name
            print(f"   {i}. {space_name} - {festival_type_name}: {space_festival_type.tema}")
        
        if len(space_festival_types) > 3:
            print(f"   ... e mais {len(space_festival_types) - 3} relacionamentos!")
            
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        db.rollback()
        raise
        
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando dados da tabela space_festival_types...")
    init_space_festival_types()
    print("✅ Script concluído!") 