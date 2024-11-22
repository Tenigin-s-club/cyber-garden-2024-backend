from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    fio: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    position: Mapped[str]
    role: Mapped[int]
    password: Mapped[str]
