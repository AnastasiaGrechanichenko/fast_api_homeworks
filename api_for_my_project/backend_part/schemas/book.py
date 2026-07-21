from pydantic import BaseModel


class CreateBook(BaseModel):
    title: str
    author: str
    price: int
    old_price: int
    image: str
    category: str
    description: str|None = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: int
    old_price: int
    image: str
    category: str
    description: str | None = None