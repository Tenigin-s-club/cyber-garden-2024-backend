from pydantic import BaseModel, model_validator
from typing import Optional



class SInventoryType(BaseModel):
    id: int
    name: str
    

class SFurnitureType(BaseModel):
    id: int
    name: str
    size_x: int
    size_y: int


class SInventoryTypeCreate(BaseModel):
    name: str
    office_id: int


class SFurnitureTypeCreate(BaseModel):
    name: str
    size_x: int 
    size_y: int
    
    
class SMapPlace(BaseModel):
    id: int | None = None
    furniture_id: int
    x: int
    y: int
    is_vertical: bool
    
    
class SMap(BaseModel):
    items: list[SMapPlace]

    
class SFurnitureIDS(BaseModel):
    furniture_ids: list[int]
    
    
class SFurnitureEmployee(SFurnitureIDS):
    user_id: str


class SFurnitureID(BaseModel):
    furniture_id: int
    

class SInventoryIDS(BaseModel):
    inventory_ids: list[int]


class SInventoryEmployee(SInventoryIDS):
    user_id: str


class SInventoryID(BaseModel):
    inventory_id: int
