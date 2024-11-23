from uuid import UUID

from pydantic import BaseModel, EmailStr


class SLoginUser(BaseModel):
    email: EmailStr
    password: str


class SInfoUser(BaseModel):
    fio: str
    email: EmailStr
    position: str
    role_id: int


class SRegisterUser(BaseModel):
    fio: str
    email: EmailStr
    position: str
    role: str
    password: str
    office_id: int | None = None
    floor_id: int | None = None


class SUser(BaseModel):
    id: UUID
    fio: str
    email: EmailStr
    position: str
    role_id: int
    password: str
