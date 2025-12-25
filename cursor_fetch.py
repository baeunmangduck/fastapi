from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from database import direct_get_conn


try:
    conn = direct_get_conn()
    q = "select id, title from blog"
    statement = text(q)

    result = conn.execute(statement=statement)
    rows = result.fetchall()  # class list 반환
    # rows = result.fetchone() # class row 반환
    # rows = result.mappings().fetchall() # 딕셔너리로 반환, 메모리를 많이 소모
    # rows = [(row.id, row.title) for row in result]
    print(rows)
    print(type(rows))
    result.close()
except SQLAlchemyError as e:
    print(" ######## ", e)
    raise e

finally:
    conn.close()
