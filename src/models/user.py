from pydantic import BaseModel, EmailStr, constr, ValidationError
from typing import Optional


class User(BaseModel):
    id: int
    email: EmailStr
    password: constr(min_length=6)
    name: Optional[str] = None