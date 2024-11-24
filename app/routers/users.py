from os.path import splitext
from uuid import UUID

import pandas as pd
import sqlalchemy.exc

from app.db.base import engine, sync_engine

from asyncpg import connect
from fastapi import APIRouter, Depends, Response, status, HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.exceptions import WrongFileExtensionException, IncorrectColumnsSetException
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
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    role = await conn.fetch(f"SELECT name FROM roles WHERE id='{user.role_id}'")
    return {'token': create_token(user.id, user.role_id), "role": role[0]["name"]}


@router.get('/roles', status_code=status.HTTP_200_OK)
async def get_all_roles():
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    return {
        'roles': [dict(role)["name"] for role in await conn.fetch('SELECT * FROM roles')]
    }


@router.post('/employee', status_code=status.HTTP_201_CREATED)
async def add_employee(employee: SRegisterUser, access_token: str = Depends(get_admin_token)):
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    role = await conn.fetch(f"SELECT * FROM roles WHERE name='{employee.role}'")
    await check_fio_or_email_exists(employee.fio, employee.email)
    new_user_id = await UsersRepository.create(
        fio=employee.fio,
        email=employee.email,
        position=employee.position,
        role_id=dict(role[0])["id"],
        password=get_password_hash(employee.password),
        office_id=employee.office_id,
        floor_id=employee.floor_id
    )
    return {'id': new_user_id}


@router.put('/employee/{employee_id}', status_code=status.HTTP_204_NO_CONTENT)
async def edit_user(employee_id: UUID, employee: SRegisterUser, access_token: str = Depends(get_admin_token)):
    conn = await connect(settings.POSTGRES_CLEAR_URL)
    role = await conn.fetch(f"SELECT * FROM roles WHERE name='{employee.role}'")
    try:
        await UsersRepository.update(
            id_=employee_id,
            fio=employee.fio,
            email=employee.email,
            position=employee.position,
            role_id=dict(role[0])["id"],
            password=get_password_hash(employee.password),
            office_id=employee.office_id,
            floor_id=employee.floor_id
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete('/employee/{employee_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(employee_id: UUID, access_token: str = Depends(get_admin_token)):
    await UsersRepository.delete(id=employee_id)


@router.post('/load_employees', status_code=status.HTTP_204_NO_CONTENT)
async def load_employees(file: UploadFile, access_token: str = Depends(get_admin_token)):
    _, file_extension = splitext(file.filename)
    if file_extension != '.xlsx':
        raise WrongFileExtensionException
    excel_data = pd.read_excel(file.filename)

    conn = await connect(settings.POSTGRES_CLEAR_URL)
    roles = {name: id for id, name in await conn.fetch('SELECT * FROM roles')}
    fios = [user["fio"] for user in await conn.fetch('SELECT * FROM users')]
    emails = [user["email"] for user in await conn.fetch('SELECT * FROM users')]

    data = pd.DataFrame(
        excel_data,
        columns=['fio', 'email', 'password', 'position', 'role']
    )
    data = data[~(data["fio"].isin(fios)) & ~(data["email"].isin(emails))]
    data['role_id'] = data['role'].map(roles)
    data = data.drop('role', axis='columns')

    try:
        data.to_sql('users', sync_engine, if_exists='append', index=False)
    except sqlalchemy.exc.IntegrityError as e:
        raise IncorrectColumnsSetException

