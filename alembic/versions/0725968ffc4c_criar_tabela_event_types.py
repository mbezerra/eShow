"""criar_tabela_event_types

Revision ID: 0725968ffc4c
Revises: 3c41237bb0cf
Create Date: 2025-07-22 17:51:47.028799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0725968ffc4c'
down_revision = '3c41237bb0cf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_types_id'), 'event_types', ['id'], unique=False)
    op.create_index(op.f('ix_event_types_type'), 'event_types', ['type'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_event_types_type'), table_name='event_types')
    op.drop_index(op.f('ix_event_types_id'), table_name='event_types')
    op.drop_table('event_types')
    # ### end Alembic commands ### 