from fastapi import FastAPI
import asyncio
import time

app = FastAPI()


async def long_running_task():
    await asyncio.sleep(20)
    return {"status": "long_running task completed"}


@app.get("/task")
async def run_task():
    result = await long_running_task()
    return result


# @app.get("/task")
# async def run_task():
#     time.sleep(20)
#     return {"status": "long_running task completed"}


@app.get("/quick")
async def quick_response():
    return {"status": "quick response"}
