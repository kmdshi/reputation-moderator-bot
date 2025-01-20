import aiosqlite as sq
from loader import db_path
from database.func_with_db.register_user import register

async def reverse_add_reputation(name, num=10):
    try:
        async with sq.connect(db_path) as db:
            cur = await db.cursor()
            
            await cur.execute("SELECT reputation FROM Users WHERE nick_name =?", (name,))
            reputation = await  cur.fetchone()

            if reputation:
                new_reputation = int(reputation[0]) - int(num)
                await cur.execute("UPDATE Users SET reputation = ? WHERE nick_name = ?", (new_reputation, name))
                await db.commit()
            else:
                await register(name)
    except sq.Error as E:
        print(f'Error: {E}')