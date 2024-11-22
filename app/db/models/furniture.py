from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID

from app.db.base import Base

class FurnitureTypes(Base):
    __tablename__ = "furniture"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    size_x: Mapped[int]
    size_y: Mapped[int]