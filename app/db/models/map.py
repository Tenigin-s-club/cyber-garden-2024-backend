from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base import Base

class Map(Base):
    __tablename__ = "map"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    office_id: Mapped[int] = mapped_column(ForeignKey("offices.id", ondelete="CASCADE"))
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id", ondelete="CASCADE"))
    furniture_id: Mapped[int] = mapped_column(ForeignKey("furniture.id", ondelete="CASCADE"))
    is_vertical: Mapped[bool]
    x: Mapped[int]
    y: Mapped[int]
    