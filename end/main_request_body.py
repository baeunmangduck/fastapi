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
    #  <class 'main_request_body.Item'>
    print("item:\n", item)
    # name='eunbae' desc='Pydantic base model' price=30.41 tax=3.41
    return item

# request body 값 
# {
#   "name": "eunbae", # Required value
#   "desc": "Pydantic base model", # Optional value
#   "price": 30.41, # Required value
#   "tax": 3.41 # Optional value
# }

@app.post("/item_price_with_tax/")
async def create_item_price_with_tax(item:Item):
    # request body 값이 딕셔너리로 변환
    item_dict = item.model_dump()
    print("item_dict:\n", item_dict)

    # 딕셔너리로 변환된 item_dict 변수 업데이트
    # tax의 경우 옵션값인데 딕셔너리에서 None일 경우 JSON에서 null로 변환됨
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    # **item.model_dump() -> item.model_dump()로부터 반환된 딕셔너리의 key-value 쌍을 풀어서
    # 바깥 딕셔너리에 각각의 요소로 포함시키는 역할
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
