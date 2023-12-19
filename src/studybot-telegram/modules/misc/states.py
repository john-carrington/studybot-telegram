from aiogram.dispatcher.filters.state import State, StatesGroup

class UserInputState(StatesGroup):
    input_fullname = State()
    query_ai = State()

class UserAuthState(StatesGroup):
    auth_user_login = State()
    auth_user_password = State()
