import aiosqlite
import datetime

from modules.misc.settings import database_file
from modules.services.user_encryption import decrypt_password


async def get_user_auth(message) -> tuple[str]:
     async with aiosqlite.connect(database_file) as data_base:
        cursor = await data_base.execute(f'SELECT login, password FROM users_bot WHERE id = {message.from_user.id}')
        login, password = await cursor.fetchone()
        if password: password = await decrypt_password(password)
        return login, password
    
    
async def get_current_week(message, position: int) -> str:
    async with aiosqlite.connect(database_file) as data_base:
        cursor = await data_base.execute(f"SELECT week_state FROM users_bot WHERE id = {message.from_user.id}")
        week_state = (await cursor.fetchone())[0]
        week = (datetime.datetime.strptime(week_state, '%Y-%m-%d') + (position * datetime.timedelta(days=1))).strftime("%Y-%m-%d")     
        return week