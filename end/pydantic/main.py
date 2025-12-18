from fastapi import FastAPI
from pydantic import BaseModel
from routes import item, user

app = FastAPI()

app.include_router(item.router)
app.include_router(user.router)
