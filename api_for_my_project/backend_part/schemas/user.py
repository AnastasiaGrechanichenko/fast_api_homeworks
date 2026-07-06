from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    login: str
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(...,ge=0, le=120)


class UserResponse(BaseModel):
    id: int
    login: str
    name: str
    age: int

class LogineSessionResponse(BaseModel):
    user_id: int
    secret: str