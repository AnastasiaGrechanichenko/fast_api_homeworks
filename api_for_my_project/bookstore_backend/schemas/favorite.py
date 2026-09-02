from pydantic import BaseModel, ConfigDict

class FavoriteResponse(BaseModel):
    id: int
    book_id:int
    title: str
    author: str
    price: int
    old_price:int
    image: str