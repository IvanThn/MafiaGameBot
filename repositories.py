from sqlalchemy import select, update

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
    res = []
    for user in session.scalars(users):
        res.append((user.user_name, user.cur_game_id))
    return res


def select_usr_id():
    session = Session(engine)

    users = select(Users.user_id)
    res = []
    for user_id in session.scalars(users):
        res.append(user_id)
    return res


def update_in_game_id(game_id: int or None, user_id: int):
    session = Session(engine)

    session.query(Users).filter(Users.user_id == user_id).update({'cur_game_id': game_id})
    session.commit()
