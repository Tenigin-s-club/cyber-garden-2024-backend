from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID

from app.db.base import Base

class UserInventoryFurniture(Base):
    __tablename__ = "user_inventory_furniture"
    
    id: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    furniture_id: Mapped[int | None] = mapped_column(ForeignKey("furniture.id"))
    inventory_id: Mapped[int | None] = mapped_column(ForeignKey("inventory.id"))