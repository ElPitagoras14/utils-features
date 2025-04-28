from pydantic import BaseModel


class LoginInfo(BaseModel):
    email: str
    password: str


class CreateInfo(BaseModel):
    name: str
    email: str
    password: str
