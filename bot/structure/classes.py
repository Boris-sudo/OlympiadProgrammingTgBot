from aiogram.fsm.state import StatesGroup, State


class LogInClass(StatesGroup):
    username = State()
