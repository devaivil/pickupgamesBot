from sqlalchemy import Column, String, Integer, insert, select, ForeignKey
from sqlalchemy.orm import relationship
from backend.src.db.db import Base, session


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, unique=True)
    tg_username = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    @classmethod
    def select_user(cls, tg_id: int):
        with session:
            user = select(cls).filter_by(tg_id=tg_id)
            result = session.execute(user)
            return result.scalar_one_or_none()

    @classmethod
    def add_user(cls, tg_id: int, tg_username: str, first_name: str, sex: str, age: int):
        with session:
            new_user = insert(cls).values(tg_id=tg_id, tg_username=tg_username, first_name=first_name, sex=sex, age=age)
            session.execute(new_user)
            session.commit()


class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    developer = Column(String, nullable=False)
    description = Column(String, nullable=False)

    parameters = relationship('GamesParameters', backref='games')

    @classmethod
    def get_games_list(cls, game_ids: list):
        games_list = session.query(cls).filter(
            cls.id.in_(game_ids)
        ).all()
        return games_list


class GamesParameters(Base):
    __tablename__ = 'games_parameters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(ForeignKey('games.id'))
    first_answer = Column(Integer, nullable=False)
    second_answer = Column(Integer, nullable=False)
    third_answer = Column(Integer, nullable=False)
    fourth_answer = Column(Integer, nullable=False)
    fifth_answer = Column(Integer, nullable=False)

    @classmethod
    def get_game_after(cls,
                       first_answer: int,
                       second_answer: int,
                       third_answer: int,
                       fourth_answer: int,
                       fifth_answer: int):
        result = session.query(cls).filter(
            cls.first_answer == first_answer,
            cls.second_answer == second_answer,
            cls.third_answer == third_answer,
            cls.fourth_answer == fourth_answer,
            cls.fifth_answer == fifth_answer
        ).all()
        return result
