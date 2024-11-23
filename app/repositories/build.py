from app.db.models import InventoryTypes, FurnitureTypes
from app.db.models.user_furniture import UserFurniture
from app.db.models.user_inventory import UserInventory
from app.repositories.base import BaseRepository
from app.schemas.build import SInventoryType, SFurnitureType


class InventoryTypesRepository(BaseRepository):
    model = InventoryTypes
    model_pydantic_schema = SInventoryType


class FurnitureTypesRepository(BaseRepository):
    model = FurnitureTypes
    model_pydantic_schema = SFurnitureType


class InventoryEmployeeRepository(BaseRepository):
    model = UserInventory
    model_pydantic_schema = None


class FurnitureEmployeeRepository(BaseRepository):
    model = UserFurniture
    model_pydantic_schema = None
