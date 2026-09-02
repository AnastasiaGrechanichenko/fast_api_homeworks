from typing import Optional

from pydantic import BaseModel, Field,EmailStr


class CreateUser(BaseModel):
    login: str
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(...,ge=0, le=120)
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    login: str
    name: str
    age: int
    email: Optional[EmailStr]=None
    contact_number: Optional[str] = None

class LogineSessionResponse(BaseModel):
    user_id: int
    secret: str

class UpdateUser(BaseModel):
    email:Optional[EmailStr] = None
    name:Optional[str] = None
    age:Optional[int] = None
    contact_number: Optional[str] = None
