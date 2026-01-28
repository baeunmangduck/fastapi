from typing import List
from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException
from sqlalchemy import Connection, text
from schemas.blog_schema import Blog, BlogData
from sqlalchemy.exc import SQLAlchemyError
from util import util
from dotenv import load_dotenv
import os
import time
import aiofiles as aio

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR")


async def get_all_blogs(conn: Connection) -> List:
    try:
        q = """
            SELECT id, title, author, content, 
            CASE WHEN image_loc IS NULL THEN '/static/default/blog_default.png' ELSE image_loc END as image_loc, 
            modified_dt FROM blog1
            """
        result = await conn.execute(text(q))

        all_blogs = [
            BlogData(
                id=row.id,
                title=row.title,
                author=row.author,
                content=util.truncate_text(row.content, 150),
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


async def get_blog_by_id(conn: Connection, id: int):
    try:
        q = """
            SELECT id, title, author, content, image_loc, modified_dt FROM blog 
            where id = :id
            """

        statement = text(q)

        result = await conn.execute(statement, {"id": id})
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
        if blog.image_loc is None:
            blog.image_loc = "/static/default/blog_default.png"
        result.close()
        return blog

    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )


async def upload_file(author: str, imagefile: UploadFile = None):
    try:
        user_dir = f"{UPLOAD_DIR}/{author}/"
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        filename_only, ext = os.path.splitext(imagefile.filename)
        upload_filename = f"{filename_only}_{(int)(time.time())}{ext}"
        upload_image_loc = user_dir + upload_filename

        async with aio.open(upload_image_loc, "wb") as outfile:
            while content := await imagefile.read(1024):
                await outfile.write(content)
        print("upload succeeded", upload_image_loc)

        return upload_image_loc[1:]

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="이미지 파일이 제대로 업로드되지 않았습니다.",
        )


async def create_blog(
    conn: Connection, title: str, author: str, content: str, image_loc=None
):
    try:
        q = f"""
            INSERT INTO blog(title, author, content, image_loc, modified_dt)
            VALUES (:title, :author, :content, :image_loc, now())
            """
        await conn.execute(
            text(q),
            {
                "title": title,
                "author": author,
                "content": content,
                "image_loc": image_loc,
            },
        )
        await conn.commit()

    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        await conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 데이터가 제대로 전달되지 않았습니다.",
        )


async def update_blog(
    conn: Connection,
    id: int,
    title: str,
    author: str,
    content: str,
    image_loc: str = None,
):

    try:
        q = f"""
            UPDATE blog
            SET title = :title, author = :author, content = :content, image_loc = :image_loc
            WHERE id = :id
            """
        statement = text(q)
        result = await conn.execute(
            statement,
            {
                "id": id,
                "title": title,
                "author": author,
                "content": content,
                "image_loc": image_loc,
            },
        )
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 id {id}가 존재하지 않음",
            )
        await conn.commit()

    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        await conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 데이터가 제대로 전달되지 않았습니다.",
        )


async def delete_blog(conn: Connection, id: int, image_loc: str = None):
    try:
        q = """
            DELETE FROM blog
            WHERE id = :id
            """
        statement = text(q)
        result = await conn.execute(statement, {"id": id})
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"해당 id {id}는 존재하지 않음",
            )
        await conn.commit()

        if image_loc is not None:
            image_path = "." + image_loc
            if os.path.exists(image_path):
                print("image path: ", image_path)

                os.remove(image_path)
    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        await conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="알 수 없는 이유로 문제가 발생했습니다.",
        )
