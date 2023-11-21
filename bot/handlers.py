import math
import api

from aiogram import Router
from aiogram.types import Message, FSInputFile, InputFile, BufferedInputFile
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

router = Router()

''' =================== SOME EXTRA CLASSES ================================================== '''


@router.message(Command("start"))
async def start_handler(msg: Message):
    await send_main_menu(msg, msg.from_user.id)


''' =================== COMMANDS ============================================================ '''

''' =================== CALLBACK QUERY ====================================================== '''

''' =================== MESSAGE ============================================================= '''

''' =================== OTHER FUNCTIONS ===================================================== '''


async def send_main_menu(message, user_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [],
    ])
    await message.answer(
        text=f"Приветствую пользователь",
        reply_markup=markup,
        parse_mode="html"
    )
