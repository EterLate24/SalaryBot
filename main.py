import telebot
from buttons import main_buttons

bot = telebot.TeleBot('5718439558:AAGfQ8DjTt3-3UIk3rW24DDNw7WUie7T_wY')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет', reply_markup=main_buttons())
    print('ok')

@bot.message_handler()
def user_commands(message):
    if message.text == "Ввести часы":
        bot.send_message(message.chat.id, 'Ввести часы')
    elif message.text == "Посмотреть часы":
        bot.send_message(message.chat.id, 'Глянуть')
    elif message.text == "Регистрация":
        bot.send_message(message.chat.id, 'Глянуфыть')
    elif message.text == "Помощь":
        bot.send_message(message.chat.id, 'ыф')

bot.polling(none_stop=True)