#!/usr/bin/env python3
"""
Script para popular a tabela space_types com valores iniciais
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.space_type_model import SpaceTypeModel

def init_space_types():
    """Inicializa a tabela space_types com valores padrão"""
    
    # Valores iniciais especificados
    initial_space_types = [
        "Bar",
        "Restaurante", 
        "Clube",
        "Balneário",
        "Parque Aquático",
        "Resort",
        "Embarcação",
        "Boate",
        "Salão de Baile",
        "Casa de Forró",
        "Centro de Tradições Regionais",
        "Associação Social",
        "Salão de Recepções",
        "Evento",
        "Festival"
    ]
    
    db = SessionLocal()
    try:
        # Verificar se já existem registros
        existing_count = db.query(SpaceTypeModel).count()
        if existing_count > 0:
            print(f"Tabela space_types já possui {existing_count} registros. Pulando inicialização.")
            return
        
        # Criar os registros iniciais
        for tipo in initial_space_types:
            space_type = SpaceTypeModel(tipo=tipo)
            db.add(space_type)
        
        db.commit()
        print(f"✅ {len(initial_space_types)} tipos de espaço criados com sucesso!")
        
        # Listar os tipos criados
        print("\nTipos de espaço criados:")
        for space_type in db.query(SpaceTypeModel).all():
            print(f"  - {space_type.tipo}")
            
    except Exception as e:
        print(f"❌ Erro ao criar tipos de espaço: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando tabela space_types...")
    init_space_types()
    print("✅ Concluído!") 