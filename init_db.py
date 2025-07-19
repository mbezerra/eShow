#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
"""
from infrastructure.database.database import engine, Base
from infrastructure.database.models.user_model import UserModel

def init_database():
    """Criar todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_database() 