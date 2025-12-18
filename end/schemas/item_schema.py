from typing import Annotated

from fastapi import Form
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError, model_validator


class Item(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    desc: str = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    tax: float = Field(..., ge=0)

    @model_validator(mode="after")
    def tax_n_price_validation(self):
        price = self.price
        tax = self.tax

        if tax > price:
            return ValueError("Tax must be less than price")

        return self


def user_form_parse(
    name: str = Form(..., min_length=2, max_length=40),
    desc: Annotated[str, Form(max_length=400)] = None,
    price: float = Form(..., gt=0),
    tax: Annotated[float, Form()] = None,
) -> Item:
    try:
        item = Item(name=name, desc=desc, price=price, tax=tax)
        return item
    except ValidationError as e:
        raise RequestValidationError(e.errors())
