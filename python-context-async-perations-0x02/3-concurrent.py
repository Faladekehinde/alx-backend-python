import asyncio
import aiosqlite

# fetch all users
async def async_fetch_users():
    """Fetch all user from the databse"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users.await cursor.fetchall()
            print("All users:", users)
            return users

async def async_fetch_older_users():
    """ Fetch users older than 40"""
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            old_users.await cursor.fetchall()
            print("All users older than 40:", old_users)
            return old_users

async def fetch_concurrently():
    """ Run both queries at thesame time"""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# Run the queries
asyncio.run(fetch_concurrently())