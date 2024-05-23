from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    get_sex = State()
    get_age = State()

    first_q = State()
    second_q = State()
    third_q = State()
    fourth_q = State()
    fifth_q = State()
    result = State()