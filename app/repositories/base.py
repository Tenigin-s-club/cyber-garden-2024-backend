from abc import ABC, abstractmethod
from sqlalchemy import select, insert, update, delete
from typing import Union
from uuid import UUID

from app.db.base import async_session_maker


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    async def find_one_or_none(**filter_by):
        pass

    @staticmethod
    @abstractmethod
    async def find_all(**filter_by):
        pass

    @staticmethod
    @abstractmethod
    async def create(**values):
        pass

    @staticmethod
    @abstractmethod
    async def update(id_, **values):
        pass

    @staticmethod
    @abstractmethod
    async def delete(**filter_by):
        pass


class BaseRepository(AbstractRepository):
    model = None
    model_pydantic_schema = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Union[model_pydantic_schema, None]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().one_or_none()
            return cls.model_pydantic_schema(**mapping_result) if mapping_result else None

    @classmethod
    async def find_all(cls, **filter_by) -> list[model_pydantic_schema]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            mapping_result = result.mappings().all()
            return [cls.model_pydantic_schema(**elem) for elem in mapping_result] if mapping_result else None

    @classmethod
    async def create(cls, **values) -> Union[UUID, None]:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**values).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, id_, **values) -> Union[UUID, None]:
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(id=id_).values(**values).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def delete(cls, **filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
            
            
