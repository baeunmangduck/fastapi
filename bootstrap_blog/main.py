from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# main.py 와 blog_svc.py에 templates가 중복 -> main.py에서 생성하고 blog_svc.py에서 import 하는 것 고려
templates = Jinja2Templates(directory="templates")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        request=request,
        name="http_error.html",
        context={
            "status_code": exc.status_code,
            "title_message": "불편을 드려 죄송합니다.",
            "detail": exc.detail,
        },
    )
