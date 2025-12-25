from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool


DB_CONN = "mysql+mysqlconnector://root:root1234@localhost:3306/blog_db"


engine = create_engine(DB_CONN)
# pool에 생성되는 connection 개수가 최대 10개 -> pool_size / 만약 connection 반환을 하지 않을 시(is_close=False), 10개 생성된 후에 대기하다 에러
# pool_size에서 최대 한도로 추가될 수 있는 connection 개수 -> max_overflow
# engine = create_engine(DB_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0)

print("--- Engine Created ---")


def execute_sleep(is_close: bool = False):
    conn = engine.connect()
    q = "select sleep(5)"
    result = conn.execute(text(q))
    result.close()

    if is_close:
        # 만약 poolclass=NullPool(connection pool 미사용)이면 , 실제로 connection이 종료됨)
        # 만약 poolclass가 NullPool이 아니면 connection pool에 connection이 반환됨
        conn.close() 
        print("conn closed")


for idx in range(20):
    print("loop idx: ", idx)
    execute_sleep(is_close=True)  # connection close가 되어 반환된 connection 재사용
    # execute_sleep(is_close=False) # connection close가 되어 반환되지 않아, connection이 계속 만들어짐

print("--- end of loop ---")
