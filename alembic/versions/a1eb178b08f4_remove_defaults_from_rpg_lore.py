from alembic import op
import sqlalchemy as sa

revision = 'a1eb178b08f4'
down_revision = 'bab699ddd45e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "rpg_lore",
        "category",
        existing_type=sa.String(length=50),
        server_default=None
    )

    op.alter_column(
        "rpg_lore",
        "order",
        existing_type=sa.Integer(),
        server_default=None
    )


def downgrade():
    op.alter_column(
        "rpg_lore",
        "category",
        existing_type=sa.String(length=50),
        server_default="Geral"
    )

    op.alter_column(
        "rpg_lore",
        "order",
        existing_type=sa.Integer(),
        server_default="0"
    )