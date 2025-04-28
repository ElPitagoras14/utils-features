from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from .config import auth_settings

SECRET_KEY = auth_settings.SECRET
ALGORITHM = auth_settings.ALGORITHM


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if not credentials:
            raise HTTPException(
                status_code=401, detail="Authorization header missing"
            )
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authentication scheme"
            )
        return self.verify_jwt(credentials.credentials)

    def verify_jwt(self, token: str) -> dict:
        try:
            user = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return user
        except JWTError:
            raise HTTPException(
                status_code=401, detail="Sesión inválida o expirada."
            )


auth_scheme = JWTBearer()


def get_current_user(payload: str = Depends(auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if payload is None:
        raise credentials_exception
    return payload
