from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class InventoryTypes(Base):
    __tablename__ = "inventory"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    