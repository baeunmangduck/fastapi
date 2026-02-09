from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from db.database import context_get_conn
from sqlalchemy import Connection
from services import auth_svc
from passlib.context import CryptContext


# router 생성
router = APIRouter(prefix="/auth", tags=["auth"])
# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str):
    return pwd_context.hash(password)


@router.get("/register")
async def register_user_ui(request: Request):
    return templates.TemplateResponse(
        request=request, name="register_user.html", context={}
    )


@router.post("/register")
async def register_user(
    name: str = Form(min_length=2, max_length=100),
    email: EmailStr = Form(...),
    password: str = Form(min_length=2, max_length=30),
    conn: Connection = Depends(context_get_conn),
):
    hashed_password = get_hashed_password(password)
    await auth_svc.register_user(
        conn=conn, name=name, email=email, hashed_password=hashed_password
    )
    return


@router.get("/login")
async def login_user_ui(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})
