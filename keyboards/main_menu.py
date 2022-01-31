from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import menu_callback

# callback_data=menu_callback.new(btn='main_menu')

check_money_btn = InlineKeyboardButton(
    text='Узнать баланс',
    callback_data=menu_callback.new(btn='BALANCE_check_balance'))

give_money_btn = InlineKeyboardButton(
    text='Пополнить баланс',
    callback_data=menu_callback.new(btn='BALANCE_replenish_balance'))

make_announcement_btn = InlineKeyboardButton(
    text='Разместить объявление',
    callback_data=menu_callback.new(btn='MESSAGE_announcement'))

make_newsletter_btn = InlineKeyboardButton(
    text='Сделать рассылку (пока не работает)',
    callback_data=menu_callback.new(btn='CREATE_MESSAGE_newsletter'))

rtfm_btn = InlineKeyboardButton(
    text='Помощь (пока не работает)',
    callback_data=menu_callback.new(btn='help'))

rates_btn = InlineKeyboardButton(
    text='Тарифы (пока не работает)',
    callback_data=menu_callback.new(btn='rates'))

main_menu = InlineKeyboardMarkup(row_width=2)

main_menu.insert(check_money_btn)
main_menu.insert(give_money_btn)
main_menu.insert(make_announcement_btn)
main_menu.insert(make_newsletter_btn)
main_menu.insert(rates_btn)
main_menu.insert(rtfm_btn)
