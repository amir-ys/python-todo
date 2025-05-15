from pydantic import BaseModel, EmailStr, constr, ValidationError
from typing import Optional


class Task(BaseModel):
    id: int
    title: str
    body: str
    category_id: int
    user_id: int
