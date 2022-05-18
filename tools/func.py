import aiohttp
from aiogram.types import Message

async def get_tasks():
    link = 'https://api.imsr.su/main/get_tasks'
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as res:
            return await res.json()


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


async def push_task(f_name, l_name, task_number, answer):
    link = 'https://api.imsr.su/add_answer'
    form = aiohttp.FormData()
    form.add_field('first_name', str(f_name))
    form.add_field('last_name', str(l_name))
    form.add_field('answer', str(answer))
    form.add_field('task_id', task_number)
    async with aiohttp.ClientSession() as session:
        await session.post(url= link, data= form)


async def push_quest(title, tasks, code, comment):
    link = 'https://api.imsr.su/add_request'
    form = aiohttp.FormData()
    form.add_field('title', str(title))
    form.add_field('description', str(tasks))
    form.add_field('start_code', str(code))
    form.add_field('comment', str(comment))
    async with aiohttp.ClientSession() as session:
        await session.post(url= link, data= form)
