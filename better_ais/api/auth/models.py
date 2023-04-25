from pydantic import BaseModel

class Login(BaseModel):
    login: str
    password: str

class TokenPair(BaseModel):
    access: str
    refresh: str
