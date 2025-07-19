#!/usr/bin/env python3
"""
Script para migração de SQLite para PostgreSQL
"""
import os
import sys
from sqlalchemy import create_engine, text
from infrastructure.database.database import Base
from infrastructure.database.models.user_model import UserModel

def migrate_to_postgres():
    """Migrar dados de SQLite para PostgreSQL"""
    
    # Verificar se a URL do PostgreSQL está configurada
    postgres_url = os.getenv("DATABASE_URL")
    if not postgres_url or not postgres_url.startswith("postgresql"):
        print("❌ DATABASE_URL não configurada para PostgreSQL")
        print("Configure no arquivo .env:")
        print("DATABASE_URL=postgresql://user:password@localhost/eshow")
        return False
    
    try:
        # Conectar ao PostgreSQL
        print("🔗 Conectando ao PostgreSQL...")
        postgres_engine = create_engine(postgres_url)
        
        # Testar conexão
        with postgres_engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conectado ao PostgreSQL: {version}")
        
        # Criar tabelas no PostgreSQL
        print("📋 Criando tabelas no PostgreSQL...")
        Base.metadata.create_all(bind=postgres_engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Migrar dados do SQLite para PostgreSQL
        print("🔄 Migrando dados do SQLite...")
        sqlite_engine = create_engine("sqlite:///./eshow.db")
        
        with sqlite_engine.connect() as sqlite_conn:
            # Buscar dados do SQLite
            result = sqlite_conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            
            if users:
                print(f"📊 Encontrados {len(users)} usuários para migrar")
                
                # Inserir no PostgreSQL
                with postgres_engine.connect() as postgres_conn:
                    for user in users:
                        insert_query = text("""
                            INSERT INTO users (id, name, email, password, is_active, created_at, updated_at)
                            VALUES (:id, :name, :email, :password, :is_active, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        
                        postgres_conn.execute(insert_query, {
                            'id': user[0],
                            'name': user[1],
                            'email': user[2],
                            'password': user[3],
                            'is_active': user[4],
                            'created_at': user[5],
                            'updated_at': user[6]
                        })
                    
                    postgres_conn.commit()
                    print("✅ Dados migrados com sucesso!")
            else:
                print("ℹ️ Nenhum usuário encontrado para migrar")
        
        print("\n🎉 Migração concluída!")
        print("📝 Para usar PostgreSQL, certifique-se de que:")
        print("1. O PostgreSQL está instalado e rodando")
        print("2. O banco 'eshow' foi criado")
        print("3. O usuário tem permissões adequadas")
        print("4. A DATABASE_URL está configurada corretamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False

if __name__ == "__main__":
    migrate_to_postgres() 