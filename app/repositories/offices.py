from app.repositories.base import BaseRepository
from app.db.models import Office, Floor
from app.schemas.office import SOffice, SFloor


class OfficesRepository(BaseRepository):
    model = Office
    model_pydantic_schema = SOffice


class FloorsRepository(BaseRepository):
    model = Floor
    model_pydantic_schema = SFloor
            