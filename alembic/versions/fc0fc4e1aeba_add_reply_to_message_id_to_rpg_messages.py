"""add reply_to_message_id to rpg_messages

Revision ID: fc0fc4e1aeba
Revises: 02a508ab3b30
Create Date: 2026-05-21
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# 🔥 ESSENCIAL (isso está faltando)
revision: str = "fc0fc4e1aeba"
down_revision: Union[str, None] = "02a508ab3b30"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "rpg_messages",
        sa.Column(
            "reply_to_message_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.create_foreign_key(
        "fk_reply_message",
        "rpg_messages",
        "rpg_messages",
        ["reply_to_message_id"],
        ["id"]
    )


def downgrade():
    op.drop_constraint(
        "fk_reply_message",
        "rpg_messages",
        type_="foreignkey"
    )

    op.drop_column(
        "rpg_messages",
        "reply_to_message_id"
    )