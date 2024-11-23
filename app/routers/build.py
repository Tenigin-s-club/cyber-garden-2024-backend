from fastapi import APIRouter, status, Depends

from app.config import settings
from app.repositories.build import InventoryTypesRepository, FurnitureTypesRepository, FurnitureEmployeeRepository, \
    InventoryEmployeeRepository
from app.schemas.build import SInventoryTypeCreate, SFurnitureTypeCreate, SMap, SFurnitureEmployee, SMapPlace, \
    SFurnitureID, SInventoryEmployee, SInventoryID, SFurnitureIDS, SInventoryIDS

from asyncpg import connect

from app.utils import check_endpoint_permissions

router = APIRouter(
    prefix="/build",
    tags=["Build"],
    dependencies=[Depends(check_endpoint_permissions)]
)


@router.get("/inventory/{office_id}")
async def get_inventory(office_id: int):
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    result = await InventoryTypesRepository.get_office_inventory(office_id)
    return result
    
    
@router.get("/furniture")
async def get_furniture():
    return await FurnitureTypesRepository.find_all()
    
    
@router.post("/inventory", status_code=status.HTTP_201_CREATED)
async def add_inventory(inventory: SInventoryTypeCreate):
    id = await InventoryTypesRepository.create_inventory(inventory)
    return SInventoryID(inventory_id=id)
    
    
@router.post("/furniture", status_code=status.HTTP_201_CREATED)
async def add_furniture(furniture: SFurnitureTypeCreate):
    return await FurnitureTypesRepository.create(**furniture.model_dump())
    

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
):
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
async def attach_employee_furniture(furniture_employee: SFurnitureEmployee) -> SFurnitureIDS:
    ids = await FurnitureEmployeeRepository.create_attaches_furniture(furniture_employee)
    return SFurnitureIDS(furniture_ids=ids)
    
@router.post("/attach/inventory", status_code=status.HTTP_201_CREATED)
async def attach_employee_inventory(inventory_employee: SInventoryEmployee):
    ids = await InventoryEmployeeRepository.create_attaches_inventory(inventory_employee)
    return SInventoryIDS(inventory_ids=ids)


@router.delete("/attach/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_furniture(employee_id: int) -> None:
    await FurnitureEmployeeRepository.delete(user_id=employee_id)


@router.delete("/attach/inventory/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_inventory(employee_id: int) -> None:
    await InventoryEmployeeRepository.delete(user_id=employee_id)
