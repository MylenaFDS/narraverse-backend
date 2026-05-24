"""add history and world_lore_id to characters

Revision ID: 23b27bc174a7
Revises: a1ad01c09617
Create Date: 2026-05-24 02:37:22.710036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23b27bc174a7'
down_revision: Union[str, Sequence[str], None] = 'a1ad01c09617'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

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
    