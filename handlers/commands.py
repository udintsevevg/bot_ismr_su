from main import dp, bot
from aiogram.types import Message
from tools.states import User_state
from tools.func import get_last_task, get_task_number

last_task = {}


@dp.message_handler(commands=['task'])
async def get_task(message: Message):
    text = 'Введите номер задания'
    await User_state.task.set()
    return await message.answer(text)


@dp.message_handler(commands=['new_task'])
async def new_task(message: Message):
    task = await get_last_task()
    message.text = task
    if not last_task.get(message.from_user.id, False):
        last_task[message.from_user.id] = task
        return await get_task_number(message)
    elif last_task.get(message.from_user.id) == task:
        return await message.answer('Нет новых заданий, Анатолий не написал(')
    else:
        return await get_task_number(message)


@dp.message_handler(commands=['push_task'])
async def push_task1(message: Message):
    text = 'Введите имя'
    await message.answer(text= text)
    return await User_state.first_name.set()


@dp.message_handler(commands=['push_quest'])
async def push_quest1(message: Message):
    text = 'Введите загаловок задания'
    await message.answer(text= text)
    return await User_state.title.set()