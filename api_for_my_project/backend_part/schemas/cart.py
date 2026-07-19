from typing import List

from pydantic import BaseModel, Field, ConfigDict, computed_field


class CreateCartItem(BaseModel):
    book_id: int
    quantity: int = Field(default=1, ge=1, le=99)


class UpdateCartRequest(BaseModel):
    quantity: int = Field(..., ge=1, le=99)


class CartItemResponse(BaseModel):
    id: int
    book_id: int
    title: str
    author: str
    price: int
    old_price: int
    image: str
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

