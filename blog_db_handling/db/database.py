from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException


DB_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"

engine = create_engine(
    DB_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0, pool_recycle=300
)


def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e
