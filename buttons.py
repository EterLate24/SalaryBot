from telebot import types

def back_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_key = types.KeyboardButton(text="Назад")
    keyboard.add(back_key)
    return keyboard

def main_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    order_key = types.KeyboardButton(text="Ввести/изменить часы")
    coupons_key = types.KeyboardButton(text="Посмотреть часы")
    keyboard.row(order_key, coupons_key)
    cards_key = types.KeyboardButton(text="Ввести/изменить ставку в час")
    app_key = types.KeyboardButton(text="Помощь")
    keyboard.row(cards_key, app_key)
    admin_key = types.KeyboardButton(text="Администратор")
    keyboard.add(admin_key)
    return keyboard

def reg_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    agree_key = types.KeyboardButton(text="Да", request_contact=True)
    disagree_key = types.KeyboardButton(text="Нет")
    keyboard.add(agree_key, disagree_key)
    return keyboard

def admin_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    view_user_hours = types.KeyboardButton(text='Посмотреть список пользователей')
    keyboard.row(view_user_hours)
    paid_user_hours = types.KeyboardButton(text='Отметить часы пользователя')
    keyboard.row(paid_user_hours)
    back_key = types.KeyboardButton(text="Назад")
    keyboard.add(back_key)
    return keyboard

def choose_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    week_key = types.KeyboardButton(text="Неделя")
    month_key = types.KeyboardButton(text="Месяц")
    back_key = types.KeyboardButton(text="Назад")
    keyboard.add(week_key, month_key, back_key)
    return keyboard

def paid_salary():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    paid_key = types.KeyboardButton(text="Да")
    back_key = types.KeyboardButton(text="Назад")
    keyboard.add(paid_key, back_key)
    return keyboard