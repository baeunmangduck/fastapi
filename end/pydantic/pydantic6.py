from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, Form, Path, Query
from schemas.item_schema import Item, user_form_parse

app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, q: str, item: Item | None = None):
    # async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item | None = None)
    return {"item_id": item_id, "q": q, "item": item}


@app.put("/items_json/{item_id}")
async def update_item_json(
    item_id: int = Path(..., gt=0),
    q: str = Query(None, max_length=50),
    q2: str = Query(None, min_length=3),
    item: Item = None,
):
    return {"item_id": item_id, "q": q, "q2": q2, "item": item}


@app.post("/items_form/{item_id}")
async def update_item_form(
    item_id: int = Path(..., gt=0, title="The id of the form"),
    q: str = Query(None, max_length=40),
    name: str = Form(..., min_length=2, max_length=40),
    desc: Annotated[str, Form(max_length=40)] = None,
    price: float = Form(..., ge=0),
    tax: Annotated[float, Form()] = None,
):
    return {
        "item_id": item_id,
        "q": q,
        "name": name,
        "desc": desc,
        "price": price,
        "tax": tax,
    }


@app.post("/items_form_01/{item_id}")
async def update_item_form_01(
    item_id: int = Path(..., gt=0, title="The id of the form"),
    q: str = Query(None, max_length=40),
    name: str = Form(..., min_length=2, max_length=40),
    desc: Annotated[str, Form(max_length=40)] = None,
    price: float = Form(..., ge=0),
    tax: Annotated[float, Form()] = None,
):
    try:
        item = Item(name=name, desc=desc, price=price, tax=tax)
        return {"item_id": item_id, "q": q, "item": item}
    except ValidationError as e:
        raise RequestValidationError(e.errors())


@app.post("/items_form_02/{item_id}")
async def update_item_form_02(
    item_id: int = Path(..., gt=0, title="The id of the form"),
    q: str = Query(None, max_length=40),
    item: Item = Depends(user_form_parse),
):
    return {"item_id": item_id, "q": q, "item": item}
