import telebot
from buttons import *
import re
from config import TOKEN
from db_connect import *
from sql_requests import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Для создания учетной записи нужен ваш номер телефона, вы согласны?', reply_markup=reg_buttons())

@bot.message_handler(content_types="contact")
def contact(message):
    phone = "".join(symbol for symbol in re.findall("\d+", message.contact.phone_number))
    new_user(message.chat.id, message.chat.last_name, message.chat.first_name, phone, message.chat.username)
    bot.send_message(message.chat.id, 'Вы зарегистрированы')

    








# @bot.message_handler()
# def user_commands(message):
#     if message.text == "Ввести часы":
#         bot.send_message(message.chat.id, 'Ввести часы')
#     elif message.text == "Посмотреть часы":
#         bot.send_message(message.chat.id, 'Глянуть')
#     elif message.text == "Регистрация":
#         bot.send_message(message.chat.id, 'Глянуфыть')
#     elif message.text == "Помощь":
#         bot.send_message(message.chat.id, 'ыф')

bot.polling(none_stop=True)