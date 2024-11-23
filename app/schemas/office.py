from pydantic import BaseModel, EmailStr
from uuid import UUID

class SCreateOffice(BaseModel):
    name: str
    image: str
    address: str
    

class SCreateFloor(BaseModel):
    office_id: int
    name: str
    

class SGetOffice(SCreateOffice):
    id: int
    
    
class SGetFloor(BaseModel):
    id: int
    name: str
    
    
class SEmployeeInventory(BaseModel):
    id: int
    name: str
    

class SGetUser(BaseModel):
    id: UUID
    fio: str
    position: str
    place: int
    email: EmailStr
    # inventory: list[SEmployeeInventory]
    

class SMap(BaseModel):
    id: int
    type: int
    x: int
    y: int
    is_vertical: bool
    
    
class SInventory(BaseModel):
    id: int
    name: str
    fio: str
