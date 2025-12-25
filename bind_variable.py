from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn
from datetime import datetime

try:
    conn = direct_get_conn()

    q = "select id, title from blog where id= :id and author= :author \
        and modified_dt < :modified_dt"

    statement = text(q)

    result = conn.execute(
        statement, {"id": 1, "author": "둘리", "modified_dt": datetime.now()}
    )
    rows = result.fetchall()
    print(rows)
    result.close()

except SQLAlchemyError as e:
    print(" ########### ", e)

finally:
    conn.close()
