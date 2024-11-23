from app.db.models.users import User
from app.repositories.base import BaseRepository
from app.schemas.users import SUser


class UsersRepository(BaseRepository):
    model = User
    model_pydantic_schema = SUser
