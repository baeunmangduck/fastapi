from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_CONN = os.getenv("DB_CONN")


engine = create_engine(
    DATABASE_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0, pool_recycle=300
)


def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )


def context_get_conn():
    conn = None
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print("SQL Alchemy Error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="요청하신 서비스에서 잠시 내부적인 문제가 발생했습니다.",
        )
    finally:
        if conn:
            conn.close()
