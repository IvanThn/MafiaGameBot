from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    wins_col = Column(Integer, nullable=False)
    cur_game_id = Column(Integer)
    cur_role = Column(String)

    def __repr__(self):
        return (f'ID: {self.user_id} NAME: {self.user_name} WINS: {self.wins_col} '
                f'GAME: {self.cur_game_id or "Не в игре"} ROLE: {self.cur_role or "Не в игре"}')


engine = create_engine("sqlite:///sqlite3.db")
Base.metadata.create_all(engine)
