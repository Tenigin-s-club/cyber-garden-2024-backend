from fastapi import APIRouter, status

from app.schemas.build import SCreateInventory, SCreateFurniture, SMap, SItem, SEmployeeItem


router = APIRouter(
    prefix="/build",
    tags=["Build"]
)


@router.get("/inventory")
async def get_inventory():
    return [
    {
        "id": 1,
        "name": "govno-mac",
    },
    {
        "id": 1,
        "name": "govno-mac",
    },
    {
        "id": 1,
        "name": "govno-mac",
    }
]
    
    
@router.get("/furniture")
async def get_furniture():
    return [
    {
        "id": 1,
        "name": "stol",
    },
        {
        "id": 1,
        "name": "stol",
    },
        {
        "id": 1,
        "name": "stol",
    }
]
    
    
@router.post("/inventory", status_code=status.HTTP_201_CREATED)
async def add_inventory(inventory: SCreateInventory):
    return {
    "id": 475
}
    
    
@router.post("/furniture", status_code=status.HTTP_201_CREATED)
async def add_furniture(Furniture: SCreateFurniture):
    return {
    "id": 777
}
    
    
@router.delete("/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(inventory_id: int) -> None:
    pass


@router.put("/edit/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_floor(
    floor_id: int,
    map: SMap
) -> None:
    pass


@router.post("/attach/employee", status_code=status.HTTP_201_CREATED)
async def attach_employee(place_employee: SEmployeeItem):
    pass


@router.put("/attach/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee_place(
    employee_id: int,
    place: SItem
) -> None:
    pass


@router.delete("/attach/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place_employee(employee_id: int) -> None:
    pass


@router.post("/attach/inventory", status_code=status.HTTP_201_CREATED)
async def attache_inventory(item_employee: SEmployeeItem):
    pass


@router.put("/attach/inventory/{employee_id}", status_code=status.HTTP_201_CREATED)
async def update_employee_inventory(
    employee_id: int,
    inventory: SItem
) -> None:
    pass


@router.delete("/attach/inventory/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(employee_id) -> None:
    pass