from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool


DB_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"


engine = create_engine(
    DB_CONN, echo=True, poolclass=QueuePool, pool_size=10, max_overflow=0
)


def direct_get_conn():
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e


@contextmanager
def context_get_conn():
    try:
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e:
        print(e)
        raise e
    finally:
        conn.close()
