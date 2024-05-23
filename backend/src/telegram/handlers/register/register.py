from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from backend.src.telegram.bot import bot
from backend.src.telegram.keyboards.reply.reply import question_answer
from backend.src.telegram.keyboards.inline.inline import lets_game
from backend.src.telegram.states import States
from backend.src.telegram.bot import logger

from backend.src.db.models.models import Users


async def register(callback: CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(callback.from_user.id,
                               "Напишите, пожалуйста, свой пол",
                               reply_markup=question_answer("Мужской", "Женский"))
        await state.set_state(States.get_sex)
    except Exception as e:
        logger.exception("register", e)
        await bot.send_message(callback.from_user.id,
                               "Кажется, произошла какая-то техническая ошибка, "
                               "извините, пожалуйста, мы решаем эти проблемы....")


async def get_user_sex(msg: Message, state: FSMContext):
    try:
        await state.update_data(sex=msg.text)
        await msg.answer("Хорошо, напишите, пожалуйста, свой возраст")
        await state.set_state(States.get_age)
    except Exception as e:
        logger.exception("get_user_sex", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")


async def create_user(msg: Message, state: FSMContext):
    try:
        await state.update_data(age=msg.text)
        get_info = await state.get_data()
        sex = get_info.get('sex')
        age = get_info.get('age')

        Users.add_user(tg_id=msg.from_user.id,
                       tg_username=msg.from_user.username,
                       first_name=msg.from_user.first_name,
                       sex=sex,
                       age=age)
        await msg.answer("Отлично! Регистрация прошла успешно, а теперь можно и подобрать Вам игру.\n"
                         "Вы сможете сделать это по кнопке ниже", reply_markup=lets_game())
    except Exception as e:
        logger.exception("create_user", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")