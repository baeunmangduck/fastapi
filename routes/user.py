from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/user", tags=["user"])


class Item(BaseModel):
    name: str
    desc: str = None
    price: float
    tax: float = None


@router.get("/")
async def read_users():
    return [{"username": "Rickle"}, {"username": "Martin"}]


@router.get("/me")
async def read_user_me():
    return {"username": "currentuser"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}
