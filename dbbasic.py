from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError


DB_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"


engine = create_engine(DB_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0)
print("engine created!")


try:
    conn = engine.connect()
    q = "select id, title from blog"
    stmt = text(q)
    result = conn.execute(stmt)

    rows = result.fetchall()
    print(rows)
    result.close()
except SQLAlchemyError as e:
    print(e)

finally:
    conn.close()
