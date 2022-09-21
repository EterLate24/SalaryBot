import telebot

bot = telebot.TeleBot('5718439558:AAGfQ8DjTt3-3UIk3rW24DDNw7WUie7T_wY')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'privet')
    print('ok')

@bot.message_handler()
def user_commands(message):
    if message.text == "Сегодня":
        bot.send_message(message.chat.id, 'Сегодня')

bot.polling(none_stop=True)