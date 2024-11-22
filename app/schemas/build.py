from pydantic import BaseModel


class SCreateInventory(BaseModel):
    name: str
    
    
class SCreateFurniture(BaseModel):
    name: str
    size_x: int
    size_y: int
    
    
class SMapPlace(BaseModel):
    id: int
    type: int
    x: int
    y: int
    is_vertical: int
    
    
class SMap(BaseModel):
    items: list[SMapPlace]
    
    
class SItem(BaseModel):
    place_id: int

    
class SEmployeeItem(SItem):
    employee_id: int
    
