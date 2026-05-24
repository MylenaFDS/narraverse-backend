"""add image_url to characters

Revision ID: ec3d8cb97e13
Revises: 23b27bc174a7
Create Date: 2026-05-24 13:03:10.377127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec3d8cb97e13'
down_revision: Union[str, Sequence[str], None] = '23b27bc174a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "characters",
        sa.Column(
            "image_url",
            sa.String(),
            nullable=True
        )
    )


def downgrade():
    op.drop_column(
        "characters",
        "image_url"
    )