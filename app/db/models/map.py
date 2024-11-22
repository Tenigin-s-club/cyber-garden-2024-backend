from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base import Base

class Map(Base):
    __tablename__ = "map"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    office_id: Mapped[int] = mapped_column(ForeignKey("offices.id"))
    floor_id: Mapped[int] = mapped_column(ForeignKey("floors.id"))
    furniture_id: Mapped[int] = mapped_column(ForeignKey("furniture.id"))
    is_vertical: Mapped[bool]
    