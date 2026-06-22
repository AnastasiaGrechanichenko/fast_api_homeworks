from pydantic import BaseModel,Field,ConfigDict,computed_field
from typing import List
class CreateUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(...,ge=0, le=120)
    password: str = Field(...,min_length=8)

class CreateBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    author: str
    price: int
    old_price: int
    image: str
    category: str

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    price: int
    old_price: int
    image: str
    category: str




class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    age: int

class CreateCartItem(BaseModel):
    book_id: int
    quantity: int = Field(default=1, ge=1, le=99)



class UpdateCartRequest(BaseModel):
    quantity: int = Field(..., ge=1, le=99)

class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
    title: str
    author: str
    price: int
    old_price: int
    quantity:int

    @computed_field
    @property
    def total_price(self) -> int:
        return self.price*self.quantity

    @computed_field
    @property
    def discount_amount(self)->int:
        return (self.old_price - self.price)* self.quantity

class CartResponse(BaseModel):
    items: List [CartItemResponse]

    @computed_field
    @property
    def total_sum(self) -> int:
        return sum(item.total_price for item in self.items)

    @computed_field
    @property
    def total_discount(self)-> int:
        return sum(item.discount_amount for item in self.items)




