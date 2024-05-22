from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    get_sex = State()
    get_age = State()