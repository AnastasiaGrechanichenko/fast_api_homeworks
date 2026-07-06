from datetime import datetime
from typing import List

from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    book_id: int
    title: str
    author: str
    price: int
    old_price: int
    quantity: int
    discount_amount: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_sum: int
    total_discount: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
