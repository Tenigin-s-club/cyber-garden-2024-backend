from uuid import UUID

from sqlalchemy import delete, insert, select, update

from app.db.base import async_session_maker
from app.db.models import InventoryTypes, FurnitureTypes
from app.db.models.user_furniture import UserFurniture
from app.db.models.user_inventory import UserInventory
from app.repositories.base import AbstractRepository
from app.schemas.build import SInventoryType, SFurnitureType
from app.schemas.users import SUser


class InventoryTypesRepository(AbstractRepository):
    @staticmethod
    async def find_all(**filter_by):
        async with async_session_maker() as session:
            query = select(InventoryTypes.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            return [SInventoryType(**elem) for elem in mapping_result] if mapping_result else None

    @staticmethod
    async def find_one_or_none(**filter_by) -> SUser:
        async with async_session_maker() as session:
            query = select(InventoryTypes.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return SInventoryType(**mapping_result) if mapping_result else None

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(SInventoryType).values(**values).returning(SInventoryType.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @staticmethod
    async def update(id, **values) -> None:
        raise NotImplementedError

    @staticmethod
    async def delete(**filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(SInventoryType).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()


class FurnitureTypesRepository(AbstractRepository):
    @staticmethod
    async def find_all(**filter_by):
        async with async_session_maker() as session:
            query = select(FurnitureTypes.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            return [SFurnitureType(**elem) for elem in mapping_result] if mapping_result else None

    @staticmethod
    async def find_one_or_none(**filter_by) -> SUser:
        async with async_session_maker() as session:
            query = select(FurnitureTypes.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return SFurnitureType(**mapping_result) if mapping_result else None

    @staticmethod
    async def create(**values) -> UUID:
        async with async_session_maker() as session:
            query = insert(FurnitureTypes).values(**values).returning(FurnitureTypes.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @staticmethod
    async def update(id, **values) -> None:
        raise NotImplementedError

    @staticmethod
    async def delete(**filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(FurnitureTypes).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()


class FurnitureEmployeeRepository(AbstractRepository):
    @staticmethod
    async def find_all(**filter_by):
        raise NotImplementedError

    @staticmethod
    async def find_one_or_none(**filter_by):
        raise NotImplementedError

    @staticmethod
    async def create(**values) -> None:
        async with async_session_maker() as session:
            query = insert(UserFurniture).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update(id_, **values) -> None:
        async with async_session_maker() as session:
            query = update(UserFurniture).filter_by(id=id_).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def delete(**filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(UserFurniture).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()


class InventoryEmployeeRepository(AbstractRepository):
    @staticmethod
    async def find_all(**filter_by):
        raise NotImplementedError

    @staticmethod
    async def find_one_or_none(**filter_by):
        raise NotImplementedError

    @staticmethod
    async def create(**values) -> None:
        async with async_session_maker() as session:
            query = insert(UserInventory).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update(id_, **values) -> None:
        async with async_session_maker() as session:
            query = update(UserInventory).filter_by(id=id_).values(**values)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def delete(**filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(UserInventory).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
