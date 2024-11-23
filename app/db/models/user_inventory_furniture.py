from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID

from app.db.base import Base

class UserInventoryFurniture(Base):
    __tablename__ = "user_inventory_furniture"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    furniture_id: Mapped[int | None] = mapped_column(ForeignKey("furniture.id", ondelete="CASCADE"))
    inventory_id: Mapped[int | None] = mapped_column(ForeignKey("inventory.id", ondelete="CASCADE"))
    inventory: Mapped["InventoryTypes"] = relationship()