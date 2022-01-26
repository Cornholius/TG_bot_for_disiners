from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


check_money_btn = InlineKeyboardButton(text='Узнать баланс', callback_data='BALANCE_check_balance')
give_money_btn = InlineKeyboardButton(text='Пополнить баланс', callback_data='BALANCE_replenish_balance')
submit_order_btn = InlineKeyboardButton(text='Разместить объявление', callback_data='CREATE_MESSAGE_enter_task')
main_menu = InlineKeyboardMarkup(row_width=2)
main_menu.insert(give_money_btn)
main_menu.insert(check_money_btn)
main_menu.insert(submit_order_btn)
