from aiogram import Dispatcher
from modules.handlers.user.main import register_user

def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user,
    )
    for handler in handlers:
        handler(dp)