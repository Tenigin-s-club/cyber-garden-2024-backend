import json

from fastapi import APIRouter, status, Depends

from app.config import settings
from app.schemas.build import SMap, SMapPlace, SInventoryType
from app.schemas.office import SOfficeCreate, SFloorCreate, SOfficeInventory, SOfficeEmployee
from app.repositories.offices import OfficesRepository, FloorsRepository

from asyncpg import connect

from app.utils import check_endpoint_permissions

router = APIRouter(
    prefix="/offices",
    tags=["Offices"],
    dependencies=[Depends(check_endpoint_permissions)]
)


@router.get('/offices', status_code=status.HTTP_200_OK)
async def get_offices():
    return await OfficesRepository.find_all()


@router.get('/floors/{office_id}', status_code=status.HTTP_200_OK)
async def get_office_floors(office_id: int):
    return await FloorsRepository.find_all(office_id=office_id)


@router.get('/inventory/{office_id}', status_code=status.HTTP_200_OK)
async def get_office_inventory(office_id: int):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    result = await conn.fetch(f"""
        SELECT user_inventory.id, inventory.name, users.fio FROM users
        JOIN user_inventory ON user_inventory.user_id = users.id
        JOIN inventory ON user_inventory.inventory_id = inventory.id
        WHERE office_id='{office_id}'
    """)
    return [SOfficeInventory(**elem) for elem in result]
    

@router.get('/employees/{office_id}')
async def get_office_employees(office_id):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    await conn.set_type_codec(
        'json',
        encoder=json.dumps,
        decoder=json.loads,
        schema='pg_catalog'
    )
    result = await conn.fetch(f"""
        SELECT
            users.id,
            users.fio,
            users.position,
            users.email,
            coalesce(json_agg(json_build_object(
                'id', inventory.id, 'name', inventory.name
                )) filter (where inventory.id is not null), '[]'
            ) as inventory
        FROM users
        JOIN user_inventory ON user_inventory.user_id = users.id
        JOIN inventory ON user_inventory.inventory_id = inventory.id
        WHERE office_id='{office_id}'
        GROUP BY users.id
    """)
    return [SOfficeEmployee(**elem) for elem in result]


@router.get('/employees/{employee_id}/inventory')
async def get_employee_inventory(employee_id: int):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    result = await conn.fetch(f"""
        SELECT inventory.id, inventory.name FROM user_inventory
        JOIN inventory ON inventory.id = user_inventory.inventory_id
        WHERE user_id='{employee_id}'
    """)
    return [SInventoryType(**elem) for elem in result]
    
    
@router.get('/map/{office_id}/{floor_id}')
async def get_map(office_id: int, floor_id: int):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    result = await conn.fetch(f"SELECT * FROM map WHERE office_id='{office_id}' AND floor_id='{floor_id}'")
    return SMap(items=[SMapPlace(**item) for item in result])
    

@router.post("/office", status_code=status.HTTP_201_CREATED)
async def create_office(office: SOfficeCreate):
    return await OfficesRepository.create(**office.model_dump())
    
    
@router.post("/floor", status_code=status.HTTP_201_CREATED)
async def create_floor(floor: SFloorCreate):
    return await FloorsRepository.create(**floor.model_dump())
    
    
@router.put("/office/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_office(
    office_id: int, 
    office: SOfficeCreate
):
    await OfficesRepository.update(office_id, **office.model_dump())


@router.put("/floor/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_floor(
    floor_id: int,
    floor: SFloorCreate
):
    await OfficesRepository.update(floor_id, **floor.model_dump())


@router.delete("/office/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_office(office_id: int) -> None:
    await OfficesRepository.delete(id=office_id)


@router.delete("/floor/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_floor(floor_id: int) -> None:
    await FloorsRepository.delete(floor_id)
