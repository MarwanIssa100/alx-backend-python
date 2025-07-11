import asyncio
import aiosqlite

tsks = [async def async_fetch_users(db_path):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            return await cursor.fetchall()
        ,
async def async_fetch_older_users(db_path):
    async with aiosqlite.connect(db_path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users WHERE age > ?",(40,)) 
            return await cursor.fetchall()
]
async def fetch_concurrently():
    results = await asyncio.gather(*tsks)
    print(results)

asyncio.run(fetch_concurrently())