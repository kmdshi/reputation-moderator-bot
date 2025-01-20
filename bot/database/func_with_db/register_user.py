import aiosqlite as sq
from loader import db_path

async def register(name):
    try:
        async with sq.connect(db_path) as db:
            cur = await db.cursor()
            await cur.execute("SELECT nick_name FROM Users WHERE nick_name =?", (name,))
            nick_name = await cur.fetchone()
            if nick_name:
                pass
            else:
                await cur.execute("INSERT INTO Users (nick_name, reputation) VALUES (?, ?)", (name, 50))
                await db.commit()
    except sq.Error as E:
        print(f'Error: {E}')