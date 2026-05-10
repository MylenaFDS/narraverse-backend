"""update map regions

Revision ID: 02a508ab3b30
Revises: 5fb8867f22e2
Create Date: 2026-05-10 00:28:16.698925

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '02a508ab3b30'
down_revision: Union[str, Sequence[str], None] = '5fb8867f22e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'rpg_map_regions',

        sa.Column('id', sa.Integer(), primary_key=True),

        sa.Column(
            'rpg_id',
            sa.Integer(),
            sa.ForeignKey('rpgs.id'),
            nullable=False
        ),

        sa.Column(
            'lore_id',
            sa.Integer(),
            sa.ForeignKey('rpg_lore.id'),
            nullable=True
        ),

        sa.Column('name', sa.String(length=100), nullable=False),

        sa.Column('pos_x', sa.Integer(), nullable=False),
        sa.Column('pos_y', sa.Integer(), nullable=False),

        sa.Column('color', sa.String(length=20), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('rpg_map_regions')