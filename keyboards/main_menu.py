from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


check_money_btn = InlineKeyboardButton(text='Узнать баланс', callback_data='BALANCE_check_balance')
give_money_btn = InlineKeyboardButton(text='Пополнить баланс', callback_data='BALANCE_replenish_balance')
make_announcement_btn = InlineKeyboardButton(text='Разместить объявление', callback_data='CREATE_MESSAGE_enter_task')
make_newsletter_btn = InlineKeyboardButton(text='Сделать рассылку', callback_data='CREATE_MESSAGE_newsletter')
rtfm_btn = InlineKeyboardButton(text='Помощь', callback_data='help')
rates_btn = InlineKeyboardButton(text='Тарифы', callback_data='rates')

main_menu = InlineKeyboardMarkup(row_width=2)

main_menu.insert(check_money_btn)
main_menu.insert(give_money_btn)
main_menu.insert(make_announcement_btn)
main_menu.insert(make_newsletter_btn)
main_menu.insert(rates_btn)
main_menu.insert(rtfm_btn)
