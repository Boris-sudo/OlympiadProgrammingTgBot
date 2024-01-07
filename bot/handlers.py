from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputFile, BufferedInputFile
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

import math
import api

router = Router()

''' =================== SOME EXTRA CLASSES ================================================== '''

import bot.structure.classes as classes

''' =================== COMMANDS ============================================================ '''


@router.message(Command("start"))
async def start_handler(msg: Message):
    await send_main_menu(msg, msg.from_user.id)


@router.callback_query(F.data == "logIn")
async def log_in_function(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Введите номер вашего телефона',
    )
    await state.set_state(classes.LogInClass.choosing_phone)


@router.callback_query(F.data == "dailyProblem")
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    # TODO написать функцию, в которой будет отсылаться `dailyProblem`
    user_id = callback.message.from_user.id
    profile = await api.get_account(user_id)
    problem = await api.get_daily_problem(user_id, profile.rating)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{problem.name}', url=f'{problem.link}')]
    ])
    await callback.message.edit_text(
        text='',
        markup=markup,
    )


@router.callback_query(F.data == "archive")
async def show_archive_tasks(callback: CallbackQuery, state: FSMContext):
    # TODO сделать функцию, которая будет отправлять ещё задачи для игрока
    pass


@router.callback_query(F.data == "topics")
async def show_topics(callback: CallbackQuery, state: FSMContext):
    # TODO сдедать функцию, которая будет отправлять темы по олимпиадному программированию
    pass


@router.callback_query(F.data == "olympiads")
async def show_olympiads(callback: CallbackQuery, state: FSMContext):
    # TODO сделать функцию, которая будет отправлять информацию о олимпиадах, в которых можно поучаствовать программистам
    pass


''' =================== CALLBACK QUERY ====================================================== '''

''' =================== MESSAGE ============================================================= '''


@router.message(classes.LogInClass.choosing_phone)
async def phone_chosen(message: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Меню', callback_data='start')],
    ])
    user_data = await state.get_data()
    phone_number = message.text.lower()
    await api.send_phone_number(phone_number)
    # await state.update_data(id=send_phone_number(phone_number))
    await message.answer(
        text=f"Вы ввели номер телефона <code>{phone_number}</code>.\n"
             "Теперь, пожалуйста, введите код активации:",
        reply_markup=markup
    )
    await state.set_state(classes.LogInClass.choosing_activation_code)


@router.message(classes.LogInClass.choosing_activation_code)
async def code_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    text = message.text.splitlines()
    code = text[0].replace(" ", "")
    password = text[1] if len(text) >= 2 else None
    user_id = user_data['id']
    api.validate_code(user_id, code, password)

    await message.answer(
        text="Регистрация прошла успешно",
    )
    await state.clear()
    await send_main_menu(message, message.from_user.id)


''' =================== OTHER FUNCTIONS ===================================================== '''


async def send_main_menu(message, user_id):
    try:
        account = api.get_account(user_id)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Ежедневная задача', callback_data='dailyProblem')],
            [InlineKeyboardButton(text='Ещё задач', callback_data='archive'),
             InlineKeyboardMarkup(text='Темы', callback_data='topics')],
            [InlineKeyboardButton(text='Олимпиады', callback_data='olympiads')],
        ])
        await message.answer(
            text=f"Привет, {message.from_user.first_name}. Что хочешь посмотреть сегодня?",
            reply_markup=markup,
            parse_mode="html"
        )
    except Exception as exc:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Зарегистрироваться', callback_data='logIn')],
        ])
        await message.answer(
            text=f"Зарегистрируйтесь, чтобы исопльзовать функционал бота.",
            reply_markup=markup,
            parse_mode="html"
        )
