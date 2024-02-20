from telebot import TeleBot
from telebot import types
import sqlite3

import settings


bot = TeleBot(settings.TOKEN)

INSERT_USER_DATA = '''
    INSERT INTO users VALUES(?, ?, ?, ?)
'''

SELECT_USER_IN_GAME = '''
    SELECT user_name, cur_game_id FROM users WHERE cur_game_id IS NOT NULL
'''

SELECT_USER_ID = '''
    SELECT user_id FROM users
'''

UPDATE_IN_GAME_ID = '''
    UPDATE users SET cur_game_id = ? WHERE user_id = ?
'''


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Hi! I'm MafiaGame bot!")
    else:
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        users_in_game = cursor.execute(SELECT_USER_IN_GAME).fetchall()
        users_in_game_list = [name[0] for name in users_in_game]
        markup = types.InlineKeyboardMarkup()
        login_btn = types.InlineKeyboardButton('Присоединиться', callback_data='login')
        markup.add(login_btn)
        bot.send_message(message.chat.id, f'В игре: @{", @".join(users_in_game_list)}', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'login':

        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        users_id = cursor.execute(SELECT_USER_ID).fetchall()
        id_list = [id[0] for id in users_id]
        if callback.from_user.id not in id_list:
            cursor.execute(INSERT_USER_DATA, (callback.from_user.id, callback.from_user.username, 0, None))
            connect.commit()

        users_in_game = cursor.execute(SELECT_USER_IN_GAME).fetchall()
        in_game_id_list = [id[1] for id in users_in_game]
        if callback.message.chat.id not in in_game_id_list:
            cursor.execute(UPDATE_IN_GAME_ID, (callback.message.chat.id, callback.from_user.id))
            connect.commit()
        else:
            cursor.execute(UPDATE_IN_GAME_ID, (None, callback.from_user.id))
            connect.commit()

        users_in_game = cursor.execute(SELECT_USER_IN_GAME).fetchall()
        users_in_game_list = [name[0] for name in users_in_game]
        markup = types.InlineKeyboardMarkup()
        login_btn = types.InlineKeyboardButton('Присоединиться', callback_data='login')
        markup.add(login_btn)
        bot.edit_message_text(f'В игре: @{", @".join(users_in_game_list)}', callback.message.chat.id, callback.message.id, reply_markup=markup)


bot.infinity_polling()
