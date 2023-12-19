import datetime
import aiosqlite

from aiogram.types import Message
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from modules.misc.states import UserAuthState, UserInputState
from modules.database.methods.update import add_user_in_database
from modules.database.methods.get import get_current_week, get_user_auth
from modules.services.fetch_user_data import getUniversityNews, getUser
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from modules.services.chatbot import ChatBot
from modules.services.schedule import getSchedule
from modules.misc.settings import database_file, faq_info
from modules.misc.throttling import rate_limit
from modules.keyboards import *

chatBot = ChatBot()
chatBot.build_vectors()


async def send_hello_message(message: Message):
    await message.answer(f'😼<b>Добро пожаловать,</b> {message.from_user.first_name}!', reply_markup=main_menu)
    
@rate_limit(2)
async def start_handler(message: Message):
    await add_user_in_database(message)
    await message.answer_sticker(r"CAACAgIAAxkBAAEJzRdkvqTADptpHH-bHivHiQzi8GjKhgACAQEAAladvQoivp8OuMLmNC8E")
    await send_hello_message(message)
    
@rate_limit(2)   
async def answer_user(message: Message):
    await message.delete()
    try:
        login, password = await get_user_auth(message)
    except:
        await add_user_in_database(message)
    load_message = await message.answer('⌛')
    match message.text:
        case '🗓Расписание':
            if login is None:   
                await load_message.edit_text('Чтобы получить расписание, небходимо авторизоваться.', reply_markup=authorization_menu)
            else:
                await load_message.edit_text(await getSchedule(message, login, password, datetime.date.today().strftime("%Y-%m-%d")), reply_markup=week_schedule_menu)
                     
        case '🤖Спросить у ИИ':
            await load_message.delete()
            await message.answer('Чем могу помочь?', reply_markup=cancel_menu)
            await UserInputState.query_ai.set()
            
        case '⚙️Настройки':
            settings_menu = InlineKeyboardMarkup(row_width=1)
            await load_message.edit_text('⚙️Настройки', reply_markup=settings_menu.add(*(settings_buttons if login else settings_buttons[:-1])))
            
        case '📰Новости':
            async with aiosqlite.connect(database_file) as data_base:
                await data_base.execute(f"UPDATE users_bot SET news_state = 0 WHERE id = {message.from_user.id}")
                await data_base.commit()
            await load_message.edit_text(await getUniversityNews(), reply_markup=news_buttons_menu)
            
        case _:
            await load_message.delete()
            await message.answer('Я Вас не понимаю', reply_markup=main_menu)
            
        
async def state_input_user_fullname(message: Message, state: FSMContext): 
    await message.delete()
    msg = (await state.get_data())['msg']
    await msg.edit_text('⌛')
    await msg.edit_text(await getUser(message.text, datetime.date.today().strftime("%Y-%m-%d")))
    await state.reset_data()
    await state.finish()
    
    
async def state_input_query_ai(message: Message, state: FSMContext): 
    load_message = await message.answer('⌛')
    if message.text == '↪️Назад': 
        await load_message.delete()
        await message.answer('Вы вышли из диалога', reply_markup=main_menu)
        await state.finish()
    else: await load_message.edit_text(await chatBot.query(message.text))
    
    
async def state_input_user_login(message: Message, state: FSMContext): 
    await message.delete()
    msg = (await state.get_data())['msg']
    await msg.edit_text('Введите пароль:')
    await state.update_data(login = message.text)
    await UserAuthState.next()
    
async def state_input_user_password(message: Message, state: FSMContext): 
    await state.update_data(password = message.text)
    await message.delete()
    msg = (await state.get_data())['msg']
    await msg.delete()
   
    user_data = await state.get_data()
    await add_user_in_database(message, user_data['login'], user_data['password'])
    await state.reset_data()
    await state.finish()
    

async def user_callback_query_handler(call: CallbackQuery, state: FSMContext):
    login, password = await get_user_auth(call)
    
    match call.data:
        case 'auth':
            await state.update_data(msg=await call.message.edit_text('Введите логин:'))
            await UserAuthState.auth_user_login.set()
            
        case 'week_day_next':
            current_week = await get_current_week(call, 1)
            await call.message.edit_text(await getSchedule(call, login, password, current_week), reply_markup=week_schedule_menu)
            
        case 'week_day_past':
            current_week = await get_current_week(call, -1)
            await call.message.edit_text(await getSchedule(call, login, password, current_week), reply_markup=week_schedule_menu)
        
        case 'without_auth':
            
            await state.update_data(msg=await call.message.edit_text('Введите ФИО: '))
            await UserInputState.input_fullname.set()
            
        case 'logout_from_account':
            async with aiosqlite.connect(database_file) as data_base:
                await data_base.execute(f"""UPDATE users_bot SET login = NULL, password = NULL WHERE id = {call.from_user.id}""")
                await data_base.commit()
            await call.message.edit_text('✅Вы успешно вышли с аккаунта!')
            
        case 'news_next':
            async with aiosqlite.connect(database_file) as data_base:
                cursor = await data_base.execute(f'SELECT news_state FROM users_bot WHERE id = {call.from_user.id}')
                interval = int((await cursor.fetchone())[0]) + 1
                await data_base.execute(f'UPDATE users_bot SET news_state = {interval} WHERE id = {call.from_user.id}')
                await data_base.commit()
            await call.message.edit_text(await getUniversityNews(interval=interval), reply_markup=news_buttons_menu)
        
        case 'news_past':
            async with aiosqlite.connect(database_file) as data_base:
                cursor = await data_base.execute(f'SELECT news_state FROM users_bot WHERE id = {call.from_user.id}')
                interval = int((await cursor.fetchone())[0]) - 1
                await data_base.execute(f'UPDATE users_bot SET news_state = {interval} WHERE id = {call.from_user.id}')
                await data_base.commit()
            await call.message.edit_text(await getUniversityNews(interval=interval), reply_markup=news_buttons_menu)
            
        case 'faq':
            await call.message.edit_text(faq_info)
            
        case 'support':
            await call.message.edit_text('⚒ Раздел в разработке')    
    
    
def register_user(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_callback_query_handler(user_callback_query_handler)
    dp.register_message_handler(state_input_user_password, state=UserAuthState.auth_user_password)
    dp.register_message_handler(state_input_user_login, state=UserAuthState.auth_user_login)
    dp.register_message_handler(state_input_query_ai, state=UserInputState.query_ai)
    dp.register_message_handler(state_input_user_fullname, state=UserInputState.input_fullname)
    dp.register_message_handler(answer_user, content_types=['text'])
    
    
    