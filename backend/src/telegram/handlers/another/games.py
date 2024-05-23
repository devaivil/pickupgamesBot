from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from backend.src.telegram.bot import bot, logger
from backend.src.telegram.keyboards.inline.inline import register_user
from backend.src.telegram.keyboards.reply.reply import question_answer
from backend.src.telegram.states import States

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

async def games_command(message: Message, state: FSMContext):
    await games(message.from_user.id, state)

async def games_button(callback_query: CallbackQuery, state: FSMContext):
    await games(callback_query.from_user.id, state)


async def first_question(message: Message, state: FSMContext):
    try:
        await state.update_data(answer_start=message.text)
        get_data = await state.get_data()
        answer_start = get_data.get('answer_start')
        if answer_start == 'Начинаем':
            await message.answer("Для начала расскажите, как Вы себя сегодня чувствуете?",
                                 reply_markup=question_answer("Утомлён", "Энергичен"))
            await state.set_state(States.second_q)
        if answer_start == 'Не сейчас':
            await message.answer("Хорошо, если не сейчас, тогда ты сможешь ознакомиться "
                                 "с другими моими возможностями в меню! Успехов!")
            await state.clear()
    except Exception as e:
        logger.exception("first_question", e)
        await message.answer("Кажется, произошла какая-то техническая ошибка, "
                             "извините, пожалуйста, мы решаем эти проблемы....")


async def second_question(message: Message, state: FSMContext):
    try:
        await state.update_data(answer_one=message.text)

        await message.answer("Окей, какой уровень сложности игры для Вас приемлем?",
                             reply_markup=question_answer("Давайте попроще", "Давайте посложнее"))
        await state.set_state(States.third_q)
    except Exception as e:
        logger.exception("second_question", e)
        await message.answer("Кажется, произошла какая-то техническая ошибка, "
                             "извините, пожалуйста, мы решаем эти проблемы....")


async def third_question(message: Message, state: FSMContext):
    try:
        await state.update_data(answer_two=message.text)

        await message.answer("Что в игре Вас цепляет больше всего?",
                             reply_markup=question_answer("Невероятный сюжет", "Интересный геймплей"))
        await state.set_state(States.fourth_q)
    except Exception as e:
        logger.exception("third_question", e)
        await message.answer("Кажется, произошла какая-то техническая ошибка, "
                             "извините, пожалуйста, мы решаем эти проблемы....")


async def fourth_question(message: Message, state: FSMContext):
    try:
        await state.update_data(answer_three=message.text)

        await message.answer("Любите ли Вы мирный путь развития?",
                             reply_markup=question_answer("Да", "Нет"))
        await state.set_state(States.fifth_q)
    except Exception as e:
        logger.exception("fourth_question", e)
        await message.answer("Кажется, произошла какая-то техническая ошибка, "
                             "извините, пожалуйста, мы решаем эти проблемы....")


async def fifth_question(message: Message, state: FSMContext):
    try:
        await state.update_data(answer_four=message.text)

        await message.answer("Какая локация игры Вам ближе?",
                             reply_markup=question_answer("Средневековье", "Современный мир"))
        await state.set_state(States.result)
    except Exception as e:
        logger.exception("fifth_question", e)
        await message.answer("Кажется, произошла какая-то техническая ошибка, "
                             "извините, пожалуйста, мы решаем эти проблемы....")


async def result_games(message: Message, state: FSMContext):
    try:
        await state.update_data(answer_five=message.text)

        await message.answer("Спасибо большое за предоставленные ответы, сейчас посмотрим, какие у меня есть игры,"
                             "исходя из Ваших ответов...")
        await bot.send_chat_action(message.from_user.id, 'typing')

        get_data = await state.get_data()
        answer_one = get_data.get('answer_one')
        answer_two = get_data.get('answer_two')
        answer_three = get_data.get('answer_three')
        answer_four = get_data.get('answer_four')
        answer_five = get_data.get('answer_five')

        param_one = 0
        param_two = 0
        param_three = 0
        param_four = 0
        param_five = 0

        if answer_one == 'Утомлён':
            param_one = 1
        if answer_one == 'Энергичен':
            param_one = 2

        if answer_two == 'Давайте попроще':
            param_two = 1
        if answer_one == 'Давайте посложнее':
            param_two = 2

        if answer_three == 'Невероятный сюжет':
            param_three = 1
        if answer_three == 'Интересный геймплей':
            param_three = 2

        if answer_four == 'Да':
            param_four = 1
        if answer_one == 'Нет':
            param_four = 2

        if answer_five == 'Средневековье':
            param_five = 1
        if answer_five == 'Современный мир':
            param_five = 2

        games_list = GamesParameters.get_game_after(
            first_answer=param_one,
            second_answer=param_two,
            third_answer=param_three,
            fourth_answer=param_four,
            fifth_answer=param_five
        )

        game_ids = [param.game_id for param in games_list]
        games = Games.get_games_list(game_ids)

        await message.answer("Вот подборка игр, которая может тебе подойти..")
        await bot.send_chat_action(message.from_user.id, 'typing')

        for game in games:
            await message.answer(f"<b>Название:</b> {game.name}\n"
                                 f"<b>Разработчик:</b> {game.developer}\n"
                                 f"<b>Описание:</b> {game.description}")
    except Exception as e:
        logger.exception("result_games", e)
        await message.answer("Кажется, произошла какая-то техническая ошибка, "
                             "извините, пожалуйста, мы решаем эти проблемы....")
    finally:
        await state.clear()