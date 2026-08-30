from datetime import datetime

from database import Base
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class Links(Base):
  __tablename__ = "links"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  short_code: Mapped[str] = mapped_column(unique=True)
  original_url: Mapped[str]
  created_at: Mapped[datetime] = mapped_column(server_default=func.now())
