from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection, text
from db.database import context_get_conn, direct_get_conn
from schemas.blog_schema import Blog, BlogData
from sqlalchemy.exc import SQLAlchemyError
from util.util import truncate_text, newline_to_br
from services import blog_svc

# router
router = APIRouter(prefix="/blogs", tags=["blogs"])

# jinja2 Template
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_all_blogs(request: Request, conn: Connection = Depends(context_get_conn)):
    conn = None
    all_blogs = blog_svc.get_all_blogs(conn)
    return templates.TemplateResponse(
        request=request, name="index.html", context={"all_blogs": all_blogs}
    )


@router.get("/show/{id}")
def get_blog_by_id(
    request: Request, id: int, conn: Connection = Depends(context_get_conn)
):
    blog = blog_svc.get_blog_by_id(conn, id)
    return templates.TemplateResponse(
        request=request, name="show_blog.html", context={"blog": blog}
    )


@router.get("/new")
def create_blog_ui(request: Request):
    return templates.TemplateResponse(request=request, name="new_blog.html", context={})


@router.post("/new")
def create_blog(
    request: Request,
    title=Form(min_length=2, max_length=100),
    author=Form(max_length=100),
    content=Form(min_length=2, max_length=4000),
    conn: Connection = Depends(context_get_conn),
):
    blog_svc.create_blog(conn, title=title, author=author, content=content)
    return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)


@router.get("/modify/{id}")
def update_blog_ui(
    request: Request, id: int, conn: Connection = Depends(context_get_conn)
):
    try:
        q = """
            SELECT id, title, author, content FROM blog WHERE id = :id
            """
        statement = text(q)
        result = conn.execute(statement, {"id": id})
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 id {id}가 존재하지 않음",
            )
        row = result.fetchone()
        return templates.TemplateResponse(
            request=request,
            name="modify_blog.html",
            context={
                "id": row.id,
                "title": row.title,
                "author": row.author,
                "content": row.content,
            },
        )
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 데이터가 제대로 전달되지 않았습니다.",
        )


@router.post("/modify/{id}")
def update_blog(
    request: Request,
    id: int,
    title=Form(min_length=2, max_length=100),
    author=Form(max_length=100),
    content=Form(min_length=2, max_length=4000),
    conn: Connection = Depends(context_get_conn),
):

    try:
        q = f"""
            UPDATE blog
            SET title = :title, author = :author, content = :content
            WHERE id = :id
            """
        statement = text(q)
        result = conn.execute(
            statement, {"id": id, "title": title, "author": author, "content": content}
        )
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 id {id}가 존재하지 않음",
            )
        conn.commit()
        return RedirectResponse(f"/blogs/show/{id}", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 데이터가 제대로 전달되지 않았습니다.",
        )


@router.post("/delete/{id}")
def delete_blog(
    request: Request, id: int, conn: Connection = Depends(context_get_conn)
):
    try:
        q = """
            DELETE FROM blog
            WHERE id = :id
            """
        statement = text(q)
        result = conn.execute(statement, {"id": id})
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 id {id}는 존재하지 않음",
            )
        conn.commit()
        return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )
