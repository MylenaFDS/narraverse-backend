"""add npc fields to character

Revision ID: e909c60bfd8f
Revises: a5ab566f6de4
Create Date: 2026-06-27
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e909c60bfd8f"
down_revision: Union[str, Sequence[str], None] = "a5ab566f6de4"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "characters",
        sa.Column(
            "is_npc",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "characters",
        sa.Column(
            "manual_control",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.add_column(
        "characters",
        sa.Column(
            "ai_control",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:

    op.drop_column("characters", "ai_control")
    op.drop_column("characters", "manual_control")
    op.drop_column("characters", "is_npc")