from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from routes import blog
from db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting up....")
    yield

    print("shutting down...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(blog.router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "처리 중 에러가 발생하였습니다.",
            "detail": exc.detail,
            "code": exc.status_code,
        },
    )
