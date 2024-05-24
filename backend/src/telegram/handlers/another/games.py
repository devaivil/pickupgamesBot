from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.src.telegram.bot import bot, logger
from backend.src.telegram.keyboards.inline.inline import register_user
from backend.src.telegram.keyboards.reply.reply import question_answer
from backend.src.telegram.states import States
from backend.src.telegram.filters.games_dicts import answers

from backend.src.db.models.models import Users, Games, GamesParameters


async def games(from_user_id: int, state: FSMContext):
    try:
        user = Users.select_user(from_user_id)
        if user:
            await bot.send_message(from_user_id,
                                   "Как упоминалось ранее, я Помощник по подбору игр, исходя из Ваших предпочтений\n"
                                   "Чтобы подобрать тебе игру нужно ответить на несколько вопросов.\n"
                                   "Начинаем?",
                                   reply_markup=question_answer("Начинаем", "Не сейчас"))
            await state.set_state(States.first_q)
        else:
            await bot.send_message(from_user_id,
                                   "Перед тем, как я смогу подобрать Вам игру на вечер, "
                                   "я должен Вас зарегистрировать.\n"
                                   "Это можно сделать по кнопке ниже", reply_markup=register_user())
    except Exception as e:
        logger.exception("games", e)
        await bot.send_message(from_user_id,
                               "Кажется, произошла какая-то техническая ошибка, "
                               "извините, пожалуйста, мы решаем эти проблемы....")

async def games_command(msg: Message, state: FSMContext):
    await games(msg.from_user.id, state)

async def games_button(callback_query: CallbackQuery, state: FSMContext):
    await games(callback_query.from_user.id, state)


async def first_question(msg: Message, state: FSMContext):
    try:
        await state.update_data(answer_start=msg.text)
        get_data = await state.get_data()
        answer_start = get_data.get('answer_start')
        if answer_start == 'Начинаем':
            await msg.answer("Для начала расскажите, как Вы себя сегодня чувствуете?",
                             reply_markup=question_answer("Утомлён", "Энергичен"))
            await state.set_state(States.second_q)
        if answer_start == 'Не сейчас':
            await msg.answer("Хорошо, если не сейчас, тогда ты сможешь ознакомиться "
                             "с другими моими возможностями в меню! Успехов!")
            await state.clear()
    except Exception as e:
        logger.exception("first_question", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")


async def second_question(msg: Message, state: FSMContext):
    try:
        await state.update_data(answer_one=msg.text)

        await msg.answer("Окей, какой уровень сложности игры для Вас приемлем?",
                         reply_markup=question_answer("Давайте попроще", "Давайте посложнее"))
        await state.set_state(States.third_q)
    except Exception as e:
        logger.exception("second_question", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")


async def third_question(msg: Message, state: FSMContext):
    try:
        await state.update_data(answer_two=msg.text)

        await msg.answer("Что в игре Вас цепляет больше всего?",
                         reply_markup=question_answer("Невероятный сюжет", "Интересный геймплей"))
        await state.set_state(States.fourth_q)
    except Exception as e:
        logger.exception("third_question", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")


async def fourth_question(msg: Message, state: FSMContext):
    try:
        await state.update_data(answer_three=msg.text)

        await msg.answer("Любите ли Вы мирный путь развития?",
                         reply_markup=question_answer("Да", "Нет"))
        await state.set_state(States.fifth_q)
    except Exception as e:
        logger.exception("fourth_question", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")


async def fifth_question(msg: Message, state: FSMContext):
    try:
        await state.update_data(answer_four=msg.text)

        await msg.answer("Какая локация игры Вам ближе?",
                         reply_markup=question_answer("Средневековье", "Современный мир"))
        await state.set_state(States.result)
    except Exception as e:
        logger.exception("fifth_question", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")


async def result_games(msg: Message, state: FSMContext):
    try:
        await state.update_data(answer_five=msg.text)

        await msg.answer("Спасибо большое за предоставленные ответы, сейчас посмотрим, какие у меня есть игры,"
                         "исходя из Ваших ответов...")
        await bot.send_chat_action(msg.from_user.id, 'typing')

        get_data = await state.get_data()
        answer_one = get_data.get('answer_one')
        answer_two = get_data.get('answer_two')
        answer_three = get_data.get('answer_three')
        answer_four = get_data.get('answer_four')
        answer_five = get_data.get('answer_five')

        param_list = {
            "param_one": answers.get(answer_one),
            "param_two": answers.get(answer_two),
            "param_three": answers.get(answer_three),
            "param_four": answers.get(answer_four),
            "param_five": answers.get(answer_five)
        }

        games_list = GamesParameters.get_game_after(
            first_answer=param_list["param_one"],
            second_answer=param_list["param_two"],
            third_answer=param_list["param_three"],
            fourth_answer=param_list["param_four"],
            fifth_answer=param_list["param_five"]
        )

        game_ids = [param.game_id for param in games_list]
        games = Games.get_games_list(game_ids)

        await msg.answer("Вот подборка игр, которая может тебе подойти..")
        await bot.send_chat_action(msg.from_user.id, 'typing')

        for game in games:
            await msg.answer(f"<b>Название:</b> {game.name}\n"
                             f"<b>Разработчик:</b> {game.developer}\n"
                             f"<b>Описание:</b> {game.description}")
    except Exception as e:
        logger.exception("result_games", e)
        await msg.answer("Кажется, произошла какая-то техническая ошибка, "
                         "извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()
