from fastapi import FastAPI, HTTPException
from uvicorn import run
from pydantic import BaseModel,Field

app = FastAPI()


ITEMS = [

]

class Item(BaseModel):
    id: int
    name: str = Field(min_length=3)
    verbose_name:str = Field(min_length=8)

@app.get("/items")
async def get_all_items():
    return ITEMS

@app.get("/items/{item_id}")
async def get_item_by_id (
        item_id:int,
        verbose_name:bool = False
):
    for item in ITEMS:
        if item.id == item_id:
            if verbose_name and item.verbose_name:
                return Item(
                    id = item.id,
                    name= item.verbose_name,
                    verbose_name=item.verbose_name
                )
            return item
    raise HTTPException(
            status_code = 404,
            detail = "Item not found"
        )

@app.post ("/items")
async def create_new_item(item:Item):
    new_id = len(ITEMS)
    new_item = Item (
        id = new_id,
        name= item.name,
        verbose_name=item.verbose_name
    )
    ITEMS.append(new_item)
    return  new_item


if __name__ == '__main__':
    run(app)
