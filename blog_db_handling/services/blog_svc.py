from typing import List
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import Connection, text
from schemas.blog_schema import Blog, BlogData
from sqlalchemy.exc import SQLAlchemyError
from util.util import truncate_text, newline_to_br


def get_all_blogs(conn: Connection) -> List:
    try:
        q = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog
            """
        result = conn.execute(text(q))
        all_blogs = [
            BlogData(
                id=row.id,
                title=row.title,
                author=row.author,
                content=truncate_text(row.content, 150),
                image_loc=row.image_loc,
                modified_dt=row.modified_dt,
            )
            for row in result
        ]
        result.close()
        return all_blogs

    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="알 수 없는 이유로 서비스 오류가 발생했습니다.",
        )


def get_blog_by_id(conn: Connection, id: int):
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
            content=newline_to_br(row.content),
            image_loc=row.image_loc,
            modified_dt=row.modified_dt,
        )
        result.close()
        return blog

    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )


def create_blog(conn: Connection, title: str, author: str, content: str):
    try:
        q = f"""
            INSERT INTO blog(title, author, content, modified_dt)
            VALUES (:title, :author, :content, now())
            """
        conn.execute(text(q), {"title": title, "author": author, "content": content})
        conn.commit()

    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 데이터가 제대로 전달되지 않았습니다.",
        )


def update_blog_ui(conn: Connection, id: int):
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

    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 데이터가 제대로 전달되지 않았습니다.",
        )


def update_blog(
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
