from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# --- Меню выбора роли ---
customerBtn = KeyboardButton('Заказчик')
designerBtn = KeyboardButton('Дизайнер')
roleMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(customerBtn, designerBtn)