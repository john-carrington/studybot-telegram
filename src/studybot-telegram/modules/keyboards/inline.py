from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


authorization_menu = InlineKeyboardMarkup(row_width=1)\
    .add(
        InlineKeyboardButton(text="Авторизоваться", callback_data="auth"),
        InlineKeyboardButton(text="Продолжить без авторизации", callback_data="without_auth")
        )


week_schedule_menu = InlineKeyboardMarkup(row_width=2)\
    .add(
        InlineKeyboardButton(text="⬅️", callback_data="week_day_past"),
        InlineKeyboardButton(text="➡️", callback_data="week_day_next"),
        )

news_buttons_menu = InlineKeyboardMarkup(row_width=2)\
    .add(
        InlineKeyboardButton(text="⬅️", callback_data="news_past"),
        InlineKeyboardButton(text="➡️", callback_data="news_next"),
        )


settings_buttons = [
    InlineKeyboardButton(text="📄FAQ", callback_data="faq"),
    InlineKeyboardButton(text="👤Поддержка", callback_data="support"),
    InlineKeyboardButton(text="🚪Выйти с аккаунта", callback_data="logout_from_account"),
]

