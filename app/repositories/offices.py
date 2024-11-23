from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import selectinload, aliased, load_only

from app.repositories.base import BaseRepository
from app.db.models import Office, User, Floor, UserInventoryFurniture, InventoryTypes, Map
from app.db.base import async_session_maker
from app.schemas.office import SGetOffice, SGetFloor, SGetUser, SMap, SInventory, SCreateOffice, SCreateFloor, SEmployeeInventory


class OfficeRepository():
    
    @staticmethod
    async def get_offices() -> list[SGetOffice]:
        async with async_session_maker() as session:
            query = select(Office.__table__.columns)
            offices = await session.execute(query)
            offices = offices.mappings().all()
            return [SGetOffice(**office) for office in offices]
        
    @staticmethod
    async def get_floors(office_id: int) -> list[SGetFloor]:
        async with async_session_maker() as session:
            query = select(Floor.id, Floor.name).filter_by(office_id=office_id)
            floors = await session.execute(query)
            floors = floors.mappings().all()
            return [SGetFloor(**floor) for floor in floors]
        
    @staticmethod
    async def get_employees(office_id) -> list[SGetUser]:
        pass
        
    @staticmethod
    async def get_map(office_id: int, floor_id: int) -> list[SMap]:
        async with async_session_maker() as session:
            m = aliased(Map)
            query = (select(m.x, m.y, m.is_vertical, m.furniture_id, m.id)
                     .filter_by(office_id=office_id, floor_id=floor_id))
            map_ = await session.execute(query)
            map_ = map_.mappings().all()
            return [SMap(**item) for item in map_]
        
    @staticmethod
    async def get_inventory(office_id) -> list[SInventory]:
        pass
    
    @staticmethod
    async def get_employee_inventory(employee_id) -> list[SEmployeeInventory]:
        async with async_session_maker() as session:
            query = select()
        
    @staticmethod
    async def create_office(office: SCreateOffice) -> int:
        async with async_session_maker() as session:
            query = insert(Office).values(office.model_dump()).returning(Office.id)
            office_id = await session.execute(query)
            await session.commit()
            return office_id.scalar()
        
    @staticmethod
    async def create_floor(floor: SCreateFloor) -> int:
        async with async_session_maker() as session:
            query = insert(Floor).values(floor.model_dump()).returning(Floor.id)
            floor_id = await session.execute(query)
            await session.commit()
            return floor_id.scalar()
        
    @staticmethod
    async def update_office(office_id: int, office: SCreateOffice) -> None:
        async with async_session_maker() as session:
            query = update(Office).values(office.model_dump()).filter_by(id=office_id)
            await session.execute(query)
            await session.commit()
            
    @staticmethod
    async def update_floor(floor_id: int, floor: SCreateFloor) -> None:
        async with async_session_maker() as session:
            query = update(Floor).values(floor.model_dump()).filter_by(id=floor_id)
            await session.execute(query)
            await session.commit()
            
    @staticmethod
    async def delete_office(office_id: int) -> None:
        async with async_session_maker() as session:
            query = delete(Office).filter_by(id=office_id)
            await session.execute(query)
            await session.commit()
            
    @staticmethod
    async def delete_floor(floor_id: int) -> None:
        async with async_session_maker() as session:
            query = delete(Floor).filter_by(id=floor_id)
            await session.execute(query)
            await session.commit()
            
            
            