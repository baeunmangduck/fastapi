from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes import blog
from db.database import engine
from util import exc_handler, middleware
from util.common import lifespan

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.add_middleware(middleware_class=middleware.DummyMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=-1,
)
app.add_middleware(middleware_class=middleware.MethodOverrideMiddleware)


app.include_router(blog.router)


app.add_exception_handler(
    StarletteHTTPException, exc_handler.custom_http_exception_handler
)

app.add_exception_handler(
    RequestValidationError, exc_handler.validation_exception_handler
)
