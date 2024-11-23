from fastapi import APIRouter, status

from app.config import settings
from app.repositories.build import InventoryTypesRepository, FurnitureTypesRepository, FurnitureEmployeeRepository, \
    InventoryEmployeeRepository
from app.schemas.build import SInventoryTypeCreate, SFurnitureTypeCreate, SMap, SFurnitureEmployee, SMapPlace, \
    SFurnitureID, SInventoryEmployee, SInventoryID

from asyncpg import connect

router = APIRouter(
    prefix="/build",
    tags=["Build"]
)


@router.get("/inventory")
async def get_inventory():
    return await InventoryTypesRepository.find_all()
    
    
@router.get("/furniture")
async def get_furniture():
    return await FurnitureTypesRepository.find_all()
    
    
@router.post("/inventory", status_code=status.HTTP_201_CREATED)
async def add_inventory(inventory: SInventoryTypeCreate):
    return await InventoryTypesRepository.create(**inventory.model_dump())
    
    
@router.post("/furniture", status_code=status.HTTP_201_CREATED)
async def add_furniture(furniture: SFurnitureTypeCreate):
    return await FurnitureTypesRepository.create(**furniture.model_dump())
    

@router.delete("/inventory/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(inventory_id: int) -> None:
    await InventoryTypesRepository.delete(id=inventory_id)


@router.delete("/inventory/{furniture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(furniture_id: int) -> None:
    await InventoryTypesRepository.delete(id=furniture_id)


@router.put("/edit/{office_id}/{floor_id}", status_code=status.HTTP_200_OK)
async def update_floor(
    office_id: int,
    floor_id: int,
    map: SMap
):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    await conn.execute(f"DELETE * FROM map WHERE office_id='{office_id}' AND floor_id='{floor_id}'")
    for item in map.items:
        if not item.id:
            await conn.execute(f"""
                INSERT INTO map (office_id, floor_id, furniture_id, x, y, is_vertical)
                VALUES ({office_id}, {floor_id}, {item.type}, {item.x}, {item.y}, {item.is_vertical});
            """)
        else:
            await conn.execute(f"""
                INSERT INTO map (id, office_id, floor_id, furniture_id, x, y, is_vertical)
                VALUES ({item.id}, {office_id}, {floor_id}, {item.type}, {item.x}, {item.y}, {item.is_vertical});
            """)
    result = await conn.fetch(f"SELECT * FROM map WHERE office_id='{office_id}' AND floor_id='{floor_id}'")
    return SMap(items=[SMapPlace(**item) for item in result])


@router.post("/attach/employee", status_code=status.HTTP_201_CREATED)
async def attach_employee_furniture(furniture_employee: SFurnitureEmployee):
    await FurnitureEmployeeRepository.create(
        user_id=furniture_employee.employee_id,
        furniture_id=furniture_employee.place_id,
    )


@router.post("/attach/inventory", status_code=status.HTTP_201_CREATED)
async def attach_employee_inventory(inventory_employee: SInventoryEmployee):
    await InventoryEmployeeRepository.create(
        user_id=inventory_employee.employee_id,
        inventory_id=inventory_employee.place_id,
    )


@router.put("/attach/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee_furniture(
    employee_id: int,
    furniture: SFurnitureID
):
    await FurnitureEmployeeRepository.update(
        id_=employee_id,
        furniture_id=furniture.furniture_id,
    )


@router.put("/attach/inventory/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee_inventory(
    employee_id: int,
    inventory: SInventoryID
):
    await InventoryEmployeeRepository.update(
        id_=employee_id,
        furniture_id=inventory.inventory_id,
    )


@router.delete("/attach/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_furniture(employee_id: int) -> None:
    await FurnitureEmployeeRepository.delete(user_id=employee_id)


@router.delete("/attach/inventory/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee_inventory(employee_id: int) -> None:
    await InventoryEmployeeRepository.delete(user_id=employee_id)
