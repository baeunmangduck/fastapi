from sqlalchemy import text
from db.database import direct_get_conn, engine
import asyncio


async def execute_query():
    conn = await direct_get_conn()
    print(f"conn type: {type(conn)}")
    query = "select * from blog"
    statement = text(query)

    result = await conn.execute(statement)

    rows = result.fetchall()
    print(rows)
    await conn.rollback()
    await conn.close()
    await engine.dispose()


async def main():
    await execute_query()


if __name__ == "__main__":
    asyncio.run(main())
