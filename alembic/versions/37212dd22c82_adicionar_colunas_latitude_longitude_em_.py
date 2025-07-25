"""adicionar_colunas_latitude_longitude_em_profiles

Revision ID: 37212dd22c82
Revises: 7ad7aed06bd6
Create Date: 2025-07-25 16:31:00.234935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37212dd22c82'
down_revision = '7ad7aed06bd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Adicionar colunas latitude e longitude na tabela profiles
    op.add_column('profiles', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('profiles', sa.Column('longitude', sa.Float(), nullable=True))


def downgrade() -> None:
    # Remover colunas latitude e longitude da tabela profiles
    op.drop_column('profiles', 'longitude')
    op.drop_column('profiles', 'latitude') 