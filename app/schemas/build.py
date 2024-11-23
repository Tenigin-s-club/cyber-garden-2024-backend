from pydantic import BaseModel


class SInventoryType(BaseModel):
    id: int
    name: str


class SFurnitureType(BaseModel):
    id: int
    name: str


class SInventoryTypeCreate(BaseModel):
    name: str


class SFurnitureTypeCreate(BaseModel):
    name: str
    size_x: int 
    size_y: int
    
    
class SMapPlace(BaseModel):
    id: int
    type: int
    x: int
    y: int
    is_vertical: bool
    
    
class SMap(BaseModel):
    items: list[SMapPlace]

    
class SFurnitureEmployee(BaseModel):
    furniture_id: int
    user_id: str


class SFurnitureID(BaseModel):
    furniture_id: int


class SInventoryEmployee(BaseModel):
    inventory_id: int
    employee_id: str


class SInventoryID(BaseModel):
    inventory_id: int
