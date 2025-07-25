"""adicionar_coluna_status_em_space_event_types

Revision ID: 131c5fdf2f57
Revises: 09931ddc1d0e
Create Date: 2025-07-24 09:47:36.305631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '131c5fdf2f57'
down_revision = '09931ddc1d0e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Para SQLite, adicionar diretamente como não nullable com valor padrão
    op.add_column('space_event_types', sa.Column('status', sa.Enum('CONTRATANDO', 'FECHADO', 'SUSPENSO', 'CANCELADO', name='statuseventtype'), nullable=False, server_default='CONTRATANDO'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('space_event_types', 'status')
    # ### end Alembic commands ### 