from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


main_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)\
    .add(
        "🗓Расписание", 
        '🤖Спросить у ИИ', 
        KeyboardButton('🧭Навигация', web_app=WebAppInfo(url='https://how-to-navigate.ru')), 
        '📰Новости', 
        '⚙️Настройки')
    
    
cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add('↪️Назад')