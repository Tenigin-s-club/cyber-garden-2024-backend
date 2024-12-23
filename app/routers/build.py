from fastapi import APIRouter, status, Depends
from typing import Literal

from app.config import settings
from app.repositories.build import InventoryTypesRepository, FurnitureTypesRepository, FurnitureEmployeeRepository, \
    InventoryEmployeeRepository
from app.schemas.build import SInventoryTypeCreate, SFurnitureTypeCreate, SMap, SFurnitureEmployee, SMapPlace, \
    SFurnitureID, SInventoryEmployee, SInventoryID, SFurnitureIDS, SInventoryIDS, SInventoryBase, SFurnitureIDFurniture

from asyncpg import connect

from app.utils import check_endpoint_permissions

router = APIRouter(
    prefix="/build",
    tags=["Build"],
    dependencies=[Depends(check_endpoint_permissions)]
)


@router.get("/inventory/{office_id}")
async def get_inventory(office_id: int, status: Literal["free", "not_free"] | None = None):
    result = await InventoryTypesRepository.get_office_inventory(office_id, status)
    return result
    
    
@router.get("/furniture/{office_id}")
async def get_furniture(office_id: int):
    return await FurnitureTypesRepository.get_office_furniture(office_id)
    
    
@router.post("/inventory", status_code=status.HTTP_201_CREATED)
async def add_inventory(inventory: SInventoryTypeCreate) -> SInventoryID:
    id = await InventoryTypesRepository.create_inventory(inventory)
    return SInventoryID(inventory_id=id)
    
    
@router.post("/furniture", status_code=status.HTTP_201_CREATED)
async def add_furniture(furniture: SFurnitureTypeCreate):
    id = await FurnitureTypesRepository.create_furniture(furniture)
    return SFurnitureIDFurniture(furniture_id=id)
    

@router.delete("/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(inventory_id: int) -> None:
    await InventoryTypesRepository.delete(id=inventory_id)


@router.delete("/furniture/{furniture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_furniture(furniture_id: int) -> None:
    await FurnitureTypesRepository.delete(id=furniture_id)


@router.put("/edit/{office_id}/{floor_id}", status_code=status.HTTP_200_OK)
async def update_floor(
    office_id: int,
    floor_id: int,
    map: SMap
) -> SMap:
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    await conn.execute(f"DELETE FROM map WHERE office_id='{office_id}' AND floor_id='{floor_id}'")
    for item in map.items:
        if not item.id:
            await conn.execute(f"""
                INSERT INTO map (office_id, floor_id, furniture_id, x, y, is_vertical)
                VALUES ({office_id}, {floor_id}, {item.furniture_id}, {item.x}, {item.y}, {item.is_vertical});
            """)
        else:
            await conn.execute(f"""
                INSERT INTO map (id, office_id, floor_id, furniture_id, x, y, is_vertical)
                VALUES ({item.id}, {office_id}, {floor_id}, {item.furniture_id}, {item.x}, {item.y}, {item.is_vertical});
            """)
    result = await conn.fetch(f"SELECT * FROM map WHERE office_id='{office_id}' AND floor_id='{floor_id}'")
    return SMap(items=[SMapPlace(**item) for item in result])


@router.post("/attach/furniture", status_code=status.HTTP_201_CREATED)
async def attach_employee_furniture(furniture_employee: SFurnitureEmployee) -> None:
    await FurnitureEmployeeRepository.create_attaches_furniture(furniture_employee)
    
    
    
@router.post("/attach/inventory", status_code=status.HTTP_201_CREATED)
async def attach_employee_inventory(inventory_employee: SInventoryEmployee) -> None:
    await InventoryEmployeeRepository.create_attaches_inventory(inventory_employee)


@router.put("/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_inventory(
    inventory_id: int,
    inventory: SInventoryBase
) -> None:
    await InventoryTypesRepository.update(inventory_id, **inventory.model_dump())


@router.delete("/attach/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_furniture(employee_id: int) -> None:
    await FurnitureEmployeeRepository.delete(user_id=employee_id)


@router.delete("/attach/inventory/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_inventory(employee_id: int) -> None:
    await InventoryEmployeeRepository.delete(user_id=employee_id)
    

@router.delete("/attach/inventory/employee/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attach_employee_inventory(
    inventory_id: int
) -> None:
    await InventoryEmployeeRepository.delete(inventory_id=inventory_id)
