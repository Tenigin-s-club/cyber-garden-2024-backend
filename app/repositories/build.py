from sqlalchemy import insert, select, or_

from app.db.models import InventoryTypes, FurnitureTypes, UserFurniture, UserInventory, WhoreHouse, User
from app.db.base import async_session_maker
from app.repositories.base import BaseRepository
from app.schemas.build import SInventoryType, SFurnitureType, \
SFurnitureEmployee, SInventoryEmployee, SInventoryID, SInventoryTypeCreate, SInventoryEmployeeOffice


class InventoryTypesRepository(BaseRepository):
    model = InventoryTypes
    model_pydantic_schema = SInventoryType
    
    @staticmethod
    async def create_inventory(inventory: SInventoryTypeCreate) -> SInventoryID:
        async with async_session_maker() as session:
            insert_query = insert(InventoryTypes).values(
                name=inventory.name
            ).returning(InventoryTypes.id)
            inventory_id = await session.execute(insert_query)
            inventory_id = inventory_id.scalar()
            insert_query_whorehouse = insert(WhoreHouse).values(
                office_id=inventory.office_id,
                inventory_id=inventory_id
            )
            await session.execute(insert_query_whorehouse)
            await session.commit()
            return inventory_id
        
    @staticmethod
    async def get_office_inventory(office_id: int, is_free: bool):
        async with async_session_maker() as session:
            query = (select(InventoryTypes.name, InventoryTypes.id, User.fio)
                     .where(or_(User.office_id == office_id, WhoreHouse.office_id == office_id))
                     .join(UserInventory, UserInventory.inventory_id == InventoryTypes.id, isouter=True)
                     .join(User, User.id == UserInventory.user_id, isouter=True))
            
            if is_free:
                query = query.where(User.fio == None)
            else:
                query = query.where(User.fio != None)
            inventory = await session.execute(query)
            inventory = inventory.unique().mappings().all()
            return [SInventoryEmployeeOffice(**row) for row in inventory]
            
            

class FurnitureTypesRepository(BaseRepository):
    model = FurnitureTypes
    model_pydantic_schema = SFurnitureType


class InventoryEmployeeRepository(BaseRepository):
    model = UserInventory
    model_pydantic_schema = None
    
    
    @staticmethod
    async def create_attaches_inventory(inventory_employee: SInventoryEmployee) -> None:
        async with async_session_maker() as session:
            ids = []
            for inventory_id in inventory_employee.inventory_ids:
                query_add = (insert(UserInventory).values(
                    user_id=inventory_employee.user_id,
                    inventory_id=inventory_id
                ).returning(UserInventory.id))
                id = await session.execute(query_add)
                ids.append(id.scalar())
                
            await session.commit()
            return ids


class FurnitureEmployeeRepository(BaseRepository):
    model = UserFurniture
    model_pydantic_schema = None
    
    
    @staticmethod
    async def create_attaches_furniture(furniture_employee: SFurnitureEmployee) -> None:
        async with async_session_maker() as session:
            ids = []
            for furniture_id in furniture_employee.furniture_ids:
                query_add = (insert(UserFurniture).values(
                    user_id=furniture_employee.user_id,
                    furniture_id=furniture_id
                ).returning(UserFurniture.id))
                id = await session.execute(query_add)
                ids.append(id.scalar())
                
            await session.commit()
            return ids
