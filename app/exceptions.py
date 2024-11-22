from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNameAlreadyTakenException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'this user name is already taken'


class UserEmailAlreadyTakenException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'this email address is already taken'


class UserInvalidCredentialsException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'invalid email or password'


class UserNotAuthenticatedException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'you are not logged in your account'


class InvalidTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'token expired or has invalid signature/format'
