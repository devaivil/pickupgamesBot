from aiogram.filters import Command, CommandStart

from backend.src.db.db import Base, engine
from backend.src.telegram.bot import dp, bot
from backend.src.telegram.utils.menu.menu import set_menu
from backend.src.telegram.handlers.register.start import start
from backend.src.telegram.handlers.register.register import register, get_user_sex, create_user
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

    dp.run_polling(bot)