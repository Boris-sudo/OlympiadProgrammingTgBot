import time
import typing

from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, InputFile, BufferedInputFile
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from PIL import Image

import math
import api

import bot.structure.classes as classes
import bot.structure.tools as tools

router = Router()

''' =================== SOME EXTRA CLASSES ================================================== '''


class ChangeRating(CallbackData, prefix="ChangeRating"):
    rating: int


class MoveInProblemset(CallbackData, prefix="MoveInProblemset"):
    last_index: int
    rating: int


class MoveInOlympiads(CallbackData, prefix="MoveInOlympiads"):
    last_index: int


class MoveInTopicsArchive(CallbackData, prefix="MoveInTopicsArchive"):
    last_index: int


class ShowTopics(CallbackData, prefix="ShowTopics"):
    index: int
    last_index_in_archive: int


class MoveInTopic(CallbackData, prefix="MoveInTopic"):
    index: int
    last_index: int
    last_index_in_archive: int


class MoveBackToTopicsArchive(CallbackData, prefix="MoveBackToTopicsArchive"):
    last_index: int


class Registration(CallbackData, prefix="Registration"):
    username: str


''' =================== COMMANDS ============================================================ '''


@router.message(Command("start"))  # /start command with MESSAGE
async def start_handler(msg: Message):
    await send_main_menu(msg, msg.from_user.id)


@router.message(Command("start"))  # /start command with CALLBACK
async def start_handler2(callback: CallbackQuery):
    await send_main_menu(callback, callback.from_user.id)


''' =================== CALLBACK QUERY ====================================================== '''


@router.callback_query(F.data == "start")  # start function
async def log_in_function(callback: CallbackQuery, state: FSMContext):
    await send_main_menu(callback, callback.from_user.id)


@router.callback_query(F.data == "register")  # registration function
async def log_in_function(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Please type your codeforces username",
    )
    await state.set_state(classes.LogInClass.username)


@router.callback_query(F.data == "dailyProblem")  # function sending daily problem
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    # TODO написать функцию, в которой будет отсылаться `dailyProblem`
    user_id = callback.from_user.id
    print(user_id)
    problem = api.get_daily_problem(user_id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'Menu', callback_data=f'start')],
        [InlineKeyboardButton(
            text=f'{problem["name"]}',
            url=f'https://codeforces.com/problemset/problem/{problem["contestId"]}/{problem["index"]}'
        )]
    ])
    await callback.message.edit_text(
        text=f'Here is your daily problem\nrating: <code>{problem["rating"]}</code>.',
        reply_markup=markup,
        parse_mode='html',
    )


@router.callback_query(F.data == "archive")  # function sending all tasks for your rating
async def show_archive_tasks(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    profile = api.get_account(user_id)

    await show_five_tasks(callback, 0, profile['rating'])


@router.callback_query(F.data == "topics")  # function sending all the theory
async def show_topics(callback: CallbackQuery, state: FSMContext):
    await show_five_topics_archives(callback, 0)


@router.callback_query(F.data == "olympiads")  # function sending olympiads
async def show_olympiads(callback: CallbackQuery, state: FSMContext):
    await show_five_olympiads(callback, 0)


@router.callback_query(F.data == "profile")  # function sending profile
async def show_profile(callback: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='menu', callback_data='start')]])
    account = api.get_account(callback.from_user.id)
    filename = tools.generate_filename()
    filepath = f'static/generated/{filename}.png'
    tools.generate_rating_diagram(account['rating_changes'], filepath)
    img = FSInputFile(filepath)
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=img,
        caption=f"Your profile rating is: <code>{account['rating']}</code>\n"
                f"Your profile codeforces username is: <code>{account['username']}</code>",
        reply_markup=markup,
        parse_mode='html',
    )


@router.callback_query(F.data == "pvp-mod")
async def show_pvp_mod(callback: CallbackQuery):  # function that finds you an opponent for battling
    account = api.get_account(callback.message.from_user.id)
    opponent = api.get_opponent(callback.message.from_user.id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [],
    ])

    await callback.message.edit_text(
        text=f'You will battle against {opponent["username"]}\n'
             f'Your rating: {account["rating"]}\n'
             f'Your opponent rating: {opponent["rating"]}\n',
        reply_markup=markup,
        parse_mode="HTML",
    )


@router.callback_query(ChangeRating.filter(0 <= F.rating <= 3500))  # up the user rating
async def callback_foo8(callback: CallbackQuery, callback_data: ChangeRating):
    await show_five_tasks(callback, 0, callback_data.rating)


@router.callback_query(MoveInProblemset.filter(F.last_index >= 0))  # show other five tasks
async def callback_foo8(callback: CallbackQuery, callback_data: MoveInProblemset):
    await show_five_tasks(callback, callback_data.last_index, callback_data.rating)


@router.callback_query(MoveInOlympiads.filter(F.last_index >= 0))  # show other five olympiads
async def callback_foo8(callback: CallbackQuery, callback_data: MoveInOlympiads):
    await show_five_olympiads(callback, callback_data.last_index)


@router.callback_query(MoveInTopicsArchive.filter(F.last_index >= 0))  # show other five archives of topics
async def callback_foo8(callback: CallbackQuery, callback_data: MoveInTopicsArchive):
    await show_five_topics_archives(callback, callback_data.last_index)


@router.callback_query(MoveInTopic.filter(F.last_index >= 0))  # show other five topics
async def callback_foo8(callback: CallbackQuery, callback_data: MoveInTopic):
    await show_five_topics(callback, callback_data.last_index, callback_data.last_index_in_archive, callback_data.index)


@router.callback_query(ShowTopics.filter(F.last_index_in_archive >= 0))  # show other five
async def callback_foo8(callback: CallbackQuery, callback_data: ShowTopics):
    await show_five_topics(callback, 0, callback_data.last_index_in_archive, callback_data.index)


@router.callback_query(MoveBackToTopicsArchive.filter(F.last_index >= 0))  # show other five tasks
async def callback_foo8(callback: CallbackQuery, callback_data: MoveBackToTopicsArchive):
    await show_five_topics_archives(callback, callback_data.last_index)
    await show_five_topics_archives(callback, callback_data.last_index_in_archive)


@router.callback_query(Registration.filter())  # show other five tasks
async def callback_foo8(callback: CallbackQuery, callback_data: Registration):
    api.create_account(callback.from_user.id, callback_data.username)
    await send_main_menu(callback, callback.from_user.id)


''' =================== MESSAGE ============================================================= '''


@router.message(classes.LogInClass.username)
async def username_chosen(message: CallbackQuery, state: FSMContext):
    username = message.text
    await confirm_registration(message, username)


''' =================== OTHER FUNCTIONS ===================================================== '''


async def send_main_menu(message, user_id):
    try:
        account = api.get_account(user_id)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Ежедневная задача', callback_data='dailyProblem')],
            [InlineKeyboardButton(text='Ещё задач', callback_data='archive')],
            [InlineKeyboardButton(text='Темы', callback_data='topics')],
            [InlineKeyboardButton(text='Олимпиады', callback_data='olympiads')],
            [InlineKeyboardButton(text='Профиль', callback_data='profile')],
        ])
        if type(message) == CallbackQuery:
            await message.message.delete()
            await message.message.answer(
                text=f"Привет, {message.from_user.first_name}. Что хочешь посмотреть сегодня?",
                reply_markup=markup,
                parse_mode="html"
            )
        else:
            await message.delete()
            await message.answer(
                text=f"Привет, {message.from_user.first_name}. Что хочешь посмотреть сегодня?",
                reply_markup=markup,
                parse_mode="html"
            )
    except Exception as exc:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='register', callback_data='register')]])
        if type(message) == CallbackQuery:
            message = message.message
        await message.delete()
        await message.answer(
            text=f"Your aren't registered yet.",
            reply_markup=markup,
            parse_mode="html"
        )


async def show_five_tasks(callback: CallbackQuery, last_index: int, rating: int):
    problemset = api.get_problemset(callback.from_user.id, rating)
    current_problems = problemset[last_index: last_index + 5]

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
    if last_index >= 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='⬅',
                                 callback_data=MoveInProblemset(last_index=last_index - 5, rating=rating).pack()))
    else:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text=' ', callback_data='dummy function'))
    markup.inline_keyboard[-1].append(InlineKeyboardButton(text='move in problemset', callback_data='dummy function'))
    if last_index < len(problemset) - 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='➡',
                                 callback_data=MoveInProblemset(last_index=last_index + 5, rating=rating).pack()))
    else:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text=' ', callback_data='dummy function'))
    # adding start button
    markup.inline_keyboard.append([InlineKeyboardButton(text='main menu', callback_data='start')])

    ''' FINALLY EDITING TEXT OF THE CALLBACK '''
    await callback.message.edit_text(
        text=f'Your current rating is: <code>{rating}</code>',
        reply_markup=markup,
        parse_mode="html",
    )


async def show_five_olympiads(callback: CallbackQuery, last_index: int):
    olympiads = api.get_olympiads()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='menu', callback_data='start')],
    ])
    # adding links to markup
    for olympiad in olympiads[last_index: last_index + 5]:
        markup.inline_keyboard.append([InlineKeyboardButton(text=f'{olympiad["name"]}', url=olympiad['link'])])
    # adding arrows to markup
    markup.inline_keyboard.append([])
    if last_index >= 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='⬅', callback_data=MoveInOlympiads(last_index=last_index - 5).pack()))
    else:
        markup.inline_keyboard[-1].append(InlineKeyboardButton(text=' ', callback_data='dummy function'))
    markup.inline_keyboard[-1].append(InlineKeyboardButton(text='move in olympiads', callback_data='dummy function'))
    if last_index < len(olympiads) - 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='➡', callback_data=MoveInOlympiads(last_index=last_index + 5).pack()))
    else:
        markup.inline_keyboard[-1].append(InlineKeyboardButton(text=' ', callback_data='dummy function'))
    # finally editing message
    await callback.message.edit_text(
        text='Choose any olympiad you would like to participate in',
        reply_markup=markup,
    )


async def show_five_topics_archives(callback: CallbackQuery, last_index: int):
    topics = api.get_topics()
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='menu', callback_data='start')]])
    # adding topics to markup
    i = last_index
    for topic in topics[last_index: last_index + 5]:
        markup.inline_keyboard.append([InlineKeyboardButton(text=f'{topic["name"]}', callback_data=ShowTopics(
            last_index_in_archive=last_index, index=i).pack())])
        i += 1
    # adding nav button to markup
    markup.inline_keyboard.append([])
    if last_index >= 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='⬅', callback_data=MoveInTopicsArchive(last_index=last_index - 5).pack()))
    else:
        markup.inline_keyboard[-1].append(InlineKeyboardButton(text=' ', callback_data='dummy function'))
    markup.inline_keyboard[-1].append(InlineKeyboardButton(text='move in algos', callback_data='dummy function'))
    if last_index < len(topics) - 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='➡', callback_data=MoveInTopicsArchive(last_index=last_index + 5).pack()))
    else:
        markup.inline_keyboard[-1].append(InlineKeyboardButton(text=' ', callback_data='dummy function'))
    # finally editing message
    await callback.message.edit_text(
        text='Choose any topic you would like to learn',
        reply_markup=markup,
    )


async def show_five_topics(callback: CallbackQuery, last_index: int, back_last_index: int, topic_index: int):
    topics_archive = api.get_topics()
    topics = topics_archive[topic_index]['children']
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='back', callback_data=MoveBackToTopicsArchive(last_index=back_last_index).pack())]])
    # adding topics to markup
    for topic in topics[last_index:last_index + 5]:
        markup.inline_keyboard.append([InlineKeyboardButton(text=f'{topic["name"]}', url=topic['link'])])
    # adding nav button to markup
    markup.inline_keyboard.append([])
    if last_index >= 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='⬅', callback_data=MoveInTopic(last_index=last_index - 5,
                                                                     last_index_in_archive=back_last_index,
                                                                     index=topic_index).pack()))
    else:
        markup.inline_keyboard[-1].append(InlineKeyboardButton(text=' ', callback_data='dummy function'))
    markup.inline_keyboard[-1].append(
        InlineKeyboardButton(text='move in topics', callback_data='dummy function'))
    if last_index < len(topics) - 5:
        markup.inline_keyboard[-1].append(
            InlineKeyboardButton(text='➡', callback_data=MoveInTopic(last_index=last_index + 5,
                                                                     last_index_in_archive=back_last_index,
                                                                     index=topic_index).pack()))
    else:
        markup.inline_keyboard[-1].append(InlineKeyboardButton(text=' ', callback_data='dummy function'))
    # finally editing message
    await callback.message.edit_text(
        text='Choose any topic you would like to learn',
        reply_markup=markup,
    )


async def confirm_registration(message, username):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='confirm', callback_data=Registration(username=username).pack())],
        [InlineKeyboardButton(text='again', callback_data='register')],
    ])
    await message.delete()
    await message.answer(
        text=f'Your codeforces username is {username}?',
        reply_markup=markup,
        parse_mode='html'
    )
