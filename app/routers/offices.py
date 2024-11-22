from fastapi import APIRouter, status
from typing import Literal

from app.schemas.office import SCreateOffice, SCreateFloor

router = APIRouter(
    prefix="/offices",
    tags=["Offices"]
)


@router.get("/offices")
async def get_offices():
    return [
    {
        "id": 1,
        "name": "WTF Office",
        "address": "sosay kudasay"
    },
    {
        "id": 3,
        "name": "WTF Office",
        "address": "sosay kudasay 2"
    },
    {
        "id": 2,
        "name": "WTF Off",
        "address": "sosay kudasay 3"
    }
]
    
    
@router.get("/floors/{office_id}")
async def get_floors(office_id: int):
    return [
    {
        "id": 5,
        "name": "Conchenoy"
    },
    {
        "id": 7,
        "name": "Conchenoy v rot"
    },
    {
        "id": 10,
        "name": "Conchenoy v shopa"
    }
]
    
    
@router.get("/employees/{office_id}")
async def get_employees(office_id):
    return [
    {
        "id": "790a838d-b21f-43d1-88f6-aac6da213ae5",
        "fio": "Piradasov Huesos Eblanovich",
        "position": "huesos developer",
        "place": 15,
        "email":"huesos@mail.ru",
        # то, что на столе
        "inventory": [{
            "id": 1,
            "name": "palka ebalka"
        },
                      {
            "id": 8,
            "name": "palka ebalka v1"
        },
                      {
            "id": 7,
            "name": "palka ebalka 2.0"
        }
                      ]
    },
        {
        "id": "790a838d-b21f-43d1-88f6-aac6da213ae5",
        "fio": "Koras Korsr Elizovetovich",
        "position": "huesos developer 2.0",
        "place": 19,
        "email":"huesos@mail.ru",
        # то, что на столе
        "inventory": [{
            "id": 1,
            "name": "palka ebalka no ne eblaka 1"
        },
                      {
            "id": 8,
            "name": "palka ebalka no ne eblaka 2"
        },
                      {
            "id": 7,
            "name": "palka ebalka no ne eblaka 3"
        }
                      ]
    },
        {
        "id": "790a838d-b21f-43d1-88f6-aac6da213ae5",
        "fio": "Koras Korsr Huyglotanovich",
        "position": "huesos developer 2.0",
        "place": 20,
        "email":"huesos@mail.ru",
        # то, что на столе
        "inventory": [{
            "id": 5,
            "name": "palka ebalka no ne eblaka no ebalka 1"
        },
                      {
            "id": 2,
            "name": "palka ebalka no ne eblaka no ebalka 2"
        },
                      {
            "id": 77,
            "name": "palka ebalka no ne eblaka no ebalka  3"
        }
                      ]
    }
]
    
    
@router.get("/map/{office_id}/{floor_id}")
async def get_map(
    office_id: int, 
    floor_id: int
):
    return [
    {
        "id": 12,
        "type": 15,
        "x": 17,
        "y": 21,
        "is_vertical": True
    },
    {
            "id": 89,
        "type": 12,
        "x": 27,
        "y": 31,
        "is_vertical": False
    },
        {
        "id": 189,
        "type": 212,
        "x": 237,
        "y": 331,
        "is_vertical": False
    }
]
   
 
@router.get("/inventory/{office_id}")  
async def get_inventory_in_office(office_id: int):
    return [
    {
        "id": 1,
        "name": "govno-mac",
        "fio": "Piradasov Huesos Eblanovich"
    },
        {
        "id": 1,
        "name": "govno-mac",
        "fio": "Piradasov Huesos Eblanovich"
    }
]
    

@router.post("/office", status_code=status.HTTP_201_CREATED)
async def create_office(office: SCreateOffice):
    return {
    "id": 2
}
    
    
@router.post("floor", status_code=status.HTTP_201_CREATED)
async def create_floor(floor: SCreateFloor):
    return {
    "id": 8
}
    
    
@router.put("/office/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_office(
    office_id: int, 
    office: SCreateOffice
):
    pass


@router.put("/floor/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_floor(
    floor_id: int,
    floor: SCreateFloor
):
    pass


@router.delete("/office/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_office(office_id) -> None:
    pass


@router.delete("/floor/{office_id}/{floor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_floor(
    office_id: int,
    floor_id: int
) -> None:
    pass
