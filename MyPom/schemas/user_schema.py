from pydantic import BaseModel


class UserModel(BaseModel):
    username: str = "test"
    email: str = "test@email.com"
    password: str = "test"


class CurrentUser(BaseModel):
    username: str
    email: str
    focus: int
