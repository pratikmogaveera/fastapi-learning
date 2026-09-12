"""merge phone and avatar branches

Revision ID: 0dd540d4c8ac
Revises: 4ba2e4855e2d, 79eceb9feb0d
Create Date: 2026-09-12 21:42:01.554396

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0dd540d4c8ac"
down_revision: Union[str, Sequence[str], None] = ("4ba2e4855e2d", "79eceb9feb0d")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  pass


def downgrade() -> None:
  """Downgrade schema."""
  pass
