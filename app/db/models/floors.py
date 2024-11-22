from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base import Base

class Floor(Base):
    id: Mapped[int]
    name: Mapped[str] = mapped_column(unique=True)