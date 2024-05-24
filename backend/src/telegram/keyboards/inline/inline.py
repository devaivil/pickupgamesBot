from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка регистрации пользователя
def register_user() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text="Регистрация", callback_data="register")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return keyboard


# Кнопка, запускающая процесс подбора игры
def lets_game() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text="Подобрать игру", callback_data="game")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return keyboard


def socials() -> InlineKeyboardMarkup:
    url = 'https://google.com'
    button = InlineKeyboardButton(text="Официальный сайт", url=url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
    return keyboard