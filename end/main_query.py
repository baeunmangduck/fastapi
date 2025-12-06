from fastapi import FastAPI
from typing import Optional

app = FastAPI()

items_db = [{"item_name": "hello"}, {"item_name": "my name is"}, {"item_name": "eunbae"}]

@app.get("/items")
# default 값이 있을 경우 쿼리 파라미터 값을 넣지 않아도 됨
async def read_item(skip: int = 0, limit: int = 2):
    return items_db[skip: skip + limit]

@app.get("/items_must/")
# default 값이 없을 경우 반드시 인자에 해당하는 쿼리 파라미터 값을 넣어야 함
# Pydantic의 검증 오류에 걸림
async def read_item_must(skip: int, limit: int):
    return items_db[skip: skip + limit]



@app.get("/items_option/")
# Optional로 타입 힌트를 해줘도 default 값이나 실제 값을 넣어줘야 함
async def read_item_optional(skip: int, limit: Optional[int] = None):
    # return items_db[skip: skip + limit]
    if limit:
        return items_db[skip: skip + limit]
    else:
        return {"limit not provided"}
    

@app.get("/items/{item_id}")
# Optional을 다르게 표현하는 법 | None = None
async def read_item_optional(item_id: str, q: str | None = None):
    # return items_db[skip: skip + limit]
    if q:
        return {"item_id": item_id, "q": q}
    else:
        return {"item_id": item_id}