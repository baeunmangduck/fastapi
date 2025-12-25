from database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError


def execute_query(conn: Connection):
    q = "select * from blog"
    statement = text(q)
    result = conn.execute(statement)

    rows = result.fetchall()
    print(rows)
    result.close()


def execute_sleep(conn: Connection):
    q = "select sleep(5)"
    statement = text(q)
    result = conn.execute(statement)
    result.close()


for idx in range(20):
    try:
        with context_get_conn() as conn:
            execute_sleep(conn)
            print("loop idx: ", idx)
    except SQLAlchemyError as e:
        print(e)
    finally:
        # conn.close()
        # print("connection is closed finally")
        pass

print("end of loop")
