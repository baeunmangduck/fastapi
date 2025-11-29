from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from typing import Optional, Annotated


app = FastAPI()


@app.post("/login/")
async def login(
    username: str = Form(), email: str = Form(), country: Annotated[str, Form()] = None
):
    return {"username": username, "email": email, "country": country}


# Form(...)일 시 반드시 값 입력해야 하나, 위의 방식을 따르는게 정석
@app.post("/login_form/")
async def login(
    username: str = Form(...),
    email: str = Form(...),
    country: Annotated[str, Form()] = None,
):
    return {"username": username, "email": email, "country": country}


@app.get("/items")
async def read_item(request: Request):
    host = request.client.host
    headers = request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": host,
        "headers": headers,
        "query_params": query_params,
        "url": url,
        "path_params": path_params,
        "http_method": http_method,
    }


@app.get("/items/{item_group}")
async def read_item(request: Request, item_group: str):
    host = request.client.host
    headers = request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": host,
        "headers": headers,
        "query_params": query_params,
        "url": url,
        "path_params": path_params,
        "http_method": http_method,
    }

@app.post("/items_json/")
async def create_item_json(request: Request):
    data = await request.json()
    print("data:\n", data)
    return {"data": data}


@app.post("/items_form/")
async def create_item_json(request: Request):
    data = await request.form()
    print("data:\n", data)
    return {"data": data}