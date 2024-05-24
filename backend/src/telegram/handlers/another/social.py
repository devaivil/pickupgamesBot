from aiogram.types import Message
from backend.src.telegram.keyboards.inline.inline import socials


async def social(msg: Message):
    await msg.answer("Чтобы не ограничиваться только моим функционалом, "
                     "Вы сможете перейти на наш официальный сайт по ссылке ниже", reply_markup=socials())

