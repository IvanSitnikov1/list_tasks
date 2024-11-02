from pydantic import BaseModel


class SUserAdd(BaseModel):
    username: str
    password: str


class SUser(BaseModel):
    id: int
    username: str
    password_hash: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
