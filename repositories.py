from sqlalchemy import select

from sqlalchemy.orm import Session
from ORM import engine, Users

# session = Session(engine)
#
# stmt = select(Users).where(Users.user_id.in_([123]))
#
# for user in session.scalars(stmt):
#     print(user)


def insert_user(user_id: int, user_name: str):
    with Session(engine) as session:
        user = Users(
            user_id=user_id,
            user_name=user_name,
            wins_col=0
        )
        session.add(user)
        session.commit()


def select_users_in_game():
    session = Session(engine)

    users = select(Users).where(Users.cur_game_id.isnot(None))
    for user in session.scalars(users):
        return user.user_name, user.cur_game_id



