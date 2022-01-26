from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# --- Меню выбора роли ---


#  --- Меню Заказчика ---
# give_money_btn = KeyboardButton('Пополнить баланс')
# check_moneyt_btn = KeyboardButton('Узнать баланс')
# submit_order_btn = KeyboardButton('Разместить объявление')
# make_a_newsletter_btn = KeyboardButton('Сделать рассылку')
# rtfm_btn = KeyboardButton('Помощь')
# main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
# main_menu.row(give_money_btn, check_moneyt_btn)
# main_menu.row(submit_order_btn, make_a_newsletter_btn)
# main_menu.add(rtfm_btn)

#  --- Объявление ---
# need_image_btn = KeyboardButton('Да')
# no_need_image_btn = KeyboardButton('Нет')
# taskMenu = ReplyKeyboardMarkup(resize_keyboard=True)
# taskMenu.row(need_image_btn, no_need_image_btn)

#  --- Меню Заказчика ---
check_moneyt_btn = InlineKeyboardButton(text='Узнать баланс', callback_data='BALANCE_check_balance')
give_money_btn = InlineKeyboardButton(text='Пополнить баланс', callback_data='BALANCE_replenish_balance')
submit_order_btn = InlineKeyboardButton(text='Разместить объявление', callback_data='CREATE_MESSAGE_enter_task')
customerMenu = InlineKeyboardMarkup(row_width=2)
customerMenu.insert(give_money_btn)
customerMenu.insert(check_moneyt_btn)
customerMenu.insert(submit_order_btn)

#  --- Объявление ---
need_image_btn = KeyboardButton(text='Да', callback_data='CREATE_MESSAGE_need_image')
no_need_image_btn = KeyboardButton(text='Нет', callback_data='CREATE_MESSAGE_no_need_image')
in_channel_btn = InlineKeyboardButton(text='В канал', callback_data='CREATE_MESSAGE_choiseChannel')
in_newsletter_btn = InlineKeyboardButton(text='В рассылку', callback_data='CREATE_MESSAGE_choiseNewsletter')
to_main_menu_btn = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
image_complete_btn = InlineKeyboardButton(text='Готово, поехали дальше', callback_data='ololo2')

taskMenu = InlineKeyboardMarkup(row_width=2)
task_choise_menu = InlineKeyboardMarkup(row_width=1)
to_main_menu = InlineKeyboardMarkup(row_width=1)
image_complete = InlineKeyboardMarkup(row_width=1)

taskMenu.insert(need_image_btn)
taskMenu.insert(no_need_image_btn)
taskMenu.insert(to_main_menu_btn)

task_choise_menu.insert(in_channel_btn)
task_choise_menu.insert(in_newsletter_btn)

to_main_menu.insert(to_main_menu_btn)

image_complete.insert(image_complete_btn)