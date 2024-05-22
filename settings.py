from dataclasses import dataclass
from environs import Env


@dataclass
class Database:
    db_name: str

@dataclass
class TgBot:
    token: str

@dataclass
class Settings:
    tg_bot: TgBot
    db:     Database


env: Env = Env()
env.read_env()

settings = Settings(tg_bot = TgBot(token = env('TOKEN')),
                    db = Database(db_name = env('DB_NAME')),)
