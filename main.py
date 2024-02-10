from telebot import TeleBot

import settings


bot = TeleBot(settings.TOKEN)


@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, "Hi! I'm MafiaGame bot!")


bot.infinity_polling()
