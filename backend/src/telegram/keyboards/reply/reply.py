from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def user_sex() -> ReplyKeyboardMarkup:
    man = KeyboardButton(text="Мужской")
    woman = KeyboardButton(text="Женский")

    kb = [[man, woman]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Ваш пол",
        one_time_keyboard=True
    )
    return keyboard