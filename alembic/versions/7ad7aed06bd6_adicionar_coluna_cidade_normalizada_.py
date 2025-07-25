"""Adicionar coluna cidade_normalizada para busca sem acentos

Revision ID: 7ad7aed06bd6
Revises: fa49132b1dc5
Create Date: 2025-07-24 23:39:41.653159

"""
from alembic import op
import sqlalchemy as sa
import unicodedata


# revision identifiers, used by Alembic.
revision = '7ad7aed06bd6'
down_revision = 'fa49132b1dc5'
branch_labels = None
depends_on = None


def _normalize_text(text: str) -> str:
    """Normaliza texto removendo acentos e convertendo para maiúsculas"""
    if not text:
        return ""
    # Remove acentos usando unicodedata
    normalized = unicodedata.normalize('NFD', text)
    # Remove caracteres de acentuação
    ascii_text = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    # Converte para maiúsculas e remove espaços extras
    return ascii_text.strip().upper()


def upgrade() -> None:
    # Adicionar coluna cidade_normalizada
    op.add_column('cep_coordinates', sa.Column('cidade_normalizada', sa.String(100), nullable=True))
    
    # Criar índice para a nova coluna
    op.create_index('idx_cep_coordinates_cidade_normalizada', 'cep_coordinates', ['cidade_normalizada'])
    
    # Popular a coluna cidade_normalizada com dados normalizados
    connection = op.get_bind()
    
    # Obter todos os registros
    result = connection.execute(sa.text("SELECT cidade, uf FROM cep_coordinates"))
    records = result.fetchall()
    
    # Atualizar cada registro com a cidade normalizada
    for record in records:
        cidade = record[0]
        uf = record[1]
        cidade_normalizada = _normalize_text(cidade)
        
        connection.execute(
            sa.text("UPDATE cep_coordinates SET cidade_normalizada = :cidade_normalizada WHERE cidade = :cidade AND uf = :uf"),
            {"cidade_normalizada": cidade_normalizada, "cidade": cidade, "uf": uf}
        )
    
    # Para SQLite, não podemos alterar nullable, mas podemos garantir que todos os registros tenham valores
    # A coluna permanecerá nullable=True, mas terá valores para todos os registros existentes


def downgrade() -> None:
    # Remover índice
    op.drop_index('idx_cep_coordinates_cidade_normalizada', 'cep_coordinates')
    
    # Remover coluna
    op.drop_column('cep_coordinates', 'cidade_normalizada') 