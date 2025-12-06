from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/items/all", summary="전체 정보 가져오기", tags=["GET"])
async def root():
    
    '''
    간단한 API
    '''

    return {"msg": "Hello FastAPI!"}

@app.get("/items/{id}", summary="id에 따른 정보 가져오기", tags=["GET"])
async def read(id: int):
    return {"id": id}


@app.get("/users/{name}/age/{age}")
async def read_user_name_age(name: str, age: int):
    return {"name": name, "age": age}

@app.get("/users/")
async def read_user(name: str="mike", age: int=32):
    return {"name": name, "age": age}
