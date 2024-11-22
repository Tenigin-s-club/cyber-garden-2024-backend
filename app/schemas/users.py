from uuid import UUID

from pydantic import BaseModel, EmailStr


class SLoginUser(BaseModel):
    email: EmailStr
    password: str


class SRegisterUser(BaseModel):
    fio: str
    email: EmailStr
    position: str
    role_id: int
    password: str


class SUser(BaseModel):
    id: UUID
    fio: str
    email: EmailStr
    position: str
    role_id: int
    password: str
