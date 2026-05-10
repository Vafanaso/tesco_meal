"""add price column to product_info, widen name

Revision ID: a1b2c3d4e5f6
Revises: 4d3cb47aca4f
Create Date: 2026-05-10 10:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "4d3cb47aca4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add a nullable ``price`` column and widen ``name`` to fit longer titles."""
    op.add_column(
        "product_info",
        sa.Column("price", sa.Float(), nullable=True),
    )
    op.alter_column(
        "product_info",
        "name",
        existing_type=sa.String(length=100),
        type_=sa.String(length=200),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Drop the ``price`` column and shrink ``name`` back to 100 chars."""
    op.alter_column(
        "product_info",
        "name",
        existing_type=sa.String(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.drop_column("product_info", "price")
