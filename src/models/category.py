from pydantic import BaseModel, EmailStr, constr, ValidationError
from typing import Optional


class Category(BaseModel):
    id: int
    title: str
    color: str
    userId: int