from telebot import TeleBot
from telebot import types

import settings

from repositories import *

bot = TeleBot(settings.TOKEN)


def get_start_button():
    users_in_game = select_users_in_game()
    users_in_game_list = [name[0] for name in users_in_game]
    markup = types.InlineKeyboardMarkup()
    login_btn = types.InlineKeyboardButton('Присоединиться', callback_data='login')
    markup.add(login_btn)
    return markup, users_in_game_list


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Hi! I'm MafiaGame bot!")
    else:
        markup, users_in_game = get_start_button()
        bot.send_message(
            message.chat.id,
            f'В игре: @{", @".join(users_in_game)}',
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'login':
        id_list = select_usr_id()
        if callback.from_user.id not in id_list:
            insert_user(callback.from_user.id, callback.from_user.username)

        users_in_game = select_users_in_game()
        in_game_id_list = [user_id[1] for user_id in users_in_game]
        if callback.message.chat.id not in in_game_id_list:
            update_in_game_id(callback.message.chat.id, callback.from_user.id)
        else:
            update_in_game_id(None, callback.from_user.id)

        markup, users_in_game = get_start_button()
        bot.edit_message_text(
            f'В игре: @{", @".join(users_in_game)}',
            callback.message.chat.id,
            callback.message.id,
            reply_markup=markup
        )


bot.infinity_polling()
