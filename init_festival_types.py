#!/usr/bin/env python3
"""
Script para popular a tabela festival_types com valores iniciais
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.festival_type_model import FestivalTypeModel

def init_festival_types():
    """Inicializa a tabela festival_types com valores padrão"""

    # Valores iniciais especificados
    initial_festival_types = [
        "Aniversário de Emancipação Política",
        "Festa Religiosa",
        "Alvorada",
        "Vaquejada",
        "Micareta",
        "Festa Junina",
        "Carnaval",
        "Cavalgada",
        "Festa de Vaqueiro",
        "Festa de Peão",
        "Festa de Colono",
        "Festa Anual",
        "Comemoração Cívica",
        "Parada do Orgulho LGBTQIA+"
    ]

    db = SessionLocal()
    try:
        # Verificar se já existem registros
        existing_count = db.query(FestivalTypeModel).count()
        if existing_count > 0:
            print(f"Tabela festival_types já possui {existing_count} registros. Pulando inicialização.")
            return

        # Criar os registros iniciais
        for type in initial_festival_types:
            festival_type = FestivalTypeModel(type=type)
            db.add(festival_type)

        db.commit()
        print(f"✅ {len(initial_festival_types)} tipos de festival criados com sucesso!")

        # Listar os tipos criados
        print("\nTipos de festival criados:")
        for festival_type in db.query(FestivalTypeModel).all():
            print(f"  - {festival_type.type}")

    except Exception as e:
        print(f"❌ Erro ao criar tipos de festival: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando tabela festival_types...")
    init_festival_types()
    print("✅ Concluído!") 