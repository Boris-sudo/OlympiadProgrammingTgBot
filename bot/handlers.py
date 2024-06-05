import asyncio
import time
import typing
import socket
import json

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
    user_id = callback.from_user.id
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


@router.callback_query(F.data == "fight")  # function making fight with another user
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await create_new_fight(callback, user_id)


@router.callback_query(F.data == "stop_fight")  # function stopping fight with another user
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    api.delete_fight(user_id)


@router.callback_query(F.data == "give_up")  # function stopping fight with another user (you give up and lose)
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    api.give_up_fight(user_id)


@router.callback_query(F.data == "check_solution")  # function check solution of fight
async def show_daily_problem(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    api.check_solution(user_id)


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
        user_in_fight = api.check_user_in_figth(user_id)
        for i in user_in_fight:
            user_in_fight = json.loads(i)
        if user_in_fight['exist'] == '1':
            await show_fight_task(message, user_id)
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Ежедневная задача', callback_data='dailyProblem')],
                [InlineKeyboardButton(text='Спаринговаться', callback_data='fight')],
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
        try:
            await message.delete()
        except:
            pass
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


async def confirm_registration(message, username: str):
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


async def create_new_fight(callback: CallbackQuery, user_id: int):
    user = api.get_account(user_id)
    address = ('127.0.0.1', user['port'])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(8)
    server.setblocking(False)

    api.create_new_fight(user_id)  # here bot sending request for django to  find opponent

    loop = asyncio.get_event_loop()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='stop searching', callback_data='stop_fight')],
    ])
    await callback.message.edit_text(
        text='Searching for opponent..',
        reply_markup=markup,
        parse_mode='html',
    )
    client, _ = await loop.sock_accept(server)
    loop.create_task(await_fight_response(callback, user_id, client))


async def await_fight_response(callback, user_id, client):
    loop = asyncio.get_event_loop()
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255))[17:-2]
        if request is not None:
            break
    client.close()

    if request == b'done':
        await show_fight_task(callback, user_id)
        return
    elif request == b'aborted':
        await send_main_menu(callback, user_id)
        return


async def show_fight_task(callback: CallbackQuery, user_id: int):
    user = api.get_account(user_id)
    address = ('127.0.0.1', user['port'])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(address)
    server.listen(8)
    server.setblocking(False)

    task = api.get_task((user_id))
    for i in task:
        task = json.loads(i)
        break

    await show_fight_task_2(callback, user_id, task, server)


async def show_fight_task_2(callback, user_id, task, server):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'{task["task"]["name"]}',
            url=f'https://codeforces.com/problemset/problem/{task["task"]["contestId"]}/{task["task"]["index"]}',
        )],
        [InlineKeyboardButton(text='check', callback_data='check_solution')],
        [InlineKeyboardButton(text='give up', callback_data='give_up')],
    ])

    await SEND_MESSAGE(callback, 'Opponent found', markup)

    loop = asyncio.get_event_loop()
    client, _ = await loop.sock_accept(server)
    loop.create_task(await_during_fight(callback, user_id, client, server, task))


async def await_during_fight(callback, user_id, client, server, task):
    loop = asyncio.get_event_loop()
    request = None
    while request != 'quit':
        request = (await loop.sock_recv(client, 255))[17:-2]
        if request is not None:
            break

    if request == b'wrong':
        await wrong_solution(callback, user_id, server, task)
    elif request == b'correct':
        await correct_solution(callback, user_id, server)
    elif request == b'finished':
        await finish_game(callback, user_id, server)


async def correct_solution(callback, user_id, server):
    await SEND_MESSAGE(callback, 'Amazing, you submitted your solution first! You won!', None)
    server.close()
    await asyncio.sleep(5)
    await send_main_menu(callback, user_id)


async def finish_game(callback, user_id, server):
    await SEND_MESSAGE(callback,'Sorry, but your opponent submitted his solution first.', None)
    server.close()
    await asyncio.sleep(5)
    await send_main_menu(callback, user_id)


async def wrong_solution(callback, user_id, server, task):
    await SEND_MESSAGE(callback, 'You haven`t solved this problem.\nIf I am wrong, please try to send your submission again.', None)
    await asyncio.sleep(1)
    await show_fight_task_2(callback, user_id, server, task)


async def SEND_MESSAGE(callback, text, markup):
    try:
        await callback.message.edit_text(
            text=text,
            reply_markup=markup,
            parse_mode='html',
        )
    except:
        try:
            await callback.edit_text(
                text=text,
                reply_markup=markup,
                parse_mode='html',
            )
        except:
            try:
                await callback.message.answer(
                    text=text,
                    reply_markup=markup,
                    parse_mode='html',
                )
            except:
                await callback.answer(
                    text=text,
                    reply_markup=markup,
                    parse_mode='html',
                )