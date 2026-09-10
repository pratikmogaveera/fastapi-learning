"""add is_active column to users

Revision ID: 4d1ff1b1ebd6
Revises: bbc6b9f7cecf
Create Date: 2026-09-10 22:13:06.172950

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4d1ff1b1ebd6"
down_revision: Union[str, Sequence[str], None] = "bbc6b9f7cecf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.add_column(
    "users", sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False)
  )


def downgrade() -> None:
  """Downgrade schema."""
  op.drop_column("users", "is_active")
