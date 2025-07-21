#!/usr/bin/env python3
"""
Script para migração de SQLite para PostgreSQL
"""
import os
import sys
from sqlalchemy import create_engine, text
from infrastructure.database.database import Base
from infrastructure.database.models.user_model import UserModel
from infrastructure.database.models.role_model import RoleModel
from infrastructure.database.models.profile_model import ProfileModel
from infrastructure.database.models.artist_type_model import ArtistTypeModel
from infrastructure.database.models.musical_style_model import MusicalStyleModel
from infrastructure.database.models.artist_model import ArtistModel

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
            # Migrar roles
            result = sqlite_conn.execute(text("SELECT * FROM roles"))
            roles = result.fetchall()
            if roles:
                print(f"📊 Encontrados {len(roles)} roles para migrar")
                with postgres_engine.connect() as postgres_conn:
                    for role in roles:
                        insert_query = text("""
                            INSERT INTO roles (id, name, description, created_at, updated_at)
                            VALUES (:id, :name, :description, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        postgres_conn.execute(insert_query, {
                            'id': role[0], 'name': role[1], 'description': role[2],
                            'created_at': role[3], 'updated_at': role[4]
                        })
                    postgres_conn.commit()
                    print("✅ Roles migrados com sucesso!")

            # Migrar artist_types
            result = sqlite_conn.execute(text("SELECT * FROM artist_types"))
            artist_types = result.fetchall()
            if artist_types:
                print(f"📊 Encontrados {len(artist_types)} tipos de artista para migrar")
                with postgres_engine.connect() as postgres_conn:
                    for artist_type in artist_types:
                        insert_query = text("""
                            INSERT INTO artist_types (id, name, description, created_at, updated_at)
                            VALUES (:id, :name, :description, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        postgres_conn.execute(insert_query, {
                            'id': artist_type[0], 'name': artist_type[1], 'description': artist_type[2],
                            'created_at': artist_type[3], 'updated_at': artist_type[4]
                        })
                    postgres_conn.commit()
                    print("✅ Tipos de artista migrados com sucesso!")

            # Migrar musical_styles
            result = sqlite_conn.execute(text("SELECT * FROM musical_styles"))
            musical_styles = result.fetchall()
            if musical_styles:
                print(f"📊 Encontrados {len(musical_styles)} estilos musicais para migrar")
                with postgres_engine.connect() as postgres_conn:
                    for musical_style in musical_styles:
                        insert_query = text("""
                            INSERT INTO musical_styles (id, name, description, created_at, updated_at)
                            VALUES (:id, :name, :description, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        postgres_conn.execute(insert_query, {
                            'id': musical_style[0], 'name': musical_style[1], 'description': musical_style[2],
                            'created_at': musical_style[3], 'updated_at': musical_style[4]
                        })
                    postgres_conn.commit()
                    print("✅ Estilos musicais migrados com sucesso!")

            # Migrar users
            result = sqlite_conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()
            if users:
                print(f"📊 Encontrados {len(users)} usuários para migrar")
                with postgres_engine.connect() as postgres_conn:
                    for user in users:
                        insert_query = text("""
                            INSERT INTO users (id, name, email, password, is_active, created_at, updated_at)
                            VALUES (:id, :name, :email, :password, :is_active, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        postgres_conn.execute(insert_query, {
                            'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3],
                            'is_active': user[4], 'created_at': user[5], 'updated_at': user[6]
                        })
                    postgres_conn.commit()
                    print("✅ Usuários migrados com sucesso!")

            # Migrar profiles
            result = sqlite_conn.execute(text("SELECT * FROM profiles"))
            profiles = result.fetchall()
            if profiles:
                print(f"📊 Encontrados {len(profiles)} perfis para migrar")
                with postgres_engine.connect() as postgres_conn:
                    for profile in profiles:
                        insert_query = text("""
                            INSERT INTO profiles (id, user_id, role_id, full_name, artistic_name, bio, cep, 
                                                logradouro, numero, complemento, cidade, uf, telefone_movel, 
                                                telefone_fixo, whatsapp, created_at, updated_at)
                            VALUES (:id, :user_id, :role_id, :full_name, :artistic_name, :bio, :cep, 
                                   :logradouro, :numero, :complemento, :cidade, :uf, :telefone_movel, 
                                   :telefone_fixo, :whatsapp, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        postgres_conn.execute(insert_query, {
                            'id': profile[0], 'user_id': profile[1], 'role_id': profile[2], 'full_name': profile[3],
                            'artistic_name': profile[4], 'bio': profile[5], 'cep': profile[6], 'logradouro': profile[7],
                            'numero': profile[8], 'complemento': profile[9], 'cidade': profile[10], 'uf': profile[11],
                            'telefone_movel': profile[12], 'telefone_fixo': profile[13], 'whatsapp': profile[14],
                            'created_at': profile[15], 'updated_at': profile[16]
                        })
                    postgres_conn.commit()
                    print("✅ Perfis migrados com sucesso!")

            # Migrar artists
            result = sqlite_conn.execute(text("SELECT * FROM artists"))
            artists = result.fetchall()
            if artists:
                print(f"📊 Encontrados {len(artists)} artistas para migrar")
                with postgres_engine.connect() as postgres_conn:
                    for artist in artists:
                        insert_query = text("""
                            INSERT INTO artists (id, profile_id, artist_type_id, dias_apresentacao, raio_atuacao,
                                               duracao_apresentacao, valor_hora, valor_couvert, requisitos_minimos,
                                               instagram, tiktok, youtube, facebook, soundcloud, bandcamp, spotify,
                                               deezer, created_at, updated_at)
                            VALUES (:id, :profile_id, :artist_type_id, :dias_apresentacao, :raio_atuacao,
                                   :duracao_apresentacao, :valor_hora, :valor_couvert, :requisitos_minimos,
                                   :instagram, :tiktok, :youtube, :facebook, :soundcloud, :bandcamp, :spotify,
                                   :deezer, :created_at, :updated_at)
                            ON CONFLICT (id) DO NOTHING
                        """)
                        postgres_conn.execute(insert_query, {
                            'id': artist[0], 'profile_id': artist[1], 'artist_type_id': artist[2],
                            'dias_apresentacao': artist[3], 'raio_atuacao': artist[4], 'duracao_apresentacao': artist[5],
                            'valor_hora': artist[6], 'valor_couvert': artist[7], 'requisitos_minimos': artist[8],
                            'instagram': artist[9], 'tiktok': artist[10], 'youtube': artist[11], 'facebook': artist[12],
                            'soundcloud': artist[13], 'bandcamp': artist[14], 'spotify': artist[15], 'deezer': artist[16],
                            'created_at': artist[17], 'updated_at': artist[18]
                        })
                    postgres_conn.commit()
                    print("✅ Artistas migrados com sucesso!")
        
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