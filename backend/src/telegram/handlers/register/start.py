from aiogram.types import Message
from backend.src.telegram.bot import logger
from backend.src.db.models.models import Users
from backend.src.telegram.keyboards.inline.inline import register_user, lets_game


async def start(msg: Message):
    try:
        user = Users.select_user(msg.from_user.id)
        if user:
            await msg.answer("Снова не во что поиграть? Давай тогда подберём игру по кнопке ниже",
                             reply_markup=lets_game())
        else:
            await msg.answer("Привет! Я бот PlayMentor.\n"
                             "Я могу помочь Вам подобрать игру, если не во что поиграть.\n"
                             "Но я заметил, что Вы не зарегистрированы у нас, "
                             "нужно пройти небольшую регистрацию по кнопке ниже.", reply_markup=register_user())
    except Exception as e:
        logger.exception("start", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")