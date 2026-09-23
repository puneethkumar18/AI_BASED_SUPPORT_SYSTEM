"""add resolved status to ticketstatus enum

Revision ID: 00b071c697fb
Revises: 362c9429e875
Create Date: 2026-09-22 05:43:14.008714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00b071c697fb'
down_revision: Union[str, Sequence[str], None] = '362c9429e875'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE ticketstatus ADD VALUE IF NOT EXISTS 'RESOLVED'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
