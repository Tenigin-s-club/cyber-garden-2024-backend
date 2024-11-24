import json

from fastapi import APIRouter, status, Depends
from fastapi.responses import FileResponse
from asyncpg import connect
from docx import Document
from sqlalchemy import select

from app.config import settings
from app.schemas.build import SMap, SMapPlace, SInventoryType
from app.schemas.office import SOfficeCreate, SFloorCreate, SOfficeInventory, SOfficeEmployee
from app.repositories.offices import OfficesRepository, FloorsRepository
from app.utils import get_admin_token
from app.db.base import async_session_maker
from app.db.models import Office


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
async def get_office_inventory(office_id: int) -> list[SOfficeInventory]:
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    result = await conn.fetch(f"""
        SELECT user_inventory.id, inventory.name, users.fio FROM users
        JOIN user_inventory ON user_inventory.user_id = users.id
        JOIN inventory ON user_inventory.inventory_id = inventory.id
        WHERE office_id='{office_id}'
    """)
    return [SOfficeInventory(**elem) for elem in result]
    

@router.get('/employees/{office_id}')
async def get_office_employees(office_id) -> list[SOfficeEmployee]:
    conn = await connect(settings.POSTGRES_CLEAR_URL)
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
            ) as inventory,
            coalesce(json_agg(json_build_object(
                'id', furniture.id
            )) filter (where furniture.id is not null), '[]'
            ) as furniture
        FROM users
        LEFT JOIN user_inventory ON user_inventory.user_id = users.id
        LEFT JOIN user_furniture ON user_furniture.user_id = users.id
        LEFT JOIN inventory ON user_inventory.inventory_id = inventory.id
        LEFT JOIN furniture ON user_furniture.furniture_id = furniture.id
        WHERE office_id='{office_id}'
        GROUP BY users.id
    """)
    return [SOfficeEmployee(**elem) for elem in result]


@router.get('/employees/{employee_id}/inventory')
async def get_employee_inventory(employee_id: str) -> list[SInventoryType]:
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    result = await conn.fetch(f"""
        SELECT inventory.id, inventory.name FROM user_inventory
        JOIN inventory ON inventory.id = user_inventory.inventory_id
        WHERE user_id='{employee_id}'
    """)
    return [SInventoryType(**elem) for elem in result]
    
    
@router.get('/map/{office_id}')
async def get_map(office_id: int, floor_id: int | None = None) -> SMap:
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    query = f"SELECT * FROM map WHERE office_id='{office_id}'"
    if floor_id:
        query += f"AND floor_id='{floor_id}'"
    result = await conn.fetch(query)
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
    
    
# @router.get('/stats', status_code=status.HTTP_200_OK)
# async def get_statistics(access_token: str = Depends(get_admin_token)):
#     doc = Document()
#     doc.add_heading('Статистика оборудования', 0)
#     conn = await connect(settings.POSTGRES_CLEAR_URL)
#     await conn.set_type_codec(
#         'json',
#         encoder=json.dumps,
#         decoder=json.loads,
#         schema='pg_catalog'
#     )
#     result = await conn.fetch("""
# SELECT 
#     offices.name AS office_name, 
#     offices.address,
#     COALESCE(
#         JSON_AGG(
#                 floors.id
#         ), '[]'
#     ) AS floors,
#     COALESCE(
#         JSON_AGG(
#             JSON_BUILD_OBJECT(
#                 'id', users.id, 
#                 'user_inventory', (
#                     SELECT COALESCE(
#                         JSON_AGG(
#                             JSON_BUILD_OBJECT(
#                                 'id', user_inventory.id
#                             )
#                         ), '[]'
#                     )
#                     FROM user_inventory
#                 )
#             )
#         ), '[]'
#     ) AS users
# FROM offices
# LEFT JOIN floors ON floors.office_id = offices.id
# LEFT JOIN users ON users.office_id = offices.id
# GROUP BY offices.id;
# """)
#     print(result)
#     result = [dict(office) for office in result]
#     for office in result:
#         print(office)
#         items_quantity = 0
#         for user in office["users"]:
#             items_quantity += len(user["user_inventory"])
#         doc.add_heading(f"Офис №{result.index(office)+1}:")
#         doc.add_paragraph(f"Название: {office["office_name"]}\nАдресс: {office["address"]}")
#         doc.add_paragraph(f"""Количество этажей: {len(office["floors"])}
# Количество сотрудников: {len(office["users"])}
# Количество инвенторя сотрудников: {items_quantity}
# """)
#     doc.save('stats.docx')
#     return FileResponse(path='stats.docx', filename='stats.docx', media_type='multipart/form-data')


    
