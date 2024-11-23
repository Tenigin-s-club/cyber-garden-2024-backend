from uuid import UUID

from asyncpg import connect
from fastapi import APIRouter, Depends, Response, status

from app.config import settings
from app.repositories.users import UsersRepository
from app.schemas.users import SLoginUser, SRegisterUser
from app.utils import (authenticate_user, check_fio_or_email_exists,
                       create_token, get_password_hash,
                       get_admin_token)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(response: Response, user: SLoginUser):
    user = await authenticate_user(user.email, user.password)
    return {'token': create_token(user.id, user.role_id)}


@router.get('/roles', status_code=status.HTTP_200_OK)
async def get_all_roles():
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    return {
        'roles': [dict(role)["name"] for role in await conn.fetch('SELECT * FROM roles')]
    }


@router.post('/employee', status_code=status.HTTP_201_CREATED)
async def add_employee(employee: SRegisterUser, access_token: str = Depends(get_admin_token)):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    role = await conn.fetch(f"SELECT * FROM roles WHERE name='{employee.role}'")
    await check_fio_or_email_exists(employee.fio, employee.email)
    new_user_id = await UsersRepository.create(
        fio=employee.fio,
        email=employee.email,
        position=employee.position,
        role_id=dict(role[0])["id"],
        password=get_password_hash(employee.password)
    )
    return {'id': new_user_id}


@router.put('/employee/{employee_id}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_user(employee_id: UUID, employee: SRegisterUser, access_token: str = Depends(get_admin_token)):
    conn = await connect(settings.POSTGRES_ASYNCPG_URL)
    role = await conn.fetch(f'SELECT * FROM roles WHERE name={employee.role_id}')
    await check_fio_or_email_exists(employee.fio, employee.email)
    await UsersRepository.update(
        id=employee_id,
        fio=employee.fio,
        email=employee.email,
        position=employee.position,
        role_id=dict(role[0])["id"],
        password=get_password_hash(employee.password)
    )


@router.delete('/employee/{employee_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(employee_id: UUID, access_token: str = Depends(get_admin_token)):
    await UsersRepository.delete(id=employee_id)
