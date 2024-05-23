from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def question_answer(first: str, second: str) -> ReplyKeyboardMarkup:
    man = KeyboardButton(text=first)
    woman = KeyboardButton(text=second)

    kb = [[man, woman]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard