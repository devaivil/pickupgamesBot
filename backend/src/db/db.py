from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import settings


DATABASE_URL = f'sqlite:///{settings.db.db_name}.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

class Base(DeclarativeBase):
    pass