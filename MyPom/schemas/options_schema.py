from pydantic import BaseModel


class UpdateFocus(BaseModel):
    focus: int
