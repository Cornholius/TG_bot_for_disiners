from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# --- Меню выбора роли ---
roleMenu = InlineKeyboardMarkup(row_width=1)
customerBtn = InlineKeyboardButton(text='Заказчик', callback_data='mainMenuCustomer')
# designerBtn = InlineKeyboardButton(text='Дизайнер', callback_data='mainMenuCustomer')
roleMenu.insert(customerBtn)
# roleMenu.insert(designerBtn)

#  --- Меню Заказчика ---
giveMoneyBtn = KeyboardButton('Пополнить баланс')
checkMoneytBtn = KeyboardButton('Узнать баланс')
submitOrderBtn = KeyboardButton('Разместить объявление')
customerMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(giveMoneyBtn, checkMoneytBtn, submitOrderBtn)
