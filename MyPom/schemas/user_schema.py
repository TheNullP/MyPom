from pydantic import BaseModel


class UserModel(BaseModel):
    username: str = "test"
    email: str = "test@email.com"
    password: str = "test"
