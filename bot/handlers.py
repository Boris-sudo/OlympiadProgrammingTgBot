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


class ChangeRating(CallbackData, prefix="ChangeRating"):
    rating: int


class MoveInProblemset(CallbackData, prefix="MoveInProblemset"):
    last_index: int
    rating: int


''' =================== COMMANDS ============================================================ '''


@router.message(Command("start"))  # /start command with MESSAGE
async def start_handler(msg: Message):
    await send_main_menu(msg, msg.from_user.id)


@router.message(Command("start"))  # /start command with CALLBACK
async def start_handler2(callback: CallbackQuery):
    await send_main_menu(callback, callback.from_user.id)


''' =================== CALLBACK QUERY ====================================================== '''


@router.callback_query(F.data == "logIn")  # login function
async def log_in_function(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Введите номер вашего телефона',
    )
    await state.set_state(classes.LogInClass.choosing_phone)


@router.callback_query(F.data == "dailyProblem")  # function sending daily problem
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    # TODO написать функцию, в которой будет отсылаться `dailyProblem`
    user_id = callback.message.from_user.id
    profile = api.get_account(user_id)
    problem = api.get_daily_problem(user_id, profile.rating)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Меню', callback_data=f'start')],
        [InlineKeyboardButton(text=f'{problem.name}', url=f'{problem.link}')]
    ])
    await callback.message.edit_text(
        text='',
        markup=markup,
    )


@router.callback_query(F.data == "archive")  # function sending all tasks for your rating
async def show_archive_tasks(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.from_user.id
    profile = api.get_account(user_id)

    await show_five_tasks(callback, 0, profile['rating'])


@router.callback_query(F.data == "topics")  # function sending all the theory
async def show_topics(callback: CallbackQuery, state: FSMContext):
    # TODO сдедать функцию, которая будет отправлять темы по олимпиадному программированию
    pass


@router.callback_query(F.data == "olympiads")  # function sending olympiads
async def show_olympiads(callback: CallbackQuery, state: FSMContext):
    # TODO сделать функцию, которая будет отправлять информацию о олимпиадах, в которых можно поучаствовать программистам
    pass


@router.callback_query(ChangeRating.filter(0 <= F.rating <= 3500))  # up the user rating
async def callback_foo8(callback: CallbackQuery, callback_data: ChangeRating):
    await show_five_tasks(callback, 0, callback_data.rating)


@router.callback_query(MoveInProblemset.filter(F.last_index >= 0))  # show other five tasks
async def callback_foo8(callback: CallbackQuery, callback_data: MoveInProblemset):
    await show_five_tasks(callback, callback_data.last_index, callback_data.rating)


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
        print(account)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Ежедневная задача', callback_data='dailyProblem')],
            [InlineKeyboardButton(text='Ещё задач', callback_data='archive')],
            [InlineKeyboardButton(text='Темы', callback_data='topics')],
            [InlineKeyboardButton(text='Олимпиады', callback_data='olympiads')],
        ])
        if type(message) == CallbackQuery:
            await message.message.answer(
                text=f"Привет, {message.from_user.first_name}. Что хочешь посмотреть сегодня?",
                reply_markup=markup,
                parse_mode="html"
            )
        else:
            await message.answer(
                text=f"Привет, {message.from_user.first_name}. Что хочешь посмотреть сегодня?",
                reply_markup=markup,
                parse_mode="html"
            )
    except Exception as exc:
        print(exc)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Зарегистрироваться', callback_data='logIn')],
        ])
        await message.answer(
            text=f"Зарегистрируйтесь, чтобы исопльзовать функционал бота.",
            reply_markup=markup,
            parse_mode="html"
        )


async def show_five_tasks(callback: CallbackQuery, last_index: int, rating: int):
    problemset = api.get_problemset(callback.from_user.id, rating)['result']
    current_problems = problemset[last_index: last_index]

    ''' CREATING MARKUP '''
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='⬆', callback_data=ChangeRating(rating=rating + 100).pack()),
            InlineKeyboardButton(text='change rating', callback_data='dummy function'),
            InlineKeyboardButton(text='⬇', callback_data=ChangeRating(rating=rating - 100).pack()),
        ],
    ])
    #  adding problems
    for problem in current_problems:
        markup.inline_keyboard.append([InlineKeyboardButton(
            text=f'{problem["name"]}',
            url=f'https://codeforces.com/problemset/problem/{problem["contestId"]}/{problem["index"]}',
        )])
    # adding navigation in problems buttons
    markup.inline_keyboard.append([])
    if last_index > 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='⬅', callback_data=MoveInProblemset(last_index=last_index - 5, rating=rating).pack()))
    else:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text=' ', callback_data='dummy function'))
    markup.inline_keyboard[-1].append(InlineKeyboardButton(text='move in problemset', callback_data='dummy function'))
    if last_index < len(problemset) - 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='➡', callback_data=MoveInProblemset(last_index=last_index + 5, rating=rating).pack()))
    else:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text=' ', callback_data='dummy function'))

    ''' FINALLY EDITING TEXT OF THE CALLBACK '''
    await callback.message.edit_text(
        text=f'Your current rating is: <code>{rating}</code>',
        reply_markup=markup,
        parse_mode="html",
    )
