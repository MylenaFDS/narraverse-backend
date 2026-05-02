"""remove server defaults from rpg_lore

Revision ID: remove_defaults_rpg_lore
Revises: bab699ddd45e
Create Date: 2026-05-02
"""

from alembic import op
import sqlalchemy as sa


# IDs
revision = 'bab699ddd45e'
down_revision = '35815c98f26f'
branch_labels = None
depends_on = None


def upgrade():
    # 🔥 remove default do banco
    op.alter_column("rpg_lore", "category", server_default=None)
    op.alter_column("rpg_lore", "order", server_default=None)


def downgrade():
    # 🔙 restaura default (caso precise voltar)
    op.alter_column("rpg_lore", "category", server_default="Geral")
    op.alter_column("rpg_lore", "order", server_default="0")
