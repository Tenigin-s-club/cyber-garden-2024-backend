from datetime import datetime, timedelta, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Header, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.exceptions import (UserInvalidCredentialsException,
                            UserNameAlreadyTakenException, InvalidTokenException, UserNotAuthenticatedException,
                            UserEmailAlreadyTakenException, DontHavePermissionException)
from app.repositories.users import UsersRepository
from app.schemas.users import SUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
expiration_time = timedelta(hours=3)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_id_and_role_from_token(token: str) -> tuple[UUID, str]:
    return (
        jwt.decode(token, settings.SECRET_KEY, settings.ENCODE_ALGORITHM).get('sub'),
        jwt.decode(token, settings.SECRET_KEY, settings.ENCODE_ALGORITHM).get('role')
    )


async def check_fio_or_email_exists(fio: str, email: EmailStr) -> None:
    if await UsersRepository.find_one_or_none(fio=fio):
        raise UserNameAlreadyTakenException
    if await UsersRepository.find_one_or_none(email=email):
        raise UserEmailAlreadyTakenException


def create_token(user_id: UUID, user_role_id: int) -> str:
    expire = datetime.now(timezone.utc) + expiration_time
    payload = {'exp': expire, 'sub': str(user_id), 'role_id': user_role_id}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, settings.ENCODE_ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> SUser:
    user = await UsersRepository.find_one_or_none(email=email)
    if not (user and verify_password(password, user.password)):
        raise UserInvalidCredentialsException
    return user


def check_token(token: str, check_admin: bool = False) -> None:
    if not token:
        raise UserNotAuthenticatedException
    try:
        role_id = jwt.decode(token, settings.SECRET_KEY, settings.ENCODE_ALGORITHM).get('role_id')
        if check_admin and role_id != 0:
            raise DontHavePermissionException
    except jwt.exceptions.DecodeError:
        raise InvalidTokenException


def get_admin_token(authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    check_token(authorization.credentials, check_admin=True)
    return authorization.credentials


def check_endpoint_permissions(request: Request, authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    if request.method == 'GET': return
    check_token(authorization.credentials, check_admin=True)
