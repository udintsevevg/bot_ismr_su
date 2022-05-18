from main import dp,bot
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from tools.states import User_state
from aiogram.dispatcher.filters import Text
from tools.func import get_task_number, push_task, push_quest


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(state = User_state.task, content_types= ['text'])
async def put_task(message: Message, state: FSMContext):
    await state.finish()
    return await get_task_number(message)


@dp.message_handler(state = [User_state.first_name, User_state.last_name, User_state.task_number, User_state.task_text], content_types= ['text'])
async def put_task(message: Message, state: FSMContext):
    states = str(await state.get_state()).split(':')[1]
    if states == 'first_name':
        await state.update_data(first_name=message.text)
        await message.answer("Отлично! Введите фамилию")
        await User_state.last_name.set()
    elif states == 'last_name':
        await state.update_data(last_name=message.text)
        await message.answer("Почти у цели! Введите номер задания")
        await User_state.task_number.set()
    elif states == 'task_number':
        await state.update_data(task_number=message.text)
        await message.answer("Последний этап! Введите ответ")
        await User_state.task_text.set()
    elif states == 'task_text':
        data = await state.get_data()
        await push_task(data['first_name'],data['last_name'],int(data['task_number']),message.text)
        await state.finish()


@dp.message_handler(state = [User_state.title, User_state.tasks, User_state.code, User_state.comment], content_types= ['text'])
async def get_title(message: Message, state: FSMContext):
    states = str(await state.get_state()).split(':')[1]
    if states == 'title':
        await state.update_data(title=message.text)
        await message.answer("Введите задание")
        await User_state.tasks.set()
    elif states == 'tasks':
        await state.update_data(tasks=message.text)
        await message.answer("Введите начальный код")
        await User_state.code.set()
    elif states == 'code':
        await state.update_data(code=message.text)
        await message.answer("Введите комментарий к заданию")
        await User_state.comment.set()
    elif states == 'comment':
        data = await state.get_data()
        await push_quest(data['title'],data['tasks'],data['code'],message.text)
        await state.finish()
