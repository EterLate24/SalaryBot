from telebot import types

def main_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    order_key = types.KeyboardButton(text="Ввести часы")
    coupons_key = types.KeyboardButton(text="Посмотреть часы")
    keyboard.row(order_key, coupons_key)
    cards_key = types.KeyboardButton(text="Регистрация")
    app_key = types.KeyboardButton(text="Помощь")
    keyboard.add(cards_key, app_key)
    return keyboard