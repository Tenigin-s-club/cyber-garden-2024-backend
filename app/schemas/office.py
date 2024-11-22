from pydantic import BaseModel

class SCreateOffice(BaseModel):
    name: str
    image: str
    address: str
    

class SCreateFloor(BaseModel):
    office_id: int
    name: str