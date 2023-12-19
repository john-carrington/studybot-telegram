import aiosqlite
import datetime

from aiogram.types import Message
from modules.services.fetch_user_data import getUserSchedule, getUserToken
from modules.misc.settings import days_of_week, database_file
from modules.keyboards import authorization_menu


async def getSchedule(message: Message, login: str, password: str, date: str) -> str:
    if login is None:   
        return await message.edit_text('Чтобы получить расписание, небходимо авторизоваться.', reply_markup=authorization_menu)
    
    async with aiosqlite.connect(database_file) as data_base:
        await data_base.execute(f"UPDATE users_bot SET week_state = '{date}' WHERE id = {message.from_user.id}")
        await data_base.commit()
    
    schedule:list[str] = sorted(await getUserSchedule(await getUserToken(login, password), date))
    day_number:int = datetime.datetime.strptime(date, "%Y-%m-%d").weekday()
    day_of_week = f'<b>{date} {days_of_week[day_number].capitalize()}</b>\n'
    msg = ''
    
    for lesson in schedule:
        if lesson[0].split('T')[0] == date:
            msg += f'{lesson[1]} - {lesson[2]} | {lesson[3][0]} {"("+lesson[-1]+")" if lesson[-1] != None else ""}' + '\n'
    if not msg: 
        msg = f'На этот день у нас нет запланированных занятий.'

    return day_of_week + msg