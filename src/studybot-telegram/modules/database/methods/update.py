
import aiosqlite

from modules.misc.settings import database_file
from modules.services.fetch_user_data import getUserToken
from modules.services.user_encryption import ecrypt_password
from aiogram.types import Message


async def add_user_in_database(message: Message, login=None, password=None) -> None:
    async with aiosqlite.connect(database_file) as data_base:
        await data_base.execute("""CREATE TABLE IF NOT EXISTS users_bot (
            id INTEGER PRIMARY KEY,
            username TEXT,
            week_state TEXT,
            news_state INTEGER,
            login TEXT,
            password TEXT)
        """)
        
        await data_base.execute(f"""INSERT OR IGNORE INTO users_bot(id, username) VALUES({message.from_user.id}, '{message.from_user.username}')""")
        await data_base.execute(f"""UPDATE users_bot SET username = '{message.from_user.username}' WHERE id = {message.from_user.id}""")
        if login and password:
            if await getUserToken(login.lower(), password):   
                password = await ecrypt_password(password)        
                await data_base.execute(f"UPDATE users_bot SET login = '{login.lower()}', password = '{password}' WHERE id = {message.from_user.id}")
                await message.answer('✅Авторизация прошла успешно!')
            else: 
                await message.answer('❌Неверный логин или пароль!')
                
        await data_base.commit()