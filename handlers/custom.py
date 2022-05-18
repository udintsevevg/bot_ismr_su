from main import dp,bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from tools.states import User_state
import aiohttp


async def get_tasks():
    link = 'https://api.imsr.su/main/get_tasks'
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as res:
            return await res.json()


async def push_task(f_name, l_name, task_number, answer):
    link = 'https://api.imsr.su/add_answer'
    form = aiohttp.FormData()
    form.add_field('first_name', str(f_name))
    form.add_field('last_name', str(l_name))
    form.add_field('answer', str(answer))
    form.add_field('task_id', task_number)
    async with aiohttp.ClientSession() as session:
        await session.post(url= link, data= form)


async def get_task_number(message: Message):
    resp = await get_tasks()
    for i in resp.get('data'):
        if str(i.get('id')) == str(message.text):
            return await message.answer(i.get('description'))
    await message.answer('Нет такого задания')


async def get_last_task():
    resp = await get_tasks()
    resp = resp.get('data')
    return max([i.get('id') for i in resp])


@dp.message_handler(state = User_state.task, content_types= ['text'])
async def put_task(message: Message, state: FSMContext):
    await state.finish()
    return await get_task_number(message)

@dp.message_handler(state = User_state.first_name, content_types= ['text'])
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Отлично! Введите фамилию")
    await User_state.last_name.set()

@dp.message_handler(state = User_state.last_name, content_types= ['text'])
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Почти у цели! Введите номер задания")
    await User_state.task_number.set()

@dp.message_handler(state = User_state.task_number, content_types= ['text'])
async def get_task_number(message: Message, state: FSMContext):
    await state.update_data(task_number=message.text)
    await message.answer("Последний этап! Введите ответ")
    await User_state.task_text.set()

@dp.message_handler(state = User_state.task_text, content_types= ['text'])
async def get_task_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await push_task(data['first_name'],data['last_name'],int(data['task_number']),message.text)
    await state.finish()



async def push_quest(title, tasks, code, comment):
    link = 'https://api.imsr.su/add_request'
    form = aiohttp.FormData()
    form.add_field('title', str(title))
    form.add_field('description', str(tasks))
    form.add_field('start_code', str(code))
    form.add_field('comment', str(comment))
    async with aiohttp.ClientSession() as session:
        await session.post(url= link, data= form)


@dp.message_handler(state = User_state.title, content_types= ['text'])
async def get_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите задание")
    await User_state.tasks.set()

@dp.message_handler(state = User_state.tasks, content_types= ['text'])
async def get_tasks(message: Message, state: FSMContext):
    await state.update_data(tasks=message.text)
    await message.answer("Введите начальный код")
    await User_state.code.set()

@dp.message_handler(state = User_state.code, content_types= ['text'])
async def get_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("Введите комментарий к заданию")
    await User_state.comment.set()

@dp.message_handler(state = User_state.comment, content_types= ['text'])
async def get_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    await push_task(data['title'],data['tasks'],data['code'],message.text)
    await state.finish()