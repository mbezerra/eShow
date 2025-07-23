#!/usr/bin/env python3
"""
Script para popular a tabela spaces com dados de exemplo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.space_model import SpaceModel
from domain.entities.space import AcessoEnum, PublicoEstimadoEnum

def init_spaces():
    """Inicializa a tabela spaces com dados de exemplo"""

    # Dados de exemplo
    sample_spaces = [
        {
            "profile_id": 1,  # Assumindo que existe um profile com ID 1
            "space_type_id": 1,  # Bar
            "event_type_id": None,
            "festival_type_id": None,
            "acesso": AcessoEnum.PUBLICO,
            "dias_apresentacao": ["sexta", "sábado"],
            "duracao_apresentacao": 3.0,
            "valor_hora": 150.0,
            "valor_couvert": 20.0,
            "requisitos_minimos": "Equipamento de som básico, microfone, instrumentos próprios",
            "oferecimentos": "Equipamento de som, iluminação, camarim, bebidas",
            "estrutura_apresentacao": "Palco de 4x3 metros, sistema de som profissional, iluminação cênica",
            "publico_estimado": PublicoEstimadoEnum.CEM_A_QUINHENTOS,
            "fotos_ambiente": ["/fotos/bar1.jpg", "/fotos/bar2.jpg"],
            "instagram": "https://instagram.com/bar_exemplo",
            "tiktok": "https://tiktok.com/@bar_exemplo",
            "youtube": None,
            "facebook": "https://facebook.com/barexemplo"
        },
        {
            "profile_id": 1,
            "space_type_id": 2,  # Restaurante
            "event_type_id": 1,  # Aniversário
            "festival_type_id": None,
            "acesso": AcessoEnum.PRIVADO,
            "dias_apresentacao": ["segunda", "terça", "quarta", "quinta", "sexta", "sábado"],
            "duracao_apresentacao": 2.0,
            "valor_hora": 200.0,
            "valor_couvert": 30.0,
            "requisitos_minimos": "Repertório variado, volume adequado para ambiente gastronômico",
            "oferecimentos": "Refeição completa, bebidas, estacionamento, segurança",
            "estrutura_apresentacao": "Área de apresentação integrada ao salão, sistema de som ambiente",
            "publico_estimado": PublicoEstimadoEnum.CINQUENTA_A_CEM,
            "fotos_ambiente": ["/fotos/restaurante1.jpg"],
            "instagram": "https://instagram.com/restaurante_exemplo",
            "tiktok": None,
            "youtube": None,
            "facebook": None
        },
        {
            "profile_id": 1,
            "space_type_id": 3,  # Clube
            "event_type_id": None,
            "festival_type_id": 7,  # Carnaval
            "acesso": AcessoEnum.PUBLICO,
            "dias_apresentacao": ["sexta", "sábado", "domingo"],
            "duracao_apresentacao": 4.0,
            "valor_hora": 300.0,
            "valor_couvert": 50.0,
            "requisitos_minimos": "Repertório animado, equipamento próprio recomendado",
            "oferecimentos": "Sistema de som profissional, iluminação, camarim, bar completo",
            "estrutura_apresentacao": "Palco grande, sistema de som de alta potência, iluminação de palco",
            "publico_estimado": PublicoEstimadoEnum.MIL_A_TRES_MIL,
            "fotos_ambiente": ["/fotos/clube1.jpg", "/fotos/clube2.jpg", "/fotos/clube3.jpg"],
            "instagram": "https://instagram.com/clube_exemplo",
            "tiktok": "https://tiktok.com/@clube_exemplo",
            "youtube": "https://youtube.com/clube_exemplo",
            "facebook": "https://facebook.com/clubeexemplo"
        }
    ]

    db = SessionLocal()
    try:
        # Verificar se já existem registros
        existing_count = db.query(SpaceModel).count()
        if existing_count > 0:
            print(f"Tabela spaces já possui {existing_count} registros. Pulando inicialização.")
            return

        # Criar os registros de exemplo
        for space_data in sample_spaces:
            space = SpaceModel(**space_data)
            db.add(space)

        db.commit()
        print(f"✅ {len(sample_spaces)} espaços de exemplo criados com sucesso!")

        # Listar os espaços criados
        print("\nEspaços criados:")
        for space in db.query(SpaceModel).all():
            print(f"  - ID {space.id}: Profile {space.profile_id}, Tipo {space.space_type_id}, Acesso: {space.acesso}")

    except Exception as e:
        print(f"❌ Erro ao criar espaços: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando tabela spaces...")
    init_spaces()
    print("✅ Concluído!") 