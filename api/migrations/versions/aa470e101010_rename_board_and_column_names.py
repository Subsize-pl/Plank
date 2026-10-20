"""rename board and column names

Revision ID: aa470e101010
Revises: fed9a8476916
Create Date: 2026-10-20 22:28:04.256766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa470e101010'
down_revision: Union[str, Sequence[str], None] = 'fed9a8476916'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename existing columns while preserving their data.
    op.alter_column("boards", "board_name", new_column_name="name")
    op.alter_column("columns", "column_name", new_column_name="name")


def downgrade() -> None:
    # Restore the original column names.
    op.alter_column("columns", "name", new_column_name="column_name")
    op.alter_column("boards", "name", new_column_name="board_name")
