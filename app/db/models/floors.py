from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.db.base import Base

class Floor(Base):
    __tablename__ = "floors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    office_id: Mapped[int] = mapped_column(ForeignKey("offices.id", ondelete="CASCADE"))
    