from fastapi import FastAPI

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