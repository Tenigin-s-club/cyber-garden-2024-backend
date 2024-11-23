from pydantic import BaseModel, EmailStr
from uuid import UUID


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
