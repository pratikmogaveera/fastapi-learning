"""add avatar_url column to users

Revision ID: 4ba2e4855e2d
Revises: 79eceb9feb0d
Create Date: 2026-09-12 21:39:09.496739

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ba2e4855e2d"
down_revision: Union[str, Sequence[str], None] = "4d1ff1b1ebd6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  pass


def downgrade() -> None:
  """Downgrade schema."""
  pass
