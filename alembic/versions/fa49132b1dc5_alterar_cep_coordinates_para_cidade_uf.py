"""
Migração para alterar a tabela cep_coordinates: remover as colunas cep, logradouro, bairro, e tornar (cidade, uf) a chave primária composta. Manter latitude, longitude, cidade, uf, created_at, updated_at.

Revision ID: fa49132b1dc5
Revises: 0f9228074c43
Create Date: 2025-07-24 23:19:47.711268
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fa49132b1dc5'
down_revision = '0f9228074c43'
branch_labels = None
depends_on = None

def upgrade():
    # Para SQLite, precisamos recriar a tabela para alterar a chave primária
    # Primeiro, criar uma tabela temporária com a nova estrutura
    op.create_table('cep_coordinates_new',
        sa.Column('cidade', sa.String(length=100), nullable=False),
        sa.Column('uf', sa.String(length=2), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(DATETIME(\'now\'))')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('cidade', 'uf', name='pk_cep_coordinates_cidade_uf')
    )
    
    # Copiar dados existentes (se houver)
    op.execute("""
        INSERT INTO cep_coordinates_new (cidade, uf, latitude, longitude, created_at, updated_at)
        SELECT DISTINCT cidade, uf, latitude, longitude, created_at, updated_at
        FROM cep_coordinates
        WHERE cidade IS NOT NULL AND uf IS NOT NULL
    """)
    
    # Remover tabela antiga
    op.drop_table('cep_coordinates')
    
    # Renomear nova tabela
    op.rename_table('cep_coordinates_new', 'cep_coordinates')
    
    # Criar índices
    op.create_index('idx_cep_coordinates_lat_lng', 'cep_coordinates', ['latitude', 'longitude'])

def downgrade():
    # Recriar tabela com estrutura original
    op.create_table('cep_coordinates_old',
        sa.Column('cep', sa.String(length=9), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('cidade', sa.String(length=100), nullable=True),
        sa.Column('uf', sa.String(length=2), nullable=True),
        sa.Column('logradouro', sa.String(length=200), nullable=True),
        sa.Column('bairro', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(DATETIME(\'now\'))')),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('cep', name='pk_cep_coordinates_cep')
    )
    
    # Copiar dados de volta (com CEPs gerados baseados em cidade/uf)
    op.execute("""
        INSERT INTO cep_coordinates_old (cep, cidade, uf, latitude, longitude, created_at, updated_at)
        SELECT 
            SUBSTR(cidade, 1, 5) || '-' || SUBSTR(uf, 1, 3) as cep,
            cidade, uf, latitude, longitude, created_at, updated_at
        FROM cep_coordinates
    """)
    
    # Remover tabela nova
    op.drop_table('cep_coordinates')
    
    # Renomear tabela antiga
    op.rename_table('cep_coordinates_old', 'cep_coordinates')
    
    # Recriar índices originais
    op.create_index('idx_cep_coordinates_cidade_uf', 'cep_coordinates', ['cidade', 'uf'])
    op.create_index('idx_cep_coordinates_lat_lng', 'cep_coordinates', ['latitude', 'longitude']) 