import telebot
from buttons import *
import re
from config import TOKEN
from db_connect import *
from sql_requests import *
from datetime import *
import datetime


bot = telebot.TeleBot(TOKEN)

# ----------------------------commands
@bot.message_handler(commands=['start'])
def start(message):
    check = exist_check(message.chat.id)
    if(check):
        bot.send_message(message.chat.id, 'Здравствуйте ' + message.chat.first_name + '!', reply_markup=main_buttons())
    else: 
        bot.send_message(message.chat.id, 'Для создания учетной записи нужен ваш номер телефона, вы согласны?', reply_markup=reg_buttons())

@bot.message_handler(content_types="contact")
def contact(message):
    phone = "".join(symbol for symbol in re.findall("\d+", message.contact.phone_number))
    reg_check = new_user(message.chat.id, message.chat.last_name, message.chat.first_name, phone, message.chat.username)
    if (reg_check):
        bot.send_message(message.chat.id, 'Вы зарегистрированы', reply_markup=main_buttons())
    else:
        bot.send_message(message.chat.id, 'Данные обновлены', reply_markup=main_buttons())


# ----------------------------messages listener
@bot.message_handler(func=lambda m: True)
def main_listener(m):
    if (m.text == 'Изменить ставку в час'):
        msg = bot.send_message(m.chat.id, 'Введите ставку в час(только число):')
        bot.register_next_step_handler(msg, change_salary_step)

    elif (m.text == 'Ввести/изменить часы'):
        msg = bot.send_message(m.chat.id, 'Введите часы за сегодня(максимум 8)')
        bot.register_next_step_handler(msg, enter_hours_step)

    elif (m.text == 'Посмотреть часы'):
        msg = bot.send_message(m.chat.id, 'Выберите промежуток или введите дату вручную в формате(дд мм гггг)', reply_markup=choose_buttons())
        bot.register_next_step_handler(msg, choose_interval_step)

    elif (m.text == 'Помощь'):
        bot.send_message(m.chat.id, 'Разработчик: @eterlate(не без помощи @Whatislove567)', reply_markup=main_buttons())

    elif (m.text == 'Посмотреть список пользователей'):
        if check_admin(m.chat.id):
            bot.send_message(m.chat.id, 'Все пользователи: ')
            result = users_list()
            message = ''
            counter = 0
            for el in result:
                counter += 1
                user_str = f"\nChat_id: {el[0]}\nТелефон: {el[1]}\nФамилия: {el[2]}\nИмя: {el[3]}\nНик: {el[4]}\n"
                message += user_str + '---------------'
                if counter > 30:
                    bot.send_message(m.chat.id, message)
                    counter = 0
                    message = ''
            if counter > 1:
                bot.send_message(m.chat.id, message)
        else:
            bot.send_message(m.chat.id, 'Вы не администратор', reply_markup=main_buttons())

    elif (m.text == 'Администратор'):
        if check_admin(m.chat.id):
            bot.send_message(m.chat.id, 'Вход выполнен', reply_markup=admin_buttons())
        else:
            bot.send_message(m.chat.id, 'Вы не администратор', reply_markup=main_buttons())
                
    elif (m.text == 'Отметить часы пользователя'):
        if check_admin(m.chat.id):
            msg = bot.send_message(m.chat.id, 'Введите Chat_id пользователя:')
            bot.register_next_step_handler(msg, paid_user_hours_step)
        else:
            bot.send_message(m.chat.id, 'Вы не администратор', reply_markup=main_buttons())

    elif (m.text == 'Назад'):
        bot.send_message(m.chat.id, 'Возвращаю...', reply_markup=main_buttons())

    else:
        bot.reply_to(m, 'Я Вас не понимаю', reply_markup=main_buttons())

# ----------------------------functions
def paid_user_hours_step(msg):
    try:
        user_chat_id = msg.text
        check_salary_exist = user_salary(user_chat_id)
        interval = non_paid_hours(user_chat_id)
        if interval:
            total_salary = 0
            message = ''
            counter = 0
            bot.send_message(msg.chat.id, f'Неоплаченные часы пользователя - {user_chat_id}:')
            
            for el in interval:
                if check_salary_exist != 0:
                    total_salary = total_salary + (el[3] * check_salary_exist)
                str_message = f'Дата: {el[2]} -- Часы: {el[3]}\n'
                message = message + str_message
                counter=counter+1
                if counter > 20:
                    bot.send_message(msg.chat.id, message)
                    counter = 0
                    message = ''
            if counter>0:
                bot.send_message(msg.chat.id, message)

            if total_salary != 0:
                bot.send_message(msg.chat.id, f'Итого: {total_salary} руб.', reply_markup=paid_salary())
                m = bot.send_message(msg.chat.id, 'Отметить выдачу?', reply_markup=paid_salary())
                bot.register_next_step_handler(m, paid_user_hours_step2, user_chat_id)
        
            else:
                bot.send_message(msg.chat.id, 'Чтобы увидеть итоговую ЗП - пользователь должен ввести ставку в час')
                
        else:
            bot.send_message(msg.chat.id, 'У пользователя нет неоплаченных часов')
    except:
        bot.reply_to(msg, 'Данные введены неверно', reply_markup=main_buttons())

def paid_user_hours_step2(m, user_chat_id):
    if m.text == 'Да':
        admin_paid_salary(user_chat_id)
        bot.send_message(m.chat.id, 'Готово', reply_markup=main_buttons())
    elif m.text == 'Назад':
        bot.send_message(m.chat.id, 'Возвращаю...', reply_markup=main_buttons())
    else: 
        bot.reply_to(m, 'Я Вас не понимаю', reply_markup=main_buttons())


def change_salary_step(msg):
    chat_id = msg.chat.id
    salary = msg.text
    check = change_salary(chat_id, salary)
    if(check):
        bot.send_message(msg.chat.id, 'Данные обновлены', reply_markup=main_buttons())
    else:
        bot.reply_to(msg, 'Данные введены неверно', reply_markup=main_buttons())

def enter_hours_step(msg):
    chat_id = msg.chat.id
    hours = msg.text
    try: 
        hours = int(hours)
        check = enter_hours(chat_id, hours)
        if(check):
            bot.send_message(msg.chat.id, 'Данные записаны', reply_markup=main_buttons())
        else:
            bot.send_message(msg.chat.id, 'Данные обновлены', reply_markup=main_buttons())
    except:
        bot.reply_to(msg, 'Данные введены неверно', reply_markup=main_buttons())

def choose_interval_step(msg):
    current_date = date.today()
    minus_week_date = current_date - timedelta(days=7)
    minus_month_date = current_date - timedelta(days=30)
    check_salary_exist = user_salary(msg.chat.id)
    if msg.text == 'Неделя':
        interval = choose_interval(msg.chat.id, current_date, minus_week_date)
        if interval:
            total_salary = 0
            message = ''
            counter = 0
            bot.send_message(msg.chat.id, f'Ваши неоплаченные часы за интервал: с {minus_week_date} по {current_date}:')
            
            for el in interval:
                if check_salary_exist != 0:
                    total_salary = total_salary + (el[3] * check_salary_exist)
                str_message = f'Дата: {el[2]} -- Часы: {el[3]}\n'
                message = message + str_message
                counter=counter+1
                if counter > 7:
                    bot.send_message(msg.chat.id, message)
                    counter = 0
                    message = ''
            if counter>0:
                bot.send_message(msg.chat.id, message)
            if total_salary != 0:
                bot.send_message(msg.chat.id, f'Итого: {total_salary} руб.')
            else:
                bot.send_message(msg.chat.id, 'Чтобы увидеть итоговую ЗП - введите ставку в час')
        else:
            bot.send_message(msg.chat.id, 'У вас нет неоплаченных часов')
            
    elif msg.text == 'Месяц':
        interval = choose_interval(msg.chat.id, current_date, minus_month_date)
        if interval:
            message = ''
            total_salary = 0
            counter = 0
            bot.send_message(msg.chat.id, f'Ваши неоплаченные часы за интервал: с {minus_month_date} по {current_date}:')
            for el in interval:
                if check_salary_exist != 0:
                    total_salary = total_salary + (el[3] * check_salary_exist)
                str_message = f'Дата: {el[2]} -- Часы: {el[3]}\n'
                message = message + str_message
                counter=counter+1
                if counter > 30:
                    bot.send_message(msg.chat.id, message)
                    counter = 0
                    message = ''
            if(counter>0):
                bot.send_message(msg.chat.id, message)
            if total_salary != 0:
                bot.send_message(msg.chat.id, f'Итого: {total_salary} руб.')
            else:
                bot.send_message(msg.chat.id, 'Чтобы увидеть итоговую ЗП - введите ставку в час')
        else:
            bot.send_message(msg.chat.id, 'У вас нет неоплаченных часов')

    elif msg.text == 'Назад':
        bot.send_message(msg.chat.id, 'Возвращаю...', reply_markup=main_buttons())

    else:
        try:
            user_date = msg.text
            minus_user_date = datetime.datetime.strptime(user_date, "%d %m %Y").date()
            print(minus_user_date)
            interval = choose_interval(msg.chat.id, current_date, minus_user_date)
            if interval:
                message = ''
                total_salary = 0
                counter = 0
                bot.send_message(msg.chat.id, f'Ваши неоплаченные часы за интервал: с {minus_user_date} по {current_date}:')
                for el in interval:
                    if check_salary_exist != 0:
                        total_salary = total_salary + (el[3] * check_salary_exist)
                    str_message = f'Дата: {el[2]} -- Часы: {el[3]}\n'
                    message = message + str_message
                    counter=counter+1
                    if counter > 50:
                        bot.send_message(msg.chat.id, message)
                        counter = 0
                        message = ''
                if(counter>0):
                    bot.send_message(msg.chat.id, message)
                if total_salary != 0:
                    bot.send_message(msg.chat.id, f'Итого: {total_salary} руб.')
                else:
                    bot.send_message(msg.chat.id, 'Чтобы увидеть итоговую ЗП - введите ставку в час')
            else: 
                bot.send_message(msg.chat.id, 'У вас нет неоплаченных часов')
        except:
            bot.send_message(msg.chat.id, 'Данные введены неверно')


    
    


bot.polling(none_stop=True)