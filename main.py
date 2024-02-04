from telebot import TeleBot

TOKEN = '6977197895:AAHLm-Brrmdix91kJJAFHEi_0FhOPJHAcYE'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def greet(message):
    bot.send_message(message.chat.id, "Hi! I'm MafiaGame bot!")


bot.infinity_polling()
