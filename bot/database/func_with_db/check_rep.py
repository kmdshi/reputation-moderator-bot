import aiosqlite as sq
from loader import db_path
from database.func_with_db.register_user import register

async def check_reputation(name):
    try:
        async with sq.connect(db_path) as db:
            cur = await db.cursor()
            
            await cur.execute("SELECT reputation FROM Users WHERE nick_name =?", (name,))
            reputation = await  cur.fetchone()
            
            if reputation:
                return reputation[0]
            else:    
                await register(name)
                return 50  
    except sq.Error as E:
        print(f'Error: {E}')
