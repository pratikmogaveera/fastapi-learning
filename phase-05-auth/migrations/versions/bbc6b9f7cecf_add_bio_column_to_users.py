"""add bio column to users

Revision ID: bbc6b9f7cecf
Revises: 8ec1395313a1
Create Date: 2026-09-10 21:49:02.681735

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bbc6b9f7cecf"
down_revision: Union[str, Sequence[str], None] = "8ec1395313a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))


def downgrade() -> None:
  """Downgrade schema."""
  op.drop_column("users", "bio")
