#!/usr/bin/env python3
"""
Script para criar um usuário de teste
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.database import get_database_session
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from domain.entities.user import User
from app.core.security import get_password_hash

def create_test_user():
    """Criar um usuário de teste"""
    print("🔧 Criando usuário de teste...")
    
    # Obter sessão do banco
    session = next(get_database_session())
    user_repo = UserRepositoryImpl(session)
    
    try:
        # Verificar se o usuário já existe
        existing_user = user_repo.get_by_email("test@eshow.com")
        if existing_user:
            print(f"   ⚠️  Usuário já existe: {existing_user.email}")
            return
        
        # Criar usuário de teste
        test_user = User(
            name="Usuário Teste",
            email="test@eshow.com",
            password=get_password_hash("test123"),
            is_active=True
        )
        
        created_user = user_repo.create(test_user)
        print(f"   ✅ Usuário criado com sucesso: {created_user.email}")
        print(f"      - ID: {created_user.id}")
        print(f"      - Nome: {created_user.name}")
        print(f"      - Senha: test123")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    create_test_user() 