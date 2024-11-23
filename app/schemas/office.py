from pydantic import BaseModel, EmailStr, model_validator
from uuid import UUID
import json

from app.schemas.build import SInventoryType


class SOfficeCreate(BaseModel):
    name: str
    image: str
    address: str
    

class SFloorCreate(BaseModel):
    office_id: int
    name: str
    

class SOffice(SOfficeCreate):
    id: int
    
    
class SFloor(SFloorCreate):
    id: int


class SOfficeInventory(BaseModel):
    id: int
    name: str
    fio: str


class SOfficeEmployee(BaseModel):
    id: UUID
    fio: str
    position: str
    email: EmailStr
    inventory: list[SInventoryType]
