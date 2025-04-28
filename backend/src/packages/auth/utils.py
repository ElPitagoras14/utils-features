from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from .config import auth_settings
from .responses import Token

SECRET_KEY = auth_settings.SECRET
ALGORITHM = auth_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = auth_settings.EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


fake_users_db = {
    "test@test.com": {
        "email": "test@test.com",
        "name": "Test User",
        "hashed_password": get_password_hash("test"),
    }
}


def authenticate_user(email: str, password: str):
    user = fake_users_db.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(
        token=token,
        type="bearer",
    )
