from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing import Optional
from fastapi import FastAPI, Path, Query


app = FastAPI()


class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    desc: str = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    tax: float | None = None

    @model_validator(mode="after")
    def tax_n_price_validation(self):
        price = self.price
        tax = self.tax

        if tax > price:
            return ValueError("Tax must be less than price")

        return self


@app.put("/items/{item_id}")
async def update_item(item_id: int, q: str, item: Item | None = None):
    # async def update_item(item_id: int = Path(...), q: str = Query(...), item: Item | None = None)
    return {"item_id": item_id, "q": q, "item": item}


@app.put("/items_json/{item_id}")
async def update_item_json(
    item_id: int = Path(..., gt=0),
    q: str = Query(None, max_length=50),
    q2: str = Query(None, min_length=3),
    item: Item | None = None,
):
    return {"item_id": item_id, "q": q, "q2": q2, "item": item}
