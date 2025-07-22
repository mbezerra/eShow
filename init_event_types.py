#!/usr/bin/env python3
"""
Script para popular a tabela event_types com valores iniciais
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from infrastructure.database.database import SessionLocal
from infrastructure.database.models.event_type_model import EventTypeModel

def init_event_types():
    """Inicializa a tabela event_types com valores padrão"""
    
    # Valores iniciais especificados
    initial_event_types = [
        "Aniversário",
        "Casamento", 
        "Formatura",
        "Inauguração",
        "Lançamento",
        "Casual",
        "Recorrente"
    ]
    
    db = SessionLocal()
    try:
        # Verificar se já existem registros
        existing_count = db.query(EventTypeModel).count()
        if existing_count > 0:
            print(f"Tabela event_types já possui {existing_count} registros. Pulando inicialização.")
            return
        
        # Criar os registros iniciais
        for type in initial_event_types:
            event_type = EventTypeModel(type=type)
            db.add(event_type)
        
        db.commit()
        print(f"✅ {len(initial_event_types)} tipos de evento criados com sucesso!")
        
        # Listar os tipos criados
        print("\nTipos de evento criados:")
        for event_type in db.query(EventTypeModel).all():
            print(f"  - {event_type.type}")
            
    except Exception as e:
        print(f"❌ Erro ao criar tipos de evento: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando tabela event_types...")
    init_event_types()
    print("✅ Concluído!") 