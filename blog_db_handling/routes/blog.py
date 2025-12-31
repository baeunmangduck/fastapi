from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy import Connection, text
from db.database import context_get_conn, direct_get_conn
from schemas.blog_schema import Blog, BlogData
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.get("/")
async def get_all_blogs(request: Request):
    conn = None
    try:
        conn = direct_get_conn()
        q = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog
            """
        result = conn.execute(text(q))
        rows = [
            BlogData(
                id=row.id,
                title=row.title,
                author=row.author,
                content=row.content,
                image_loc=row.image_loc,
                modified_dt=row.modified_dt,
            )
            for row in result
        ]
        result.close()
        return rows
    except SQLAlchemyError as e:
        print(e)
        raise e

    finally:
        if conn:
            conn.close()


@router.get("/show/{id}")
def get_blog_by_id(
    request: Request, id: int, conn: Connection = Depends(context_get_conn)
):
    try:
        q = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog 
            where id = :id
            """

        statement = text(q)

        result = conn.execute(statement, {"id": id})
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 ID {id}는(은) 존재하지 않음",
            )

        row = result.fetchone()
        blog = BlogData(
            id=row.id,
            title=row.title,
            author=row.author,
            content=row.content,
            image_loc=row.image_loc,
            modified_dt=row.modified_dt,
        )

        result.close()
        return blog
    except SQLAlchemyError as e:
        print(e)
        raise e
