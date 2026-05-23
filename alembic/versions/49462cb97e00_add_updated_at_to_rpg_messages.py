"""add updated_at to rpg_messages

Revision ID: 49462cb97e00
Revises: fc0fc4e1aeba
Create Date: 2026-05-22 22:16:52.765070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49462cb97e00'
down_revision: Union[str, Sequence[str], None] = 'fc0fc4e1aeba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
    "rpg_messages",
    sa.Column(
        "updated_at",
        sa.DateTime(),
        nullable=True
    )
)

    op.execute(
        "UPDATE rpg_messages SET updated_at = created_at WHERE updated_at IS NULL"
    )
    pass


def downgrade() -> None:
    op.drop_column("rpg_messages", "updated_at")
    pass
