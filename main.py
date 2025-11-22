from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="루트", tags=["test1"])
async def root():
    
    '''
    이것은 간단한 API입니다. 
    '''
    return {"msg": "Hello FastAPI!"}

@app.get("/items/{id}", tags=["test2"])
async def read(id: int):
    return {"id": id}


@app.get("/users/{name}/age/{age}")
async def read_user_name_age(name, age):
    return {"name": name, "age": age}

@app.get("/users/")
async def read_user(name="mike", age=32):
    return {"name": name, "age": age}
