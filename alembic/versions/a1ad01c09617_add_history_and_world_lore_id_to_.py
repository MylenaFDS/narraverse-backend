"""add history and world_lore_id to characters

Revision ID: a1ad01c09617
Revises: 49462cb97e00
Create Date: 2026-05-24 02:27:52.550203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1ad01c09617'
down_revision: Union[str, Sequence[str], None] = '49462cb97e00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "characters",
        sa.Column(
            "history",
            sa.Text(),
            nullable=True
        )
    )

    op.add_column(
        "characters",
        sa.Column(
            "world_lore_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_character_world_lore",
        "characters",
        "rpg_lore",
        ["world_lore_id"],
        ["id"]
    )


def downgrade():
    op.drop_constraint(
        "fk_character_world_lore",
        "characters",
        type_="foreignkey"
    )

    op.drop_column(
        "characters",
        "world_lore_id"
    )

    op.drop_column(
        "characters",
        "history"
    )