from telebot import types

def main_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    order_key = types.KeyboardButton(text="Ввести/изменить часы")
    coupons_key = types.KeyboardButton(text="Посмотреть часы")
    keyboard.row(order_key, coupons_key)
    cards_key = types.KeyboardButton(text="Изменить ставку в час")
    app_key = types.KeyboardButton(text="Помощь")
    keyboard.add(cards_key, app_key)
    return keyboard

def reg_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    agree_key = types.KeyboardButton(text="Да", request_contact=True)
    disagree_key = types.KeyboardButton(text="Нет")
    keyboard.add(agree_key, disagree_key)
    return keyboard

def choose_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    week_key = types.KeyboardButton(text="Неделя")
    month_key = types.KeyboardButton(text="Месяц")
    keyboard.add(week_key, month_key)
    return keyboard