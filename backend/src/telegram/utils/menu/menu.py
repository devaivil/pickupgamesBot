from aiogram import Bot
from aiogram.types import BotCommand

from backend.src.telegram.utils.menu.commands_list import commands
from settings import settings

bot = Bot(token=settings.tg_bot.token, parse_mode='HTML')


# Кнопка меню, которая упаравляет основным функционалом
async def set_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in commands.items()
    ]
    await bot.set_my_commands(main_menu_commands)