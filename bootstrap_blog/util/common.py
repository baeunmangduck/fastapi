from contextlib import asynccontextmanager
from db.database import engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up....")
    yield

    print("shutting down...")
    await engine.dispose()
