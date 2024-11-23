from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base import Base


class WhoreHouse(Base):
    __tablename__ = "whorehouse"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    office_id: Mapped[int] = mapped_column(ForeignKey("offices.id"))
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"), unique=True)
    
    