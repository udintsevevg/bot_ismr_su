from aiogram.dispatcher.filters.state import State, StatesGroup

class User_state(StatesGroup):
    task = State()
    first_name = State()
    last_name = State()
    task_number = State()
    task_text = State()
    title = State()
    tasks = State()
    code = State()
    comment = State()
