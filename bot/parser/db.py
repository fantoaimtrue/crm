import asyncpg
from config.set import settings

async def create_db_pool():
    return await asyncpg.create_pool(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )


async def create_tables():
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        """)

async def create_user(user_id: int, username: str, first_name: str, last_name: str):
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            """
            INSERT INTO users (user_id, username, first_name, last_name)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) DO NOTHING
            """,
            user_id, username, first_name, last_name
        )

async def get_user(user_id: int):
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        return await connection.fetchrow(
            """
            SELECT user_id, username, first_name, last_name
            FROM users
            WHERE user_id = $1
            """,
            user_id
        )

async def update_user(user_id: int, username: str, first_name: str, last_name: str):
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            """
            UPDATE users
            SET username = $2, first_name = $3, last_name = $4
            WHERE user_id = $1
            """,
            user_id, username, first_name, last_name
        )

async def delete_user(user_id: int):
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            """
            DELETE FROM users
            WHERE user_id = $1
            """,
            user_id
        )
