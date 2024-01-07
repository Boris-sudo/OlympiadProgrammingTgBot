from aiogram.fsm.state import StatesGroup, State


class LogInClass(StatesGroup):
    choosing_phone = State()
    choosing_activation_code = State()
