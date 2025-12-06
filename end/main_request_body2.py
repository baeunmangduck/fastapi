from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    desc: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

# json의 각 요소의 키와 함수의 인자와 동일해야 함 (ex: item, user)
# {
#     "item": {
#         "name": "Eunbae",
#         "desc": "Student",
#         "price": 32,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "baeeun",
#         "full_name": "baeeunmangduck"
#     }
# }
@app.put("/items_multi/{item_id}")
async def update_item_multi(item_id: int, item: Item, user: User, q: str | None = None):
    result = {"item_id": item_id, "item": item, "user": user}
    if q:
        result = {"item_id": item_id, "item": item, "user": user, "q": q}
    return result