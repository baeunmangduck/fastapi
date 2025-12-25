from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool


DB_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"


engine = create_engine(
    DB_CONN, echo=True, poolclass=QueuePool, pool_size=10, max_overflow=0
)

print("--- Engine Created ---")


def execute_sleep():
    # with절을 사용하면 자동으로 connection이 반환됨
    with engine.connect() as conn:
        q = "select sleep(5)"
        result = conn.execute(text(q))
        result.close()
        # conn.close() -> with절을 사용하면 해당 메서드가 필요 없음


for idx in range(20):
    print("loop idx: ", idx)
    execute_sleep()


print("--- end of loop ---")
