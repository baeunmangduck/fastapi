from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None



@app.post("/items")
async def items(item: Item):
    print("type of item:\n", type(item))
    print("item:\n", item)
    return item


