from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID

from app.db.base import Base

class UserFurniture(Base):
    __tablename__ = "user_furniture"
    # primary key = user_id + furniture_id
    # rename user_id -> employee_id??
    # unique constraint on user_id
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    furniture_id: Mapped[int] = mapped_column(ForeignKey("furniture.id", ondelete="CASCADE"))
