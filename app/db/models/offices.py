from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Office(Base):
    __tablename__ = "offices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str] = mapped_column(unique=True)
    image: Mapped[str]
    
    