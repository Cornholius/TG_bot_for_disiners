from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# --- Меню выбора роли ---
roleMenu = InlineKeyboardMarkup(row_width=1)
customerBtn = InlineKeyboardButton(text='Заказчик', callback_data='mainMenuCustomer')
# designerBtn = InlineKeyboardButton(text='Дизайнер', callback_data='mainMenuCustomer')
roleMenu.insert(customerBtn)
# roleMenu.insert(designerBtn)

#  --- Меню Заказчика ---
give_money_btn = KeyboardButton('Пополнить баланс')
check_moneyt_btn = KeyboardButton('Узнать баланс')
submit_order_btn = KeyboardButton('Разместить объявление')
make_a_newsletter_btn = KeyboardButton('Сделать рассылку')
rtfm_btn = KeyboardButton('Помощь')
customerMenu = ReplyKeyboardMarkup(resize_keyboard=True)
customerMenu.row(give_money_btn, check_moneyt_btn)
customerMenu.row(submit_order_btn, make_a_newsletter_btn)
customerMenu.add(rtfm_btn)
