from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text

from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=text('uuid_generate_v4()'))
    fio: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    position: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    role: Mapped["Role"] = relationship()
    password: Mapped[str]
    office_id: Mapped[int | None] = mapped_column(ForeignKey("offices.id"))
    floor_id: Mapped[int | None] = mapped_column(ForeignKey("floors.id"))
    inventory: Mapped[list["UserInventory"]] = relationship(uselist=True)
    furniture: Mapped[list["UserFurniture"]] = relationship(uselist=True)
    
