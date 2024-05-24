from aiogram.filters import Command, CommandStart

from backend.src.db.db import Base, engine
from backend.src.telegram.bot import dp, bot
from backend.src.telegram.utils.menu.menu import set_menu
from backend.src.telegram.handlers.register.start import start
from backend.src.telegram.handlers.register.register import register, get_user_sex, create_user
from backend.src.telegram.handlers.another.games import (games_command, games_button, first_question, second_question,
                                                         third_question, fourth_question, fifth_question, result_games)
from backend.src.telegram.handlers.another.social import social
from backend.src.telegram.states import States

if __name__ == '__main__':
    # Инициализирует БД
    Base.metadata.create_all(engine)

    # Создает кнопку меню
    dp.startup.register(set_menu)

    # Регистрация команды /start
    dp.message.register(start, CommandStart())

    # Регистрация перехода для регистрации
    dp.callback_query.register(register, lambda c: c.data == 'register')
    dp.message.register(get_user_sex, States.get_sex)
    dp.message.register(create_user, States.get_age)

    # Регистрация подбора игры
    dp.message.register(games_command, Command('games'))
    dp.callback_query.register(games_button, lambda c: c.data == 'game')
    dp.message.register(first_question, States.first_q)
    dp.message.register(second_question, States.second_q)
    dp.message.register(third_question, States.third_q)
    dp.message.register(fourth_question, States.fourth_q)
    dp.message.register(fifth_question, States.fifth_q)
    dp.message.register(result_games, States.result)

    # Регистрация ссылки на официальный сайт
    dp.message.register(social, Command('socials'))

    dp.run_polling(bot)